from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import yaml
ROOT = Path(__file__).resolve().parents[1]
def load_config(path='config/config.yaml'):
    p=Path(path); p=p if p.is_absolute() else ROOT/p
    cfg=yaml.safe_load(p.read_text()) or {}; cfg['_root']=str(ROOT)
    cfg['event']=todays_event(cfg)
    return cfg
def todays_event(cfg,today=None):
    """Unlike edmonton_folk_fest (one fixed venue all festival), this event
    moves to a different park every show night across two ESO series
    (Symphony in the Park, Symphony Under the Sky) - see config/schedule.json.
    Returns None on any date with no scheduled show, which run_demo.py and
    watch.py both treat as "nothing to do today", so this pipeline stays
    completely idle (no network calls, no publish) between show nights."""
    schedule=json.loads((ROOT/'config'/'schedule.json').read_text())
    tz=ZoneInfo(cfg.get('project',{}).get('timezone','America/Edmonton'))
    date_str=today or datetime.now(tz).strftime('%Y-%m-%d')
    entry=schedule.get(date_str)
    if not entry:return None
    return {
        'name':'Edmonton Symphony Orchestra Outdoor Concert',
        'venue':entry['venue'],
        'city':entry.get('city'),
        'latitude':entry['latitude'],
        'longitude':entry['longitude'],
        'local_radius_km':10,
        'influence_radius_km':20,
        'dates':date_str,
        'show_time_local':entry.get('time_local'),
        'series':entry.get('series'),
        'concluded':False,
    }
def resolve_path(cfg,value):
    p=Path(value); return p if p.is_absolute() else Path(cfg['_root'])/p
