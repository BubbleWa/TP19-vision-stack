import re
import pandas as pd
from app_risk.config_risk import DATASETS_DIR
import joblib

# Load datasets
risky_phrases = pd.read_csv(f"{DATASETS_DIR}/risky_phrases.csv")
educational_tips = pd.read_csv(f"{DATASETS_DIR}/educational_tips.csv")
law_references = pd.read_csv(f"{DATASETS_DIR}/law_references.csv")
reporting_guide = pd.read_csv(f"{DATASETS_DIR}/reporting_guide.csv")

# Load ML model + multilabel binarizer
model = joblib.load(f"{DATASETS_DIR}/../ml/artifacts/risk_model.joblib")
mlb = joblib.load(f"{DATASETS_DIR}/../ml/artifacts/risk_mlb.joblib")

def predict_risks(text: str, state: str):
    text_lower = text.lower()
    rule_labels = set()
    highlights = []

    # --- Rule-based detection ---
    for _, row in risky_phrases.iterrows():
        category = row["category_key"]
        for kw in str(row["keywords"]).split(";"):
            kw = kw.strip()
            if not kw:
                continue
            pattern = re.escape(kw)
            if re.search(pattern, text_lower, re.IGNORECASE):
                rule_labels.add(category)
                highlights.append({"phrase": kw, "category": category})

    # --- ML-based detection ---
    ml_pred = model.predict([text_lower])
    ml_labels = set(mlb.inverse_transform(ml_pred)[0]) if len(ml_pred) > 0 else set()

    # --- Combine ML + Rules ---
    final_labels = set(ml_labels).union(rule_labels)

    # If any rule labels exist, drop ML-only "noise"
    if rule_labels:
        final_labels = rule_labels.union(ml_labels.intersection(rule_labels))

    # Remove "not_cyberbullying" if any real category exists
    if "not_cyberbullying" in final_labels and len(final_labels) > 1:
        final_labels.remove("not_cyberbullying")

    # --- Educational Tips ---
    tips = educational_tips[educational_tips["category_key"].isin(final_labels)].to_dict(orient="records")

    # --- Laws ---
    laws = law_references[law_references["category_key"].isin(final_labels)].to_dict(orient="records")

    # Filter state-specific laws or fallback to ALL/Federal
    state_laws = [law for law in laws if law["state"] in [state, "ALL", "Federal"]]

    # --- Reporting Guides ---
    reporting = reporting_guide[reporting_guide["category_key"].isin(final_labels)].to_dict(orient="records")
    state_reporting = [r for r in reporting if r["state"] in [state, "ALL"]]

    # --- Risk Score ---
    score = "Low"
    if any(c in final_labels for c in ["abuse", "age", "gender", "ethnicity", "religion", "scam"]):
        score = "High"
    if "threats" in final_labels or "sexual" in final_labels:
        score = "High"
    if "selfharm" in final_labels:
        score = "Critical"
    if final_labels == {"not_cyberbullying"}:
        score = "Low"

    return {
        "input": text,
        "analysis": {
            "labels": list(final_labels),
            "highlights": highlights,
            "laws": state_laws,
            "tips": tips,
            "reporting": state_reporting,
            "score": score
        }
    }
