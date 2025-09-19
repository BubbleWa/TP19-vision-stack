# APP_RISK/config_risk.py

import os

APP_NAME = "Cybermate Risk Detector"
APP_VERSION = "2.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "ml", "artifacts")

RISK_MODEL_PATH = os.path.join(ARTIFACTS_DIR, "risk_model.joblib")
RISK_MLB_PATH = os.path.join(ARTIFACTS_DIR, "risk_mlb.joblib")
