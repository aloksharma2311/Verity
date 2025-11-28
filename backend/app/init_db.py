from .database import Base, engine
from . import models  # ensure models are imported so tables are known

def init_db():
    print("Dropping all tables (if any)...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init_db()
