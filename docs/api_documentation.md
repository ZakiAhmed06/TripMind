# TripMind REST API Reference

Base URL: `http://localhost:8000/api`  
Interactive Swagger Docs: `http://localhost:8000/docs`

---

## 1. Authentication Endpoints

### `POST /api/auth/register`
Creates a new traveler account.
- **Request Body:**
  ```json
  {
    "full_name": "Aarav Sharma",
    "email": "aarav@example.com",
    "password": "Password123!"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "aarav@example.com",
      "full_name": "Aarav Sharma",
      "is_admin": false
    }
  }
  ```

### `POST /api/auth/login`
Authenticates a user and issues an access token.
- **Request Body:**
  ```json
  {
    "email": "aarav@example.com",
    "password": "Password123!"
  }
  ```

### `GET /api/auth/me`
Fetches current user profile and saved travel preferences.
- **Header:** `Authorization: Bearer <token>`

---

## 2. Destination Endpoints

### `GET /api/destinations`
Lists destinations with optional filtering and pagination.
- **Query Parameters:**
  - `query` (string, optional): Keyword search
  - `category` (string, optional): Filter by category
  - `state` (string, optional): Filter by state
  - `max_budget` (float, optional): Maximum daily budget
  - `limit` (int, default: 50)
  - `offset` (int, default: 0)

### `GET /api/destinations/{id}`
Returns complete destination details including catalogued tourist attractions.

---

## 3. Machine Learning Endpoints

### `POST /api/recommendations`
Ranks destinations using content-based cosine similarity and multi-attribute preference weights.
- **Request Body:**
  ```json
  {
    "origin": "Delhi",
    "budget": 25000,
    "duration_days": 4,
    "travellers_count": 2,
    "interests": ["Mountains", "Adventure"]
  }
  ```

### `POST /api/budget/predict`
Predicts trip expenses using the trained Random Forest Regressor.
- **Request Body:**
  ```json
  {
    "destination_name": "Manali",
    "duration_days": 4,
    "travellers_count": 2,
    "transport_mode": "Train",
    "hotel_category": "Standard (3-star)",
    "season": "Peak",
    "food_preference": "Both",
    "sightseeing_count": 6
  }
  ```

### `POST /api/crowd/predict`
Classifies expected footfall density (Low, Medium, High).
- **Request Body:**
  ```json
  {
    "destination_name": "Manali",
    "month": 12,
    "day_of_week": 6,
    "is_weekend": true,
    "is_public_holiday": true,
    "season": "Winter"
  }
  ```

---

## 4. Itinerary & Generative AI Endpoints

### `POST /api/itinerary/generate`
Generates a structured day-wise itinerary combining Gemini 2.5 Flash, RAG context, and ML budget limits.
- **Request Body:**
  ```json
  {
    "destination_name": "Manali",
    "origin": "Delhi",
    "duration_days": 3,
    "travellers_count": 2,
    "budget": 20000,
    "travel_interests": ["Mountains", "Nature"]
  }
  ```

### `POST /api/itinerary/replan`
Dynamically modifies an existing itinerary to replace outdoor activities with weather-safe indoor sights.

### `POST /api/assistant/chat`
Context-aware conversational AI assistant query with RAG citation metadata.
- **Header:** `Authorization: Bearer <token>`

---

## 5. Route & Weather Endpoints

### `POST /api/routes/optimize`
Orders attraction coordinates using Haversine distance and 2-opt TSP improvement.

### `GET /api/weather/{destination_id}`
Returns cached or live 7-day temperature and precipitation forecast from Open-Meteo.
