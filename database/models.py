import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database.database_config import Base, engine


class Task(Base):
    __tablename__ = 'tasks'
    

    id: Mapped[int] = mapped_column(primary_key=True, index=True, comment="Уникальный идентификатор записи")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          comment="Дата и время создания записи")
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(),
                                                          server_default=func.now(),
                                                          comment="Дата и время обновления записи")

    name: Mapped[str] = mapped_column(String(length=128), unique=True, comment="Название задачи")
    description: Mapped[str] = mapped_column(comment="Описание задачи")
    done: Mapped[bool] = mapped_column(comment="Отметка о выполнении задачи", nullable=False, default=False,
                                       server_default="FALSE")
