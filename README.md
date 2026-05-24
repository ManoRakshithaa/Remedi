# Remedi — Medicine Adherence Tracker & Daily Streaks

## Overview
**Remedi** is a small **Flask** web application backed by a **SQLite** database. It helps users:
- Maintain a list of medicines (with daily reminder times)
- Mark medicines as “taken” for the current day
- Track a simple **daily adherence streak** based on whether **all medicines** have been taken

The app is designed as a lightweight CRUD-like medicine tracker with a streak mechanism.

---

## Key Features
- **SQLite-backed data storage**
  - Stores medicines with:
    - medicine name/details
    - reminder time (`reminder_time`)
    - taken status (`taken`)
    - the date the medicine was taken (`taken_date`)
- **Daily adherence streak tracking**
  - Maintains a `streaks` table that records whether a day is completed (`completed = 1`)
  - A day is marked completed when the user has marked **all medicines as taken**
- **Web UI (Flask routes)**
  - **Home (`/`)**
    - Lists all medicines ordered by `reminder_time`
    - Shows the number of days with completed streak entries (`completed = 1`)
  - **Add medicine (`/add`)**
    - Form-based addition (GET shows form, POST creates medicine record)
    - Formats and stores `reminder_time` (optionally including a “food” component)
  - **Mark medicine as taken (`/taken/<medicine_id>`)**
    - Sets `taken = 1` and `taken_date = today` for the selected medicine
    - Ensures today’s streak entry exists in `streaks` with `completed = 1` when all medicines are taken
  - **Delete medicine (`/delete/<medicine_id>`)**
    - Removes a medicine record from the database

---

## Tech Stack
- **Python**
- **Flask**: Web framework / routing / templating
- **SQLite**: Local relational database
- **Gunicorn**: Production WSGI server
- Supporting Flask ecosystem libraries (as listed in dependencies):
  - Jinja2, MarkupSafe, itsdangerous, Werkzeug
  - Click, Blinker

---

## Project Architecture
### Application Layer
- **`app.py`**
  - Implements the Flask application and all core request handlers.
  - Responsibilities:
    - Initialize and migrate database schema at startup via `init_db`
    - Serve web routes for listing, adding, updating, and deleting medicines
    - Coordinate streak logic based on medicine completion state

### Database Layer (SQLite)
`app.py` creates and uses two tables:

1. **`medicines`**
   - Stores each medicine’s core attributes:
     - medicine details (e.g., name fields from the add form)
     - `reminder_time`
     - `taken` flag
     - `taken_date` (date the medicine was marked taken)

2. **`streaks`**
   - Stores daily completion:
     - a date field (daily granularity)
     - `completed` flag indicating whether the day is fully completed

### Route Behavior (Core Flow)
- **Startup**
  - `init_db` runs when the app starts to ensure the schema exists.

- **Home (`/`)**
  - Fetches all medicines from `medicines`, ordered by `reminder_time`
  - Computes streak summary by counting streak rows where `completed = 1`

- **Add (`/add`)**
  - **GET**: renders the add medicine form
  - **POST**:
    - reads medicine fields from the submitted form
    - formats `reminder_time` (optionally including “food”)
    - inserts the new record into `medicines`
    - redirects back to `/`

- **Mark Taken (`/taken/<medicine_id>`)**
  - Updates the selected medicine:
    - `taken = 1`
    - `taken_date = today`
  - Checks whether all medicines are marked taken (based on the `taken = 1` count)
  - If all are taken, ensures today’s record exists in `streaks` and sets `completed = 1`

- **Delete (`/delete/<medicine_id>`)**
  - Deletes the medicine row by ID from `medicines`
  - redirects back to `/`

---

## Installation (Placeholder)
> Instructions below are placeholders—use your environment and the repository’s `requirements.txt`.

1. Clone the repository:
   bash
   git clone <repository-url>
   cd Remedi
   
2. Create and activate a virtual environment (recommended):
   bash
   python -m venv .venv
   source .venv/bin/activate
   
3. Install dependencies:
   bash
   pip install -r requirements.txt
   

---

## Usage (Placeholder)
### Run the development server
bash
python app.py


### Run with Gunicorn (production-style)
bash
gunicorn app:app


### Access the app
Open your browser to the server address (commonly):
- `http://127.0.0.1:5000`

---

## Notes for Developers
- The streak logic is based on whether **all medicines** are marked taken (`taken = 1`), and it updates/ensures today’s `streaks` entry with `completed = 1`.
- Database schema is created at startup via `init_db` within `app.py`.

---
*This README was generated with [PresentMe](https://www.presentmeapp.xyz/). View the full presentation [here](https://www.presentmeapp.xyzhttp://localhost:5000/p/ba766500-f661-4e47-a604-6a682a0eeabd).*
