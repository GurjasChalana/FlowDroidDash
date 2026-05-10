# FlowDroid Dashboard

A Flask dashboard for viewing FlowDroid taint analysis reports and uploading APKs for analysis.

## Setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Run

```bash
.venv/bin/python dashboard/app.py
```

Open http://127.0.0.1:5000/.

## Analysis Notes

APK analysis requires:

- Java available on `PATH`
- Android SDK platforms at `/opt/android-sdk/platforms/`
- `GROQ_API_KEY` set in the environment for report summaries and fallback sink classification

