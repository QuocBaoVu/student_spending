from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database URL for SQLite
DB_URL = "sqlite:///student_spending_app.db"

def get_db_connection():
    engine = create_engine(DB_URL, echo=True)
    return engine



