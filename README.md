# Device Fingerprint
- This application creates a unique device fingerprint using client-side JavaScript and server-side data, with implemented support for conversion to a dataclass, dictionary, and flattened structure, enabling consistent identification across different environments.

## Features
### Implemented
- Generates a unique device fingerprint

- Supports conversion to a dataclass, standard dictionary, and flattened dictionary format

- Includes a Django-based e-commerce example application to demonstrate integration and usage

### Planned
- A ML model to determine whether two device fingerprints belong to the same user

- Potential integration with Selenium to simulate diverse user traffic

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
- On visiting the homepage (http://127.0.0.1:8000/) a fingerprint is generated and logged to the browser console

- Fingerprint data Conversion functions are located at website/fingerprint/helpers.py 

## Components
Fingerprint Dataclass:
- Located in data/fingerprint.py

Fingerprint Script:
- Located at scripts/fingerprint.js