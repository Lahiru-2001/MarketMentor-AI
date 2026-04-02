from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings


# Create the main database engine using the connection URL
engine = create_engine(settings.DATABASE_URL)


# Create a session factory for database operations
# autocommit=False → changes are committed manually
# autoflush=False → prevents automatic flushing before queries
# bind=engine → attaches this session to the created engine
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Used in FastAPI endpoints with dependency injection
def get_db():
    db = SessionLocal()   # Create a new database session
    try:
        yield db         # Provide session to the route function
    finally:
        db.close()       # Always close session after request completes