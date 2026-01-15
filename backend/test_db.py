from sqlalchemy import text
from core.dependencies import engine

try:

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Database connection successful")
        
except Exception as e:
   
    print("Database connection failed:", e)
