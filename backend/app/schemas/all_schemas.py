from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# ==================== User & Auth Schemas ====================
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class UserPreferenceUpdate(BaseModel):
    preferred_categories: Optional[str] = "Mountains,Adventure,Heritage"
    budget_range: Optional[str] = "10000-30000"
    default_travellers: Optional[int] = 2
    default_origin: Optional[str] = "Delhi"
    travel_style: Optional[str] = "Balanced"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_admin: bool
    preferences: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# ==================== Destination & Attraction Schemas ====================
class AttractionResponse(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str] = None
    estimated_duration_hours: float
    entry_fee: float
    is_outdoor: bool
    latitude: float
    longitude: float
    popularity_rank: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class DestinationResponse(BaseModel):
    id: int
    name: str
    state: str
    country: str = "India"
    category: str
    average_budget: float
    average_temperature: float
    adventure_score: float
    nature_score: float
    nightlife_score: float
    heritage_score: float
    photography_score: float
    family_friendly: bool
    best_season: str
    popularity_score: float
    latitude: float
    longitude: float
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class DestinationDetailResponse(DestinationResponse):
    attractions: List[AttractionResponse] = []


# ==================== ML Recommendation Schemas ====================
class RecommendationRequest(BaseModel):
    origin: Optional[str] = "Delhi"
    budget: float = Field(gt=0, description="Total budget in INR")
    duration_days: int = Field(ge=1, le=30, default=4)
    travellers_count: int = Field(ge=1, le=20, default=2)
    interests: List[str] = Field(default_factory=lambda: ["Mountains", "Nature", "Adventure"])
    transport_mode: Optional[str] = "Train"
    accommodation_category: Optional[str] = "Standard (3-star)"
    season: Optional[str] = "Winter"
    state: Optional[str] = None


class DestinationRecommendation(BaseModel):
    destination_id: int
    name: str
    state: str
    category: str
    similarity_score: float  # Content-based cosine & multi-attribute score (0 to 1)
    match_percentage: float  # Display percentage (e.g. 92%)
    estimated_budget: float
    recommended_season: str
    average_temperature: float
    latitude: float
    longitude: float
    image_url: Optional[str] = None
    description: Optional[str] = None
    match_explanation: str
    top_attractions: List[str] = []


class RecommendationResponse(BaseModel):
    recommendations: List[DestinationRecommendation]
    total_found: int


# ==================== ML Budget Schemas ====================
class BudgetPredictionRequest(BaseModel):
    destination_name: str
    duration_days: int = Field(ge=1, le=30, default=4)
    travellers_count: int = Field(ge=1, le=20, default=2)
    transport_mode: str = "Train"  # Flight, Train, Cab, Bus
    hotel_category: str = "Standard (3-star)"  # Budget, Standard (3-star), Luxury (4/5-star)
    season: str = "Peak"  # Peak, Moderate, Off-peak
    food_preference: str = "Both"  # Veg, Non-Veg, Both
    sightseeing_count: int = 6
    destination_category: Optional[str] = "Mountains"


class ExpenseBreakdown(BaseModel):
    transportation: float
    accommodation: float
    food: float
    sightseeing: float
    miscellaneous: float
    total: float
    currency: str = "INR"


class BudgetPredictionResponse(BaseModel):
    destination: str
    duration_days: int
    travellers_count: int
    predicted_total_expense: float
    per_person_expense: float
    breakdown: ExpenseBreakdown
    model_used: str = "RandomForestRegressor"
    is_model_trained: bool = True
    confidence_note: str = "Estimated via trained Random Forest model with backend sanity validation."


# ==================== ML Crowd Schemas ====================
class CrowdPredictionRequest(BaseModel):
    destination_name: str
    month: int = Field(ge=1, le=12, default=10)
    day_of_week: int = Field(ge=0, le=6, default=5)  # 0=Monday, 6=Sunday
    is_weekend: bool = True
    is_public_holiday: bool = False
    season: Optional[str] = "Winter"


class CrowdPredictionResponse(BaseModel):
    destination: str
    month: int
    crowd_level: str  # Low, Medium, High
    crowd_score: float  # 0 to 1
    best_time_to_visit: str
    recommendation: str
    model_used: str = "RandomForestClassifier"


