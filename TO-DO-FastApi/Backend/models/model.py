from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from config.db import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)  # Unique title constraint
    description = Column(String, nullable=True)
    status = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint("title", name="uq_task_title"),  # Explicit uniqueness
    )
