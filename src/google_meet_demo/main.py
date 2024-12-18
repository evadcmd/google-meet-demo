from fastapi import FastAPI

from google_meet_demo.router import auth, liveness_probe

api = FastAPI()

api.include_router(auth.router)
api.include_router(liveness_probe.router)