# app_risk/main_risk.py

from fastapi import FastAPI
from app_risk.routes.risk_detect import router as risk_router
from app_risk.config_risk import APP_NAME, APP_VERSION

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# Health check
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Register routes
app.include_router(risk_router)
