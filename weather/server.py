import asyncio
import os
import json
from pathlib import Path
from typing import Dict, Optional, Any
from dotenv import load_dotenv
from aiohttp import ClientSession

load_dotenv()

# Cache configuration
CACHE_DIR = Path.home() / '.cache' / 'weather'
LOCATION_CACHE_FILE = CACHE_DIR / 'location_cache.json'

ACCUWEATHER_API_KEY = os.getenv('ACCUWEATHER_API_KEY')
BASE_URL = 'http://dataservice.accuweather.com'


async def get_cached_location_key(location: str) -> Optional[str]:
  """Get location key from cache."""
  if not LOCATION_CACHE_FILE.exists():
    return None

  try:
    with open(LOCATION_CACHE_FILE, 'r') as f:
      cache = json.load(f)
      return cache.get(location)
  except (json.JSONDecodeError, FileNotFoundError):
    return None


async def get_location_key(location: str) -> str:
  """Get location key from cache."""

  location_key = await get_cached_location_key(location)

  if location_key:
    return location_key
  else:
    async with ClientSession() as session:
      async with session.get(
        f'{BASE_URL}/locations/v1/cities/search', params={'apikey': ACCUWEATHER_API_KEY, 'q': location}
      ) as resp:
        data = await resp.json()

        if len(data) == 0:
          raise ValueError(f'Location not found: {location}')

        location_key = data[0]['Key']

        # Save to cache
        try:
          if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True, exist_ok=True)

          if LOCATION_CACHE_FILE.exists():
            with open(LOCATION_CACHE_FILE, 'r') as f:
              cache = json.load(f)
          else:
            cache = {}

          cache[location] = location_key
          with open(LOCATION_CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
        except Exception as e:
          print(f'Warning: Failed to cache location key: {e}')

        return location_key


async def get_daily_weather(location: str, days: int = 5) -> Dict[str, Any]:
  location_key = await get_location_key(location)

  print('location_key: ', location_key)

  async with ClientSession() as session:
    async with session.get(
      f'{BASE_URL}/forecasts/v1/daily/{days}day/{location_key}',
      params={'apikey': ACCUWEATHER_API_KEY, 'metric': 'true'},
    ) as resp:
      data = await resp.json()

      if 'DailyForecasts' not in data:
        raise ValueError(f'Failed to get weather data: {data}')

  return data['DailyForecasts']


if __name__ == '__main__':
  print(asyncio.run(get_daily_weather('Ho Chi Minh', 5)))
