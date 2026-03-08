import time
from app.database import engine, Base
import app.models  # forces model registration


def startup_db():
    retries = 15
    for i in range(retries):
        try:
            with engine.connect():
                print("Database connected")
                print("Tables:", Base.metadata.tables.keys())
                Base.metadata.create_all(bind=engine)
                print("Tables created")
                return
        except Exception as e:
            print(f"DB not ready ({i+1}/{retries}): {e}")
            time.sleep(2)
