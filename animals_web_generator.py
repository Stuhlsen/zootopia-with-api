from typing import Any

import data_fetcher


TEMPLATE_FILE = "animals_template.html"
OUTPUT_FILE = "animals.html"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def _safe_characteristics(animal: dict[str, Any]) -> dict[str, Any]:
    characteristics = animal.get("characteristics")
    return characteristics if isinstance(characteristics, dict) else {}


def _safe_locations(animal: dict[str, Any]) -> list[str]:
    locations = animal.get("locations")
    if isinstance(locations, list):
        return [str(x).strip() for x in locations if str(x).strip()]
    return []


def build_animal_card(animal: dict[str, Any]) -> str:
    """Build one HTML card (<li>...</li>) matching the template CSS classes."""
    name = str(animal.get("name", "Unknown")).strip()
    characteristics = _safe_characteristics(animal)
    locations = _safe_locations(animal)

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
    """Build HTML list items for all animals."""
    return "\n\n".join(build_animal_card(animal) for animal in animals)


def build_not_found_html(animal_name: str) -> str:
    """Build a styled message if no animals are found."""
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


def load_template() -> str:
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        return file.read()


def write_output(html: str) -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(html)


def render_page(template: str, content_html: str) -> str:
    if PLACEHOLDER not in template:
        raise ValueError(
            f"Placeholder '{PLACEHOLDER}' not found in {TEMPLATE_FILE}."
        )
    return template.replace(PLACEHOLDER, content_html)


def main() -> None:
    animal_name = input("Please enter an animal: ").strip()

    template = load_template()
    animals = data_fetcher.fetch_data(animal_name)

    if animals:
        animals_html = build_animals_html(animals)
    else:
        animals_html = build_not_found_html(animal_name)

    final_html = render_page(template, animals_html)
    write_output(final_html)

    print(f"Website was successfully generated to the file {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
