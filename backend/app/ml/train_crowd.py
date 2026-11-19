"""
MODEL 3: Tourist Crowd Prediction Engine Training & Evaluation
Uses Random Forest Classifier trained on temporal and seasonal visitor indicators,
evaluated with Accuracy, Precision, Recall, F1-score and Confusion Matrix, saved via Joblib.
"""
import os
import json
import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def train_crowd_model():
    csv_path = "data/processed/historical_visitors.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cannot find {csv_path}. Run generate_datasets.py first.")

    df = pd.read_csv(csv_path)
    logger.info("Loaded %d visitor footfall records.", len(df))

    cat_features = ["season"]
    num_features = ["month", "day_of_week", "is_weekend", "is_public_holiday"]

    X = df[cat_features + num_features]
    y = df["crowd_level"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features)
        ]
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logger.info("Training Random Forest Classifier on %d samples, testing on %d samples...", len(X_train), len(X_test))

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)
    conf_mat = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        "model_name": "RandomForestClassifier",
        "n_estimators": 100,
        "Accuracy": round(float(acc), 4),
        "Precision": round(float(prec), 4),
        "Recall": round(float(rec), 4),
        "F1_Score": round(float(f1), 4),
        "Confusion_Matrix": conf_mat,
        "classes": pipeline.named_steps["classifier"].classes_.tolist(),
        "training_samples": len(X_train),
        "test_samples": len(X_test)
    }
    logger.info("Crowd Model Evaluation Metrics: %s", metrics)

    os.makedirs("backend/trained_models", exist_ok=True)
    model_path = "backend/trained_models/crowd_model.joblib"
    metrics_path = "backend/trained_models/crowd_metrics.json"

    joblib.dump(pipeline, model_path)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info("Saved crowd model to %s", model_path)
    return pipeline, metrics


if __name__ == "__main__":
    train_crowd_model()
