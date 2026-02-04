import os
from typing import Any

import requests
from dotenv import load_dotenv


API_URL = "https://api.api-ninjas.com/v1/animals"
ENV_KEY_NAME = "API_NINJAS_KEY"


def _load_api_key() -> str:
    """Load API key from .env/environment variables."""
    load_dotenv()
    api_key = os.getenv(ENV_KEY_NAME, "").strip()

    if not api_key:
        raise RuntimeError(
            f"Missing {ENV_KEY_NAME}. Create a .env file with "
            f"{ENV_KEY_NAME}=your_key"
        )

    return api_key


def fetch_data(animal_name: str) -> list[dict[str, Any]]:
    """
    Fetches the animals data for the animal 'animal_name'.

    Returns:
        A list of animals, each animal is a dictionary:
        {
          'name': ...,
          'taxonomy': {...},
          'locations': [...],
          'characteristics': {...}
        }
    """
    api_key = _load_api_key()

    headers = {"X-Api-Key": api_key}
    params = {"name": animal_name}

    response = requests.get(API_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        return []

    return data
