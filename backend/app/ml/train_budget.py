"""
MODEL 2: Travel Expense Prediction Engine Training & Evaluation
Uses Random Forest Regressor trained on travel configurations with One-Hot encoding,
evaluated with MAE, RMSE, and R2 score, saved to Joblib.
"""
import os
import json
import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def train_budget_model():
    csv_path = "data/processed/travel_expenses.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cannot find {csv_path}. Run generate_datasets.py first.")

    df = pd.read_csv(csv_path)
    logger.info("Loaded %d expense records for training.", len(df))

    # Feature columns
    cat_features = [
        "destination_category",
        "transport_mode",
        "hotel_category",
        "season",
        "food_preference"
    ]
    num_features = [
        "duration_days",
        "travellers_count",
        "sightseeing_count"
    ]

    X = df[cat_features + num_features]
    y = df["total_trip_expense"]

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features)
        ]
    )

    # Random Forest Regressor pipeline
    model_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=120, max_depth=15, random_state=42, n_jobs=-1))
    ])

    # Train / Test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logger.info("Training Random Forest Regressor on %d samples, testing on %d samples...", len(X_train), len(X_test))

    model_pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = model_pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "model_name": "RandomForestRegressor",
        "n_estimators": 120,
        "max_depth": 15,
        "MAE": round(float(mae), 2),
        "RMSE": round(float(rmse), 2),
        "R2_Score": round(float(r2), 4),
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "dataset_type": "Synthetic-grounded travel expense configurations"
    }
    logger.info("Budget Model Evaluation Metrics: %s", metrics)

    # Save model and metrics
    os.makedirs("backend/trained_models", exist_ok=True)
    model_path = "backend/trained_models/budget_model.joblib"
    metrics_path = "backend/trained_models/budget_metrics.json"

    joblib.dump(model_pipeline, model_path)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info("Saved budget model to %s", model_path)
    return model_pipeline, metrics


if __name__ == "__main__":
    train_budget_model()
