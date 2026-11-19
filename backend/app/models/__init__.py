import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from backend.app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    preferred_categories = Column(Text, default="Mountains,Adventure,Heritage")  # Comma separated
    budget_range = Column(String(100), default="10000-30000")
    default_travellers = Column(Integer, default=2)
    default_origin = Column(String(100), default="Delhi")
    travel_style = Column(String(100), default="Balanced")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="preferences")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    state = Column(String(100), index=True, nullable=False)
    country = Column(String(100), default="India")
    category = Column(String(100), index=True, nullable=False)  # Mountains, Beaches, Heritage, etc.
    average_budget = Column(Float, nullable=False)  # Budget per person per day in INR
    average_temperature = Column(Float, nullable=False)  # in Celsius
    adventure_score = Column(Float, default=5.0)
    nature_score = Column(Float, default=5.0)
    nightlife_score = Column(Float, default=5.0)
    heritage_score = Column(Float, default=5.0)
    photography_score = Column(Float, default=5.0)
    family_friendly = Column(Boolean, default=True)
    best_season = Column(String(100), default="October - March")
    popularity_score = Column(Float, default=8.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    attractions = relationship("Attraction", back_populates="destination", cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="destination")
    feedback = relationship("Feedback", back_populates="destination")


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), default="Sightseeing")
    description = Column(Text, nullable=True)
    estimated_duration_hours = Column(Float, default=2.0)
    entry_fee = Column(Float, default=0.0)  # INR
    is_outdoor = Column(Boolean, default=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    popularity_rank = Column(Integer, default=1)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    destination = relationship("Destination", back_populates="attractions")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=True)
    title = Column(String(255), nullable=False)
    origin = Column(String(100), default="Delhi")
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    total_days = Column(Integer, default=3)
    travellers_count = Column(Integer, default=2)
    transport_mode = Column(String(50), default="Train")  # Flight, Train, Cab, Bus
    accommodation_type = Column(String(50), default="Standard (3-star)")  # Budget, Standard, Luxury
    food_preference = Column(String(50), default="Both")  # Veg, Non-Veg, Both
    total_budget = Column(Float, default=20000.0)
    status = Column(String(50), default="Upcoming")  # Upcoming, Completed, Draft
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="trips")
    destination = relationship("Destination", back_populates="trips")
    itineraries = relationship("Itinerary", back_populates="trip", cascade="all, delete-orphan", order_by="Itinerary.day_number")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)
    date = Column(String(50), nullable=True)
    activities_json = Column(JSON, nullable=False)  # List of activity objects
    estimated_daily_expense = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="itineraries")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # Transport, Accommodation, Food, Sightseeing, Misc
    estimated_amount = Column(Float, default=0.0)
    actual_amount = Column(Float, default=0.0)
    currency = Column(String(10), default="INR")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    trip = relationship("Trip", back_populates="expenses")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    rating = Column(Integer, default=5)
    liked = Column(Boolean, default=True)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="feedback")
    destination = relationship("Destination", back_populates="feedback")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    session_title = Column(String(255), default="Trip Assistance")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.id")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    date = Column(String(50), nullable=False)
    temperature_avg = Column(Float, nullable=False)
    temperature_min = Column(Float, nullable=False)
    temperature_max = Column(Float, nullable=False)
    precipitation_probability = Column(Float, default=0.0)
    weather_code = Column(Integer, default=0)
    summary = Column(String(255), default="Clear sky")
    cached_at = Column(DateTime, default=datetime.datetime.utcnow)
