from sqlalchemy import Column, Integer, VARCHAR, Boolean, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(50), unique=True, nullable=False)  # Unique title constraint
    description = Column(VARCHAR(255), nullable=True)
    status = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deadline = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.user_id"))  # Updated foreign key reference

    # Define relationship with User
    user = relationship("User", back_populates="tasks")

    __table_args__ = (
        UniqueConstraint("title", name="uq_task_title"),  # Explicit uniqueness
    )

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(VARCHAR(50), unique=True, nullable=False)  # Unique name constraint
    user_password = Column(VARCHAR(255), nullable=False)

    # Define relationship with Task
    tasks = relationship("Task", back_populates="user", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint("user_name", name="uq_user_name"),  # Explicit uniqueness
    )
