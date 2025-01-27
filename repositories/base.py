from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


class SqlalchemyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
