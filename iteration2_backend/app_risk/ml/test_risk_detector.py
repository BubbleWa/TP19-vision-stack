# APP_RISK/ml/test_risk_detector.py
import os
import joblib

# === Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT_DIR = os.path.join(BASE_DIR, "ml", "artifacts")

# Load trained model + label binarizer
pipeline = joblib.load(os.path.join(ARTIFACT_DIR, "risk_model.joblib"))
mlb = joblib.load(os.path.join(ARTIFACT_DIR, "risk_mlb.joblib"))

# === Test sentences for each category ===
test_samples = {
    "abuse": "You are such a stupid idiot, nobody likes you",
    "age": "That old grandma doesnt know how to use the internet",
    "ethnicity": "Go back to your country, you foreigner",
    "gender": "She is such a dumb girl, what a bitch",
    "misinformation": "Covid is a hoax, vaccines kill people",
    "not_cyberbullying": "I love pizza, whats your favourite topping?",
    "religion": "Muslims are terrorists and Christians are brainwashed",
    "scam": "Click here to win a lottery prize, free gift just for you",
    "selfharm": "I feel worthless and want to end my life",
    "sexual": "Send me your nudes, you sexy slut",
    "threats": "I will stab you tonight with a knife"
}

# === Run predictions ===
for category, text in test_samples.items():
    pred = pipeline.predict([text])
    labels = mlb.inverse_transform(pred)
    print(f"\nText ({category} example): {text}")
    print(f"Predicted Risks: {labels[0] if labels[0] else 'None'}")
