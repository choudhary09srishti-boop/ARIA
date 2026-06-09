from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
DB_PASSWORD = os.getenv("DB_PASSWORD")

project_ref = SUPABASE_URL.replace("https://", "").replace(".supabase.co", "")
DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)

DATABASE_URL = f"postgresql+psycopg2://postgres:{DB_PASSWORD_ENCODED}@db.{project_ref}.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        