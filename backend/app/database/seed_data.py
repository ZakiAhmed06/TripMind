"""
Database Initializer & Seeder for TripMind
Populates destinations, attractions, and initial demo accounts from CSVs into the active database.
"""
import os
import pandas as pd
import logging
from sqlalchemy.orm import Session
from backend.app.database.session import SessionLocal, Base, engine
from backend.app.models import User, UserPreference, Destination, Attraction
from backend.app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db():
    logger.info("Creating database tables if not existing...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1. Seed Demo User
        demo_user = db.query(User).filter(User.email == "demo@tripmind.ai").first()
        if not demo_user:
            logger.info("Creating demo user: demo@tripmind.ai")
            demo_user = User(
                email="demo@tripmind.ai",
                full_name="Aarav Sharma",
                hashed_password=get_password_hash("TripMind123!"),
                is_active=True,
                is_admin=True
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

            # Preferences
            pref = UserPreference(
                user_id=demo_user.id,
                preferred_categories="Mountains,Adventure,Heritage,Nature",
                budget_range="15000-35000",
                default_travellers=2,
                default_origin="Delhi",
                travel_style="Balanced"
            )
            db.add(pref)
            db.commit()

        # 2. Seed Destinations
        dest_count = db.query(Destination).count()
        if dest_count < 300:
            csv_path = "data/processed/destinations.csv"
            if os.path.exists(csv_path):
                logger.info("Seeding destinations from %s...", csv_path)
                df_dest = pd.read_csv(csv_path)
                for _, row in df_dest.iterrows():
                    existing = db.query(Destination).filter(Destination.name == row["destination_name"]).first()
                    if not existing:
                        d = Destination(
                            name=row["destination_name"],
                            state=row["state"],
                            country=row.get("country", "India"),
                            category=row["category"],
                            average_budget=float(row["average_budget"]),
                            average_temperature=float(row["average_temperature"]),
                            adventure_score=float(row["adventure_score"]),
                            nature_score=float(row["nature_score"]),
                            nightlife_score=float(row["nightlife_score"]),
                            heritage_score=float(row["heritage_score"]),
                            photography_score=float(row["photography_score"]),
                            family_friendly=bool(row["family_friendly"]),
                            best_season=row["best_season"],
                            popularity_score=float(row["popularity_score"]),
                            latitude=float(row["latitude"]),
                            longitude=float(row["longitude"]),
                            description=row["description"],
                            image_url=row["image_url"]
                        )
                        db.add(d)
                db.commit()
                logger.info("Destinations seeded successfully.")

        # 3. Seed Attractions
        attr_count = db.query(Attraction).count()
        if attr_count < 500:
            attr_csv = "data/processed/attractions.csv"
            if os.path.exists(attr_csv):
                logger.info("Seeding attractions from %s...", attr_csv)
                df_attr = pd.read_csv(attr_csv)
                
                # Pre-fetch destination id mapping
                all_dest = {d.name.lower(): d.id for d in db.query(Destination).all()}
                
                for _, row in df_attr.iterrows():
                    d_id = all_dest.get(row["destination_name"].lower())
                    if d_id:
                        a = Attraction(
                            destination_id=d_id,
                            name=row["name"],
                            category=row.get("category", "Sightseeing"),
                            description=row.get("description", ""),
                            estimated_duration_hours=float(row.get("estimated_duration_hours", 2.0)),
                            entry_fee=float(row.get("entry_fee", 0.0)),
                            is_outdoor=bool(row.get("is_outdoor", True)),
                            latitude=float(row["latitude"]),
                            longitude=float(row["longitude"]),
                            popularity_rank=int(row.get("popularity_rank", 1)),
                            image_url=row.get("image_url", "")
                        )
                        db.add(a)
                db.commit()
                logger.info("Attractions seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    init_db()
