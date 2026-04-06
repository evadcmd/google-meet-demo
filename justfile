calendar:
    uv run python -m google_meet_demo.quickstart.calendar

meeting:
    uv run python -m google_meet_demo.quickstart.meeting

dev:
    uv run uvicorn google_meet_demo.main:api --port 8000 --reload --app-dir src
