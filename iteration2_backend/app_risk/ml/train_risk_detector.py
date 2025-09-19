# APP_RISK/ml/train_risk_detector.py

import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# === Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "datasets", "risk_training.csv")
ARTIFACT_DIR = os.path.join(BASE_DIR, "ml", "artifacts")
os.makedirs(ARTIFACT_DIR, exist_ok=True)

print("Loading dataset from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

# === Normalize column names ===
df.columns = df.columns.str.strip().str.lower()

# Expecting: "message", "risk_category"
if "message" not in df.columns or "risk_category" not in df.columns:
    raise ValueError(f"Expected columns ['message','risk_category'], got {df.columns.tolist()}")

# === Clean data ===
# Drop rows with missing messages
df = df.dropna(subset=["message"])
df["message"] = df["message"].astype(str)

# Handle NaN risk_category
df["risk_category"] = df["risk_category"].fillna("").astype(str)

# Convert "age;ethnicity" -> ["age","ethnicity"]
df["risk_category"] = df["risk_category"].apply(lambda x: x.split(";") if x else [])

# === Encode labels ===
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df["risk_category"])
X = df["message"]

print("Categories detected:", mlb.classes_)

# === Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# === Build Pipeline ===
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("clf", OneVsRestClassifier(LogisticRegression(max_iter=500, class_weight="balanced"), n_jobs=-1))
])

# === Train ===
print("Training model...")
pipeline.fit(X_train, y_train)

# === Evaluate ===
y_pred = pipeline.predict(X_test)
print("\nEvaluation Report:")
print(classification_report(y_test, y_pred, target_names=mlb.classes_))

# === Save Artifacts ===
joblib.dump(pipeline, os.path.join(ARTIFACT_DIR, "risk_model.joblib"))
joblib.dump(mlb, os.path.join(ARTIFACT_DIR, "risk_mlb.joblib"))
print(f"Model and label binarizer is saved to {ARTIFACT_DIR}")
