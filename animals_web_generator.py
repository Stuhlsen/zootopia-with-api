import os
from typing import Any

import requests
from dotenv import load_dotenv


API_URL = "https://api.api-ninjas.com/v1/animals"
TEMPLATE_FILE = "animals_template.html"
OUTPUT_FILE = "animals.html"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def load_api_key() -> str:
    """Load the API Ninjas key from .env and return it."""
    load_dotenv()
    api_key = os.getenv("API_NINJAS_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "Missing API_NINJAS_KEY. Create a .env file with "
            "API_NINJAS_KEY=your_key"
        )

    return api_key


def fetch_animals(animal_name: str, api_key: str) -> list[dict[str, Any]]:
    """Fetch animals data from API Ninjas for a given animal name."""
    headers = {"X-Api-Key": api_key}
    params = {"name": animal_name}

    response = requests.get(
        API_URL,
        headers=headers,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        return []

    return data


def safe_get_characteristics(animal: dict[str, Any]) -> dict[str, Any]:
    """Return characteristics dict or an empty dict if missing/invalid."""
    characteristics = animal.get("characteristics")
    if isinstance(characteristics, dict):
        return characteristics
    return {}


def safe_get_locations(animal: dict[str, Any]) -> list[str]:
    """Return locations list or an empty list if missing/invalid."""
    locations = animal.get("locations")
    if isinstance(locations, list):
        return [str(x).strip() for x in locations if str(x).strip()]
    return []


def build_animal_card(animal: dict[str, Any]) -> str:
    """Build one HTML card (<li>...</li>) matching the template CSS classes."""
    name = str(animal.get("name", "Unknown")).strip()
    characteristics = safe_get_characteristics(animal)
    locations = safe_get_locations(animal)

    diet = str(characteristics.get("diet", "Unknown")).strip()
    animal_type = str(characteristics.get("type", "Unknown")).strip()
    location_text = ", ".join(locations) if locations else "Unknown"

    return (
        f'<li class="cards__item">\n'
        f'  <div class="card">\n'
        f'    <div class="card__content">\n'
        f'      <div class="card__title">{name.upper()}</div>\n'
        f'      <p class="card__text"><strong>Diet:</strong> {diet}</p>\n'
        f'      <p class="card__text"><strong>Location:</strong> '
        f"{location_text}</p>\n"
        f'      <p class="card__text"><strong>Type:</strong> '
        f"{animal_type}</p>\n"
        f"    </div>\n"
        f"  </div>\n"
        f"</li>"
    )


def build_animals_html(animals: list[dict[str, Any]]) -> str:
    """Build HTML for all animals returned by the API."""
    return "\n\n".join(build_animal_card(animal) for animal in animals)


def load_template() -> str:
    """Load the HTML template from disk."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        return file.read()


def write_output(html: str) -> None:
    """Write the final HTML to the output file."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(html)


def render_page(template: str, content_html: str) -> str:
    """Replace the placeholder in the template with generated HTML."""
    if PLACEHOLDER not in template:
        raise ValueError(
            f"Placeholder '{PLACEHOLDER}' not found in {TEMPLATE_FILE}. "
            "Check your template file."
        )

    return template.replace(PLACEHOLDER, content_html)


def build_not_found_message(animal_name: str) -> str:
    """Return a friendly message HTML if no animals were found."""
    safe_name = animal_name.strip()
    return (
        f'<li class="cards__item">\n'
        f'  <div class="card">\n'
        f'    <div class="card__content">\n'
        f'      <div class="card__title">NOT FOUND</div>\n'
        f'      <p class="card__text">The animal "{safe_name}" doesn\'t exist.</p>\n'
        f"    </div>\n"
        f"  </div>\n"
        f"</li>"
    )


def main() -> None:
    """Run the generator: ask user, fetch data, generate HTML file."""
    api_key = load_api_key()
    animal_name = input("Enter a name of an animal: ").strip()

    template = load_template()

    if not animal_name:
        content_html = build_not_found_message("")

    else:
        animals = fetch_animals(animal_name, api_key)
        if animals:
            content_html = build_animals_html(animals)
        else:
            content_html = build_not_found_message(animal_name)

    final_html = render_page(template, content_html)
    write_output(final_html)

    print(f"Website was successfully generated to the file {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
