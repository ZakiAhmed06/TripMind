import os
import json
import logging
import joblib
import numpy as np
import pandas as pd
from backend.app.ml.recommendation_model import DestinationRecommendationModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def evaluate_recommendations(model: DestinationRecommendationModel, df: pd.DataFrame, top_k: int = 5):
    test_queries = [
        {"interests": ["Mountains", "Adventure"], "budget": 20000, "duration": 4, "travellers": 2, "target_cat": "Mountains"},
        {"interests": ["Beaches", "Nightlife"], "budget": 30000, "duration": 5, "travellers": 2, "target_cat": "Beaches"},
        {"interests": ["Heritage", "Culture"], "budget": 18000, "duration": 3, "travellers": 2, "target_cat": "Heritage"},
        {"interests": ["Wildlife", "Nature"], "budget": 25000, "duration": 4, "travellers": 2, "target_cat": "Wildlife"},
        {"interests": ["Spiritual"], "budget": 12000, "duration": 3, "travellers": 2, "target_cat": "Spiritual"}
    ]

    precision_list = []
    recall_list = []
    ndcg_list = []

    for query in test_queries:
        recs = model.rank(
            user_interests=query["interests"],
            budget=query["budget"],
            duration_days=query["duration"],
            travellers_count=query["travellers"],
            top_k=top_k
        )
        target_cat = query["target_cat"]
        relevant_count_in_top_k = sum(1 for r in recs if target_cat.lower() in r["category"].lower() or any(i.lower() in r["category"].lower() for i in query["interests"]))
        total_relevant_in_db = len(df[df["category"].str.lower() == target_cat.lower()])
        
        p_at_k = relevant_count_in_top_k / top_k
        precision_list.append(p_at_k)

        r_at_k = relevant_count_in_top_k / max(1, total_relevant_in_db)
        recall_list.append(r_at_k)

        dcg = 0.0
        idcg = 0.0
        for i, r in enumerate(recs):
            rel = 1.0 if (target_cat.lower() in r["category"].lower() or any(it.lower() in r["category"].lower() for it in query["interests"])) else 0.0
            dcg += rel / np.log2(i + 2)
        for i in range(min(top_k, relevant_count_in_top_k)):
            idcg += 1.0 / np.log2(i + 2)
        ndcg_val = (dcg / idcg) if idcg > 0 else 0.0
        ndcg_list.append(ndcg_val)

    metrics = {
        f"Precision@{top_k}": round(float(np.mean(precision_list)), 4),
        f"Recall@{top_k}": round(float(np.mean(recall_list)), 4),
        f"NDCG@{top_k}": round(float(np.mean(ndcg_list)), 4),
        "total_test_queries": len(test_queries)
    }
    return metrics


def train_and_save():
    csv_path = "data/processed/destinations.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cannot find {csv_path}. Run generate_datasets.py first.")

    df = pd.read_csv(csv_path)
    model = DestinationRecommendationModel()
    model.fit(df)

    metrics = evaluate_recommendations(model, df, top_k=5)
    logger.info("Recommendation Model Evaluation Metrics: %s", metrics)

    os.makedirs("backend/trained_models", exist_ok=True)
    model_path = "backend/trained_models/recommendation_model.joblib"
    metrics_path = "backend/trained_models/recommendation_metrics.json"

    joblib.dump(model, model_path)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info("Model saved to %s", model_path)
    return model, metrics


if __name__ == "__main__":
    train_and_save()