# ==================== Itinerary & Activity Schemas ====================
class ActivityItem(BaseModel):
    id: Optional[str] = None
    time_slot: str  # Morning, Afternoon, Evening, Night
    attraction_name: str
    description: str
    duration_hours: float = 2.0
    estimated_cost: float = 0.0
    is_outdoor: bool = True
    sequence_order: int = 1
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category: Optional[str] = "Sightseeing"


class DayItinerary(BaseModel):
    day_number: int
    date: Optional[str] = None
    title: str
    activities: List[ActivityItem]
    food_recommendations: List[str] = []
    transport_tips: str = "Local cabs and auto-rickshaws recommended."
    estimated_daily_expense: float = 0.0


class ItineraryGenerateRequest(BaseModel):
    destination_name: str
    origin: str = "Delhi"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_days: int = Field(ge=1, le=14, default=4)
    travellers_count: int = Field(ge=1, le=20, default=2)
    budget: float = Field(gt=0, default=25000.0)
    travel_interests: List[str] = Field(default_factory=lambda: ["Sightseeing", "Nature", "Culture"])
    transport_mode: str = "Train"
    accommodation_category: str = "Standard (3-star)"
    food_preference: str = "Both"


class ItineraryResponse(BaseModel):
    id: Optional[int] = None
    trip_id: Optional[int] = None
    destination_name: str
    origin: str
    duration_days: int
    travellers_count: int
    total_budget: float
    estimated_total_expense: float
    expense_breakdown: ExpenseBreakdown
    days: List[DayItinerary]
    travel_tips: List[str] = []
    source: str = "Gemini AI + ML Optimizer"


class ItineraryUpdateRequest(BaseModel):
    days: List[DayItinerary]
    estimated_total_expense: Optional[float] = None


class ReplanningRequest(BaseModel):
    trip_id: Optional[int] = None
    destination_name: str
    current_days: List[DayItinerary]
    affected_day: int
    reason: str = "Heavy Rainfall Forecast"
    weather_condition: Optional[str] = "Heavy Rain"
    total_budget: float = 25000.0


# ==================== Conversational AI Schemas ====================
class ChatMessageRequest(BaseModel):
    session_id: Optional[int] = None
    trip_id: Optional[int] = None
    message: str
    current_destination: Optional[str] = None
    current_budget: Optional[float] = None
    itinerary_context: Optional[Dict[str, Any]] = None


class ChatMessageResponse(BaseModel):
    session_id: int
    reply: str
    suggested_actions: List[str] = []
    modified_itinerary: Optional[Dict[str, Any]] = None
    retrieved_sources: List[str] = []


# ==================== Trip Management Schemas ====================
class TripCreate(BaseModel):
    destination_id: Optional[int] = None
    destination_name: str
    title: str
    origin: str = "Delhi"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_days: int = 3
    travellers_count: int = 2
    transport_mode: str = "Train"
    accommodation_type: str = "Standard (3-star)"
    food_preference: str = "Both"
    total_budget: float = 20000.0
    status: str = "Upcoming"
    days_data: Optional[List[DayItinerary]] = None
    expense_breakdown: Optional[ExpenseBreakdown] = None


class TripResponse(BaseModel):
    id: int
    user_id: int
    destination_id: Optional[int] = None
    destination_name: Optional[str] = None
    destination_state: Optional[str] = None
    destination_image: Optional[str] = None
    title: str
    origin: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_days: int
    travellers_count: int
    transport_mode: str
    accommodation_type: str
    food_preference: str
    total_budget: float
    status: str
    days: List[DayItinerary] = []
    expenses: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True


# ==================== Feedback Schemas ====================
class FeedbackCreate(BaseModel):
    destination_id: Optional[int] = None
    trip_id: Optional[int] = None
    rating: int = Field(ge=1, le=5, default=5)
    liked: bool = True
    review: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    destination_id: Optional[int] = None
    rating: int
    liked: bool
    review: Optional[str] = None

    class Config:
        from_attributes = True
