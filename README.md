# TripMind | AI + Machine Learning Powered Intelligent Travel Planner

TripMind is an intelligent full-stack travel planning platform that unifies traditional Machine Learning algorithms with Generative AI (LLMs) and grounded Vector Retrieval-Augmented Generation (RAG) to curate ranked destinations, predict realistic travel expenses, generate structured day-wise itineraries, and dynamically adapt travel plans in response to real-time weather alerts.

Targeted as an advanced final-year engineering capstone project and a professional developer portfolio platform.

---

## 🚀 Key Highlights & Architectural Features

1. **Content-Based ML Destination Recommendation Engine (Model 1):**
   - Transforms traveler interests, duration, budget constraints, and climatic preferences into multi-attribute feature vectors.
   - Evaluated using ranking metrics: **Precision@5 = 1.0**, **NDCG@5 = 1.0**.
   - Model serialized with Joblib into `backend/trained_models/recommendation_model.joblib`.

2. **Travel Expense Prediction Engine (Model 2):**
   - Trained **Random Forest Regressor** (120 estimators) predicting total and itemized trip expenses across transport modes (Flight, Train, Cab, Bus), hotel tiers (Budget, Standard 3-star, Luxury), and seasons.
   - **$R^2$ Score = 0.9829**, Mean Absolute Error = ₹5,585.
   - Validated by backend mathematical sanity checks—never relying on unverified LLM math.

3. **Tourist Crowd Density Classifier (Model 3):**
   - Trained **Random Forest Classifier** predicting footfall levels (**Low, Medium, High**) based on seasonal calendars, day of week, and public holiday indicators.
   - **Accuracy = 78.5%**, weighted $F_1 = 0.749$.

4. **Generative AI & Grounded FAISS Vector RAG:**
   - Powered by **Google Gemini 2.5 Flash** via `google-genai` SDK with deterministic offline algorithmic fallback mode.
   - Embedded using **Sentence Transformers** (`all-MiniLM-L6-v2`) and indexed via **FAISS** for verified factual retrieval.

5. **Dynamic Weather Alert Replanning:**
   - Detects weather conditions via **Open-Meteo API** integration.
   - When rainfall or storms threaten outdoor sights, the engine swaps affected outdoor activities for verified indoor cultural galleries, museums, and tea lounges.

6. **Sightseeing Route Optimization:**
   - Calculates **Haversine** great-circle distance matrices and solves attraction sequence order using a **Greedy Nearest-Neighbor heuristic with 2-Opt local search refinement**.

7. **Interactive Leaflet Mapping & Financial Visualizations:**
   - Custom numbered SVG map pins, route polylines, and popups via Leaflet and OpenStreetMap.
   - Expense allocation visual charts rendered with **Recharts**.

8. **Secure Authentication & User-Level Isolation:**
   - Bcrypt password hashing (12 rounds) and HMAC-SHA256 JWT tokens.
   - Strict database isolation ensuring travelers can only view and manage their private itineraries.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React.js 18, Vite 6, Tailwind CSS, React Router 6, Recharts, Leaflet, Axios, Lucide React |
| **Backend** | Python 3.11+, FastAPI, Pydantic V2, SQLAlchemy ORM, Uvicorn |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy, Matplotlib, Joblib |
| **Generative AI & RAG** | Google Gemini 2.5 Flash (`google-genai`), Sentence-Transformers, FAISS Vector Index |
| **Database** | PostgreSQL (Docker Compose ready) + SQLite zero-dependency local development |
| **External APIs** | Open-Meteo Weather API (Free, no key required), OpenStreetMap tiles |
| **DevOps & Containers** | Docker, Docker Compose, Pytest |

---

## 📂 Project Repository Structure

