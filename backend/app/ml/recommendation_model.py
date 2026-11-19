import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer


class DestinationRecommendationModel:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.tfidf = TfidfVectorizer(stop_words="english")
        self.df_destinations = None
        self.feature_matrix = None
        self.feature_columns = [
            "adventure_score",
            "nature_score",
            "nightlife_score",
            "heritage_score",
            "photography_score",
            "average_temperature",
            "popularity_score"
        ]

    def fit(self, df: pd.DataFrame):
        self.df_destinations = df.copy().reset_index(drop=True)

        # 1. Numerical feature scaling
        num_features = self.scaler.fit_transform(self.df_destinations[self.feature_columns])

        # 2. Text feature vectorization on category & description
        combined_text = (
            self.df_destinations["category"] + " " +
            self.df_destinations["state"] + " " +
            self.df_destinations["description"].fillna("")
        )
        text_features = self.tfidf.fit_transform(combined_text).toarray()

        # 3. Concatenate normalized numeric & TF-IDF vectors
        self.feature_matrix = np.hstack([num_features, text_features])
        return self

    def rank(
        self,
        user_interests: list,
        budget: float,
        duration_days: int = 4,
        travellers_count: int = 2,
        state_filter: str = None,
        top_k: int = 10
    ):
        if self.df_destinations is None or self.feature_matrix is None:
            raise ValueError("Model has not been trained or loaded yet.")

        daily_budget_per_person = budget / max(1, (duration_days * travellers_count))
        scores = []
        user_interests_lower = [i.lower() for i in user_interests]

        interest_attr_map = {
            "adventure": "adventure_score",
            "nature": "nature_score",
            "nightlife": "nightlife_score",
            "heritage": "heritage_score",
            "photography": "photography_score",
            "culture": "heritage_score",
            "mountains": "nature_score",
            "beaches": "nature_score",
            "wildlife": "nature_score",
            "spiritual": "heritage_score"
        }

        for idx, row in self.df_destinations.iterrows():
            if state_filter and row["state"].lower() != state_filter.lower():
                continue

            match_components = []
            for interest in user_interests_lower:
                attr_col = interest_attr_map.get(interest)
                if attr_col and attr_col in row:
                    score_val = row[attr_col] / 10.0
                    match_components.append(score_val)
                elif interest in row["category"].lower():
                    match_components.append(1.0)
                elif interest in row["description"].lower():
                    match_components.append(0.8)

            interest_match_score = np.mean(match_components) if match_components else 0.5
            category_match = 1.0 if any(i in row["category"].lower() for i in user_interests_lower) else 0.65

            dest_daily = row["average_budget"]
            budget_ratio = daily_budget_per_person / max(100.0, dest_daily)
            if 0.7 <= budget_ratio <= 2.5:
                budget_score = 1.0
            elif budget_ratio < 0.7:
                budget_score = max(0.2, budget_ratio / 0.7)
            else:
                budget_score = max(0.7, 1.0 - (budget_ratio - 2.5) * 0.05)

            popularity_weight = row["popularity_score"] / 10.0

            final_similarity = (
                0.45 * interest_match_score +
                0.25 * category_match +
                0.20 * budget_score +
                0.10 * popularity_weight
            )
            final_similarity = float(np.clip(final_similarity, 0.05, 0.99))

            estimated_trip_cost = round(dest_daily * duration_days * travellers_count * 1.35, 2)

            explanation = (
                f"Matches your interest in {', '.join(user_interests[:3])} with a strong "
                f"{row['category']} profile ({row['state']}). Fits within the estimated per-person daily budget."
            )

            scores.append({
                "destination_id": int(row["destination_id"]),
                "name": row["destination_name"],
                "state": row["state"],
                "category": row["category"],
                "similarity_score": round(final_similarity, 4),
                "match_percentage": round(final_similarity * 100, 1),
                "estimated_budget": estimated_trip_cost,
                "recommended_season": row["best_season"],
                "average_temperature": float(row["average_temperature"]),
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "image_url": row["image_url"],
                "description": row["description"],
                "match_explanation": explanation
            })

        ranked = sorted(scores, key=lambda x: x["similarity_score"], reverse=True)
        return ranked[:top_k]
