# Device Fingerprint Analyzer

![Project Status](https://img.shields.io/badge/status-early%20development-orange)

## Features:
- Generates a unique fingerprint for each user's device using a wide range of metrics, primarily collected via client-side JavaScript, with some additional server-side data.
- A ML model to determine whether two device fingerprints belong to the same user. (Not yet implemented)
- Potential integration with Selenium to simulate diverse user traffic. (Not yet implemented)

- TODO: Mechanism needs to be implemented to prevent duplicate fingerprints. Currently each visit on homepage generates a new fingerprint.

## Usage

### Clone
```bash
git clone https://github.com/lllDavid/device_fingerprint_analyzer
```
### Change Directory
```bash
cd device_fingerprint_analyzer
```

### Install
```bash
pip install -r requirements.txt
```

### Apply Migrations
```bash
cd website
python manage.py migrate
```
### Run the Django Application (Website)
```bash
python manage.py runserver
```
## Fingerprint
- On visiting the homepage (http://127.0.0.1:8000/) a fingerprint is generated and printed in the Browsers console. 
- It is then saved in the database (both as complete fingerprint aswell as its sub components). 
- To populate the Fingerprint Dataclass one can use create_fingerprint_instance in website/fingerprint/helpers.py. 
- To retrieve the complete Fingerprint as dictionary use fetch_full_fingerprint in website/fingerprint/helpers.py.
- Any Selenium or ML Model logic isnt yet implemented.

## Components
Fingerprint Dataclass:
- Located at data/fingerprint.py

Fingerprint Script:
- Located at scripts/fingerprint.js