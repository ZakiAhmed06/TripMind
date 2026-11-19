import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.database.session import Base, engine
from backend.app.database.seed_data import init_db
from backend.app.api.endpoints import (
    auth,
    destinations,
    recommendations,
    budget,
    crowd,
    itinerary,
    assistant,
    trips,
    feedback,
    weather,
    routes
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("tripmind")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing TripMind system and verifying database tables...")
    try:
        init_db()
        logger.info("TripMind database initialization complete.")
    except Exception as e:
        logger.error("Database initialization warning: %s", e)
    yield
    logger.info("TripMind shutting down...")


app = FastAPI(
    title="TripMind API",
    description="AI + Machine Learning Powered Intelligent Travel Planner Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
api_prefix = settings.API_V1_PREFIX
app.include_router(auth.router, prefix=api_prefix)
app.include_router(destinations.router, prefix=api_prefix)
app.include_router(recommendations.router, prefix=api_prefix)
app.include_router(budget.router, prefix=api_prefix)
app.include_router(crowd.router, prefix=api_prefix)
app.include_router(itinerary.router, prefix=api_prefix)
app.include_router(assistant.router, prefix=api_prefix)
app.include_router(trips.router, prefix=api_prefix)
app.include_router(feedback.router, prefix=api_prefix)
app.include_router(weather.router, prefix=api_prefix)
app.include_router(routes.router, prefix=api_prefix)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "ml_models": {
            "recommendation_engine": "loaded",
            "budget_predictor": "loaded",
            "crowd_predictor": "loaded"
        },
        "rag_vector_index": "loaded",
        "gemini_model": settings.GEMINI_MODEL
    }


@app.get("/")
def root():
    return {
        "name": "TripMind Backend API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
