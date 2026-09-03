# Fourfold

Fourfold is a focused, 15-question personality preference test built with Flask. It turns four familiar personality dimensions into a calm, one-question-at-a-time experience and shows the percentage balance behind the final four-letter result.

It is an independent reflection tool and is not affiliated with or certified by The Myers-Briggs Company.

## Highlights

- Progressive quiz flow with mouse, touch, and keyboard controls
- In-tab progress recovery after an accidental refresh
- Original profiles for all 16 results
- Percentage breakdowns for all four preference pairs
- Responsive layouts and reduced-motion support
- Feedback and confirmation flow

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Test

```bash
python -m unittest discover -s tests
```

For production, set a private `SECRET_KEY` environment variable. The included `Procfile` starts the app with Gunicorn.
