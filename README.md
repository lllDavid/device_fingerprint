# Device Fingerprint Analyzer

![Project Status](https://img.shields.io/badge/status-early%20development-orange)

## Features:
- Generates a unique fingerprint for each user's device using a wide range of metrics, primarily collected via client-side JavaScript, with some additional server-side data.
- A ML model to determine whether two device fingerprints belong to the same user. (Not yet implemented)
- Potential integration with Selenium to simulate diverse user traffic. (Not yet implemented)


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

### Run the Django Application (Website)
```bash
cd website
python manage.py runserver
```
## Fingerprint
On visiting the homepage (http://127.0.0.1:8000/) a fingerprint is generated and printed in the Browsers console.

## Components
Fingerprint Dataclass:
- Located at data/fingerprint.py and website/fingerprint/fingerprint.py

Collect Fingerprint Script:
- Located at scripts/collect_fingerprint.js and website/static/js/collect_fingerprint.js