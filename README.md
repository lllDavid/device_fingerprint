# Device Fingerprint

![Project Status](https://img.shields.io/badge/status-early%20development-orange)

## Features
### Implemented
- Generates a fingerprint for each user's device using a wide range of metrics, primarily collected via client-side JavaScript, with some additional server-side data.

- Example Django-based E-Commerce store to demonstrate integration and usage.

### Planned
- A ML model to determine whether two device fingerprints belong to the same user.

- Potential integration with Selenium to simulate diverse user traffic. 

- TODO: Mechanism needs to be implemented to prevent duplicate fingerprints. Currently each visit on homepage generates a new fingerprint.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/lllDavid/device_fingerprint
```
### 2. Install dependencies

**Navigate to the directory:**
```bash
cd device_fingerprint
```

**Create a virtual environment:**
```bash
python -m venv venv
```

**Activate the virtual environment:**
```bash
.\venv\Scripts\activate
```

**Install requirements:**
```bash
pip install -r requirements.txt
```
### 3. Apply Migrations
```bash
cd website
python manage.py migrate
```
### 4. Run the Django Application
```bash
python manage.py runserver
```
## Fingerprint
- On visiting the homepage (http://127.0.0.1:8000/), a device fingerprint is generated and logged to the browser console.

- It is then saved in the database (both as complete fingerprint aswell as its sub components). 

- To populate the Fingerprint Dataclass, use the create_fingerprint_instance function in website/fingerprint/helpers.py. 

- To retrieve the complete Fingerprint as dictionary use fetch_full_fingerprint in website/fingerprint/helpers.py.

## Components
Fingerprint Dataclass:
- Located in data/fingerprint.py

Fingerprint Script:
- Located at scripts/fingerprint.js