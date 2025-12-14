# ANPR-System

Automatic Number Plate Recognition (ANPR) Project using Python, OpenCV, and EasyOCR.

## Features
- Detect license plates from images or video.
- Check against a database of stolen vehicles.
- Alerts via Streamlit interface .

## Setup
1. Clone the repository
2. Create a virtual environment
3. Install requirements:

pip install -r requirements.txt

4. Run Streamlit app:
streamlit run lnpr_streamlit.py

## Files
- `lnpr.py` → Core ANPR logic
- `lnpr_streamlit.py` → Web interface
- `populate_stolen.py` → Populate database
- `anpr_system.db` → SQLite database
