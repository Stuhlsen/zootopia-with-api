# Zootopia With API 🦊

This project generates a simple animal website (`animals.html`) based on live animal data fetched from the
:contentReference[oaicite:0]{index=0} Animals API.

It is a refactored, multi-file version of the original “Zootopia” generator:  
- **Data Fetcher**: retrieves animal data (independent of HTML generation)  
- **Website Generator**: renders the website from the fetched data

---

## How it works

### Architecture
- `data_fetcher.py`  
  Fetches animal data from the API and returns a **list of dictionaries** in the expected format:
  `name`, `taxonomy`, `locations`, `characteristics`.

- `animals_web_generator.py`  
  Prompts the user for an animal name, calls the data fetcher, and generates `animals.html` using
  `animals_template.html`.

---

## Project structure

```text
.
├── animals_web_generator.py   # CLI entry point (website generator)
├── data_fetcher.py            # API client (data fetcher)
├── animals_template.html      # HTML template with placeholder
├── animals.html               # generated output (created after running the script)
├── requirements.txt           # dependencies
├── .env                       # API key (local only; must NOT be committed)
└── .gitignore                 # ignores .env and other files
```
---

## ✅ Requirements

- Python 3.10+ recommended

- API Ninjas account + API key

- Internet connection (for API requests)

## Installation
```text
pip install -r requirements.txt
```

On Windows:
```text
py -m pip install -r requirements.txt
```
## Configuration

Create a .env file in the project root:
```text
API_NINJAS_KEY=your_api_key_here
```
## Usage
```text
python animals_web_generator.py
```

Example:
```text
Please enter an animal: Fox
Website was successfully generated to the file animals.html.
```

Open animals.html in your browser.

## Notes

The generator injects HTML into animals_template.html via a placeholder:
__REPLACE_ANIMALS_INFO__ (update the constant in the generator if yours differs).

If the API returns no results, the website shows a friendly “not found” message.

## License

Educational / learning project.