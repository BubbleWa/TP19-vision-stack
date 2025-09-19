# APP_RISK/routes/risk_detect.py

from fastapi import APIRouter
from pydantic import BaseModel
from app_risk.services.risk_service import predict_risks

router = APIRouter()

class RiskRequest(BaseModel):
    text: str
    state: str | None = None

@router.post("/risk_detect")
def detect_risk(req: RiskRequest):
    result = predict_risks(req.text, req.state)
    return {"input": req.text, "analysis": result}
