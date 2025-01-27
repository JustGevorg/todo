from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///todoservice.db', echo=True)
SyncSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
