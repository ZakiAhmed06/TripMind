# TripMind: Data Sources, Methodology & Limitations

## Overview
TripMind integrates empirical tourism metadata, geographical coordinates, weather APIs, and realistic synthetic behavioral data to power its Machine Learning recommendation engines, expense predictors, crowd models, and Generative AI services.

---

## 1. Destination & Attraction Catalog
- **File:** `data/processed/destinations.csv` & `data/processed/attractions.csv`
- **Total Destinations:** 315 curated Indian destinations across 24 states and union territories.
- **Total Attractions:** 1,575 catalogued tourist attractions with outdoor flags, entry fees, coordinates, and duration estimates.
- **Attributes Collected:**
  - `destination_id`: Unique integer identifier.
  - `destination_name`: Official tourist destination name.
  - `state` / `country`: Geographic state and country jurisdiction.
  - `category`: Primary travel category (Mountains, Beaches, Heritage, Adventure, Wildlife, Spiritual, Nature, Culture, Nightlife, Food, Photography).
  - `average_budget`: Estimated average daily budget per person (INR).
  - `average_temperature`: Mean annual/seasonal temperature (°C).
  - `adventure_score`, `nature_score`, `nightlife_score`, `heritage_score`, `photography_score`: Calibrated attribute ratings (1.0 - 10.0 scale).
  - `family_friendly`: Boolean suitability indicator.
  - `best_season`: Documented optimal visiting window.
  - `popularity_score`: Regional popularity index.
  - `latitude`, `longitude`: Validated WGS84 decimal coordinates.
  - `description` & `image_url`: Unsplash tourism imagery and descriptive summaries.
- **Primary References:**
  - Incredible India (Ministry of Tourism, Govt. of India): https://www.incredibleindia.org/
  - OpenStreetMap (OSM) Nominatim & Overpass API geocoding: https://www.openstreetmap.org/
  - India Tourism Statistics (data.gov.in)
- **Licensing:** Open Data Commons / Creative Commons Attribution (CC-BY).

---

## 2. Travel Expense Dataset
- **File:** `data/processed/travel_expenses.csv`
- **Total Records:** 3,500 trip configurations.
- **Target Variable:** `total_trip_expense` (continuous float in INR).
- **Component Breakdown:** Transportation, Accommodation, Food, Sightseeing, and Miscellaneous expenses.
- **Methodology & Documentation:**
  - In accordance with project requirements, travel pricing is constructed via realistic parametric simulation reflecting benchmark Indian market rates (IRCTC train fare bands, domestic airfare averages, standard hotel tariff tiers, and state tourism entry charges).
  - Clearly labelled as synthetic-grounded empirical training data.
- **Machine Learning Architecture:** Random Forest Regressor with Multi-feature Pipeline (One-Hot categorical encoding, standard scaling, and R² / RMSE evaluation).

---

## 3. Crowd & Footfall Dynamics Dataset
- **File:** `data/processed/historical_visitors.csv`
- **Total Records:** 4,000 seasonal observations across top tourist corridors.
- **Features:** Destination name, calendar month, day of week, weekend indicator, public holiday indicator, season category.
- **Target Variable:** `crowd_level` (Categorical: Low, Medium, High) and continuous `crowd_score` (0.0 to 1.0).
- **Machine Learning Architecture:** Random Forest Classifier evaluated using Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.

---

## 4. External Real-Time Integrations
- **Weather Services:**
  - Provider: **Open-Meteo API** (Free, Open Access, No API key required).
  - Endpoint: `https://api.open-meteo.com/v1/forecast`
  - Integration: Daily temperature forecasts, precipitation probability, and weather condition codes with SQLite/Postgres caching layer.
- **Generative AI & LLM:**
  - Model: **Google Gemini 2.5 Flash** via `google-genai` SDK.
  - Purpose: Structured day-wise itinerary generation, conversational assistance, and dynamic weather replanning.
  - Offline Fallback: Full deterministic mock generator available when API key is unconfigured.
- **Vector Search & RAG Knowledge Base:**
  - Embeddings: Sentence-Transformers (`all-MiniLM-L6-v2`) / TF-IDF Vector Space fallback.
  - Vector Store: FAISS (Facebook AI Similarity Search) index for grounded document retrieval.

---

## 5. Limitations & Ethical Notice
1. **Financial Estimates:** All predicted expenses are estimates for itinerary planning and do not represent guaranteed real-time booking quotes.
2. **Crowd Predictions:** Crowd levels are algorithmic estimates based on seasonal patterns and calendar flags, not live satellite or gate counters.
3. **Weather Alerts:** Weather replanning triggers rely on Open-Meteo forecast probabilities and are advisory in nature.
