import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "TripMind"


def test_auth_and_user_flow():
    email = "testuser_unique@tripmind.ai"
    # Register
    reg_resp = client.post("/api/auth/register", json={
        "email": email,
        "full_name": "Test Explorer",
        "password": "Password123!"
    })
    # If already exists or 201
    assert reg_resp.status_code in [201, 400]

    # Login
    login_resp = client.post("/api/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # Protected me endpoint
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == email


def test_get_destinations():
    response = client.get("/api/destinations?limit=10")
    assert response.status_code == 200
    destinations = response.json()
    assert len(destinations) > 0
    assert "name" in destinations[0]
    assert "category" in destinations[0]


def test_destination_search():
    response = client.get("/api/destinations/search?q=Manali")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("manali" in d["name"].lower() for d in data)


def test_destination_details():
    # First get a valid destination id
    list_resp = client.get("/api/destinations?limit=1")
    dest_id = list_resp.json()[0]["id"]

    detail_resp = client.get(f"/api/destinations/{dest_id}")
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert detail["id"] == dest_id
    assert "attractions" in detail
    assert isinstance(detail["attractions"], list)


def test_ml_recommendations():
    payload = {
        "origin": "Delhi",
        "budget": 25000.0,
        "duration_days": 4,
        "travellers_count": 2,
        "interests": ["Mountains", "Adventure"]
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    top = data["recommendations"][0]
    assert "similarity_score" in top
    assert top["similarity_score"] > 0
    assert "match_percentage" in top


def test_ml_budget_prediction():
    payload = {
        "destination_name": "Manali",
        "duration_days": 4,
        "travellers_count": 2,
        "transport_mode": "Train",
        "hotel_category": "Standard (3-star)",
        "season": "Peak",
        "food_preference": "Both",
        "sightseeing_count": 6
    }
    response = client.post("/api/budget/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_total_expense" in data
    assert data["predicted_total_expense"] > 0
    assert "breakdown" in data
    b = data["breakdown"]
    assert b["transportation"] > 0
    assert b["accommodation"] > 0
    assert b["food"] > 0


def test_ml_crowd_prediction():
    payload = {
        "destination_name": "Manali",
        "month": 12,
        "day_of_week": 6,
        "is_weekend": True,
        "is_public_holiday": True,
        "season": "Winter"
    }
    response = client.post("/api/crowd/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["crowd_level"] in ["Low", "Medium", "High"]
    assert "crowd_score" in data
    assert "recommendation" in data


def test_itinerary_generation():
    payload = {
        "destination_name": "Manali",
        "origin": "Delhi",
        "duration_days": 3,
        "travellers_count": 2,
        "budget": 20000.0,
        "travel_interests": ["Mountains", "Adventure"]
    }
    response = client.post("/api/itinerary/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["destination_name"] == "Manali"
    assert len(data["days"]) == 3
    assert len(data["days"][0]["activities"]) > 0


def test_dynamic_replanning():
    # First generate itinerary
    gen_payload = {
        "destination_name": "Manali",
        "origin": "Delhi",
        "duration_days": 3,
        "travellers_count": 2,
        "budget": 20000.0,
        "travel_interests": ["Mountains", "Adventure"]
    }
    gen_resp = client.post("/api/itinerary/generate", json=gen_payload)
    itin_days = gen_resp.json()["days"]

    # Now request replanning for Day 2 due to heavy rain
    replan_payload = {
        "destination_name": "Manali",
        "current_days": itin_days,
        "affected_day": 2,
        "reason": "Severe Rainfall and Landslide Warning",
        "total_budget": 20000.0
    }
    replan_resp = client.post("/api/itinerary/replan", json=replan_payload)
    assert replan_resp.status_code == 200
    new_days = replan_resp.json()
    assert len(new_days) == 3
    # Check that day 2 was updated with indoor activities
    day2_acts = new_days[1]["activities"]
    assert any(act["is_outdoor"] is False for act in day2_acts)


def test_route_optimization():
    payload = {
        "attractions": [
            {"name": "Solang Valley", "latitude": 32.3160, "longitude": 77.1578},
            {"name": "Hadimba Temple", "latitude": 32.2483, "longitude": 77.1804},
            {"name": "Old Manali Cafe", "latitude": 32.2562, "longitude": 77.1812},
            {"name": "Jogini Waterfall", "latitude": 32.2704, "longitude": 77.1950}
        ]
    }
    response = client.post("/api/routes/optimize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ordered_attractions" in data
    assert "total_distance_km" in data
    assert len(data["ordered_attractions"]) == 4


def test_user_trip_isolation():
    # Create user A
    client.post("/api/auth/register", json={
        "email": "userA@tripmind.ai",
        "full_name": "User Alpha",
        "password": "Password123!"
    })
    tokenA = client.post("/api/auth/login", json={"email": "userA@tripmind.ai", "password": "Password123!"}).json()["access_token"]

    # User A creates a trip
    trip_resp = client.post(
        "/api/trips",
        json={
            "destination_name": "Goa",
            "title": "Alpha Private Vacation",
            "total_days": 4,
            "total_budget": 30000.0
        },
        headers={"Authorization": f"Bearer {tokenA}"}
    )
    assert trip_resp.status_code == 201
    trip_id = trip_resp.json()["id"]

    # Create user B
    client.post("/api/auth/register", json={
        "email": "userB@tripmind.ai",
        "full_name": "User Beta",
        "password": "Password123!"
    })
    tokenB = client.post("/api/auth/login", json={"email": "userB@tripmind.ai", "password": "Password123!"}).json()["access_token"]

    # User B attempts to access User A's private trip
    forbidden_resp = client.get(f"/api/trips/{trip_id}", headers={"Authorization": f"Bearer {tokenB}"})
    assert forbidden_resp.status_code == 404  # Isolated / Not found for user B
