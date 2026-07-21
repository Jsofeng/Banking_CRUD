import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()  # this will read backend/.env

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("TEST_DATABASE_URL")

engine = create_engine(DATABASE_URL)

# template for opening database connections.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
It links your Python classes to database tables and manages the metadata,
allowing you to define database schemas using object-oriented Python code.
"""

Base = declarative_base()
