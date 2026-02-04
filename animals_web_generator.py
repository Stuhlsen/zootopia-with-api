import os
from typing import Any

import requests
from dotenv import load_dotenv


API_URL = "https://api.api-ninjas.com/v1/animals"
TEMPLATE_FILE = "animals_template.html"
OUTPUT_FILE = "animals.html"


def load_api_key() -> str:
    """Load API Ninjas key from .env / environment variables."""
    load_dotenv()
    api_key = os.getenv("API_NINJAS_KEY", "").strip()
    if not api_key:
        raise RuntimeError("API_NINJAS_KEY fehlt. Prüfe deine .env Datei.")
    return api_key


def fetch_animals(animal_name: str, api_key: str) -> list[dict[str, Any]]:
    """Fetch animals from API Ninjas by name."""
    headers = {"X-Api-Key": api_key}
    params = {"name": animal_name}

    response = requests.get(API_URL, headers=headers, params=params, timeout=10)

    if response.status_code != 200:
        raise RuntimeError(
            f"API request failed ({response.status_code}): {response.text}"
        )

    data = response.json()
    if not isinstance(data, list):
        raise RuntimeError("Unerwartetes Antwortformat (kein List-JSON).")

    return data


def extract_display_fields(animal: dict[str, Any]) -> dict[str, str]:
    """Pick only the fields we want to display nicely on the website."""
    name = str(animal.get("name", "Unknown")).strip()

    characteristics = animal.get("characteristics") or {}
    taxonomy = animal.get("taxonomy") or {}
    locations = animal.get("locations") or []

    diet = str(characteristics.get("diet", "Unknown")).strip()

    # Many API responses have a useful "type" inside characteristics (e.g. Hound)
    # Fallback to taxonomy["class"] (e.g. Mammalia) if missing.
    animal_type = str(
        characteristics.get("type") or taxonomy.get("class") or "Unknown"
    ).strip()

    if isinstance(locations, list):
        location = ", ".join(str(x).strip() for x in locations if str(x).strip())
    else:
        location = str(locations).strip()

    return {
        "name": name,
        "diet": diet,
        "location": location or "Unknown",
        "type": animal_type,
    }


def build_animal_card_html(display: dict[str, str]) -> str:
    """Create one animal card (<li>...</li>) matching the template CSS classes."""
    name = display["name"].upper()
    diet = display["diet"]
    location = display["location"]
    animal_type = display["type"]

    return f"""
      <li class="cards__item">
        <div class="card">
          <div class="card__content">
            <div class="card__title">{name}</div>
            <p class="card__text"><span class="card__text-label">Diet:</span> {diet}</p>
            <p class="card__text"><span class="card__text-label">Location:</span> {location}</p>
            <p class="card__text"><span class="card__text-label">Type:</span> {animal_type}</p>
          </div>
        </div>
      </li>
    """.strip()


def generate_website(animals: list[dict[str, Any]]) -> None:
    """Generate animals.html from template and animal data."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        template = file.read()

    cards_html = "\n".join(
        build_animal_card_html(extract_display_fields(a))
        for a in animals
    )

    final_html = template.replace("__REPLACE_ANIMALS_INFO__", cards_html)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(final_html)


def main() -> None:
    api_key = load_api_key()

    # Milestone 1: fixed query "Fox"
    animals = fetch_animals("Fox", api_key)
    generate_website(animals)
    print(f"Website was successfully generated to the file {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
