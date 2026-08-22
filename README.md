# Edmonton Symphony Orchestra Outdoor Concerts — Environmental Intelligence

Sit-rep pipeline for the ESO's outdoor concert season: weather, AQHI, wildfire
smoke, nearby traffic cameras, and lightning/severe-weather watch, scoped to
whichever park is hosting that night's show.

Unlike `edmonton_folk_fest`/`riders_sitrep` (one fixed venue for the whole
run), this event moves to a different park roughly weekly across two ESO
series — Symphony in the Park (five one-off community parks) and Symphony
Under the Sky (Hawrelak Park, several nights). `config/schedule.json` maps
each show date to its venue; `core/config.py` looks up today's date and
injects the right venue into `cfg['event']` on every run. On any date with no
scheduled show, `cfg['event']` is `None` and both `run_demo.py` and
`watch.py` exit immediately — no network calls, no publish, nothing changes
in `docs/` between show nights.

To add or correct a date, edit `config/schedule.json` directly — no other
code needs to change.

## Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_demo.py
xdg-open output/dashboard.html
```

`data_mode: auto` attempts live Open-Meteo weather and falls back to bundled
samples. Requires `FIRMS_API_KEY` and `AB511_API_KEY` in the environment
(see `/opt/airquality/config/intelligence.env` on the server, or this repo's
own `.env`, gitignored).

## Test

```bash
python -m unittest discover -s tests -v
```

## Outputs

- `output/dashboard.html`
- `output/sitrep.pdf`
- `output/dashboard_data.json`
- `output/intelligence_summary.json`
- `output/run.log`