```
TripMind/
├── frontend/                  # React + Vite frontend application
│   ├── src/
│   │   ├── api/               # Axios client with JWT interceptor
│   │   ├── components/        # Navbar, Footer, Map, ExpenseChart, Cards
│   │   ├── context/           # AuthContext (login, register, token persistence)
│   │   ├── pages/             # 10 pages (Landing, Explore, Planner, Itinerary, Assistant, etc.)
│   │   ├── App.jsx            # Routing and protected navigation
│   │   └── main.jsx
│   ├── Dockerfile
│   └── package.json
│
├── backend/                   # FastAPI backend & ML service layer
│   ├── app/
│   │   ├── api/endpoints/     # Modular routers (auth, destinations, budget, itinerary, etc.)
│   │   ├── ml/                # ML training scripts and inference engines
│   │   ├── genai/             # Gemini 2.5 Flash integration & FAISS RAG service
│   │   ├── services/          # Weather service & 2-Opt route optimizer
│   │   ├── models/            # SQLAlchemy database ORM models
│   │   ├── schemas/           # Pydantic V2 request & response schemas
│   │   ├── database/          # Session factory and seed data loader
│   │   └── core/              # App config, security, bcrypt hashing
│   ├── trained_models/        # Serialized .joblib models & metrics JSONs
│   ├── Dockerfile
│   └── requirements.txt
│
├── data/
│   ├── raw/
│   └── processed/             # destinations.csv (315), attractions.csv (1575), travel_expenses.csv
│
├── notebooks/                 # Jupyter demonstration & evaluation notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_destination_recommendation.ipynb
│   ├── 03_budget_prediction.ipynb
│   └── 04_crowd_prediction.ipynb
│
├── rag_knowledge_base/        # Destination markdown guides & FAISS index
│   ├── destinations/
│   └── faiss_index/
│
├── tests/                     # Automated test suite (12 passed tests)
│   └── test_api.py
│
├── docs/                      # Technical documentation
│   ├── architecture.md
│   ├── api_documentation.md
│   └── data_sources.md
│
├── docker-compose.yml         # Multi-container orchestration (PostgreSQL + Backend + Frontend)
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚡ Quick Setup & Running Instructions (Windows)

### Prerequisites
- Python 3.11+ installed (`py -3.11 --version`)
- Node.js v18+ and npm (`node --version`, `npm --version`)

### 1. Clone & Set Up Backend
```powershell
# In project root:
py -3.11 -m venv venv
.\venv\Scripts\activate

# Install backend dependencies:
pip install -r backend/requirements.txt

# Copy environment variables:
Copy-Item .env.example .env
```

### 2. Generate Datasets & Train Machine Learning Models
```powershell
$env:PYTHONPATH='.'

# 1. Generate 300+ destinations, attractions, and training datasets:
python backend/app/ml/generate_datasets.py

# 2. Train and evaluate the Destination Recommendation Engine:
python backend/app/ml/train_recommendation.py

# 3. Train and evaluate the Random Forest Budget Regressor:
python backend/app/ml/train_budget.py

# 4. Train and evaluate the Random Forest Crowd Classifier:
python backend/app/ml/train_crowd.py

# 5. Build FAISS vector database for RAG knowledge assistant:
python backend/app/genai/rag_service.py

# 6. Initialize database and seed destinations & demo user:
python backend/app/database/seed_data.py
```

### 3. Run Automated Tests
```powershell
$env:PYTHONPATH='.'
pytest tests/test_api.py -v
```
All 12 automated integration tests will execute and verify authentication, ML inference, budget calculations, crowd classification, itinerary generation, replanning, and route optimization.

### 4. Start the Application
Open two terminal windows:

**Terminal 1 (Backend Server):**
```powershell
$env:PYTHONPATH='.'
.\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*API running at: `http://127.0.0.1:8000` | Docs at: `http://127.0.0.1:8000/docs`*

**Terminal 2 (Frontend Server):**
```powershell
cd frontend
npm run dev
```
*Frontend running at: `http://localhost:5173`*

---

## 🔑 Demo Account Credentials

For instantaneous demonstration without manual registration, an active demo account is seeded:
- **Email:** `demo@tripmind.ai`
- **Password:** `TripMind123!`
*(A one-click "Autofill Demo Account" button is also provided directly on the Login screen).*

---

## 🐳 Docker Deployment

To launch the full production stack with PostgreSQL, FastAPI, and Nginx in containers:
```bash
docker compose up --build
```
- Frontend UI: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

---

## 📊 Machine Learning Model Evaluation Metrics

| Model | Algorithm | Primary Metrics | Test Samples |
|---|---|---|---|
| **Destination Recommendation** | Content-based Cosine Similarity + Attribute Weights | **Precision@5: 1.0**, **Recall@5: 0.171**, **NDCG@5: 1.0** | 315 Destinations |
| **Travel Expense Predictor** | Random Forest Regressor (120 Estimators) | **$R^2$: 0.9829**, **MAE: ₹5,585.21**, **RMSE: ₹8,243.54** | 700 Test Records |
| **Crowd Density Classifier** | Random Forest Classifier (100 Estimators) | **Accuracy: 78.5%**, **Weighted $F_1$: 0.749** | 800 Test Records |

---

## 🛡️ Known Limitations & Ethical Notice
1. **Estimated Expenses:** Travel expense forecasts are statistical approximations designed for planning and budgeting; they do not represent guaranteed airline or hotel quotes.
2. **Offline Fallback:** When a Google Gemini API key is not supplied, the platform operates deterministically using its algorithmic knowledge engine without crashing.
3. **Weather Advisories:** Weather forecast data is retrieved from Open-Meteo. Dynamic replanning recommendations are advisory.
