from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///todoservice.db', echo=True)
async_engine = create_async_engine('sqlite+aiosqlite:///todoservice.db', echo=True)
SyncSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
Base = declarative_base()
