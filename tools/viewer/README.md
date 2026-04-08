# OpenDream Live Viewer

An optional browser-based viewer that displays dream events in real-time as
they are written during the night. This tool is **not** part of the core
OpenDream skill — it is a developer/observer utility.

## Prerequisites

- Python 3.10+
- An installed OpenDream workspace (see the main [README](../../README.md))

## Install

Install the viewer dependencies (these are **not** installed by `setup.py`):

```bash
pip install aiohttp watchdog
```

## Usage

```bash
# From the skill root
python3 tools/viewer/dream_events.py

# Or with an explicit workspace path
python3 tools/viewer/dream_events.py /path/to/workspace

# Custom port (default: 9736)
python3 tools/viewer/dream_events.py --port 9736
```

Then open **http://localhost:9736** in your browser.

## What It Does

- Watches the `dreams/` directory for new or modified `.md` files
- Streams events over WebSocket at `ws://localhost:9736/opendream.stream`
- Serves a self-contained HTML viewer at `GET /`

### Events

| Event | Trigger |
|-------|---------|
| `dream_start` | First cycle file of the night created |
| `cycle_start` | New `cycle-N-name.md` file created |
| `thought` | Content appended to a cycle file |
| `morning_recall` | `morning-recall.md` written |
| `dream_end` | Morning recall signals end of session |

## Files

| File | Purpose |
|------|---------|
| `dream_events.py` | WebSocket event server (aiohttp + watchdog) |
| `viewer.html` | Browser-based dream viewer UI |
