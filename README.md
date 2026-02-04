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
