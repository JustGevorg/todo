from database.models import Base
from database.database_config import engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)