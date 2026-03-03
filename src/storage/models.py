from sqlalchemy import String, Text, DateTime, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


class JobListing(Base):
    __tablename__ = "job_listings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    company: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    occupation: Mapped[Optional[str]] = mapped_column(String(100))
    location: Mapped[Optional[str]] = mapped_column(String(255))

    salary_raw: Mapped[Optional[str]] = mapped_column(String(100))
    salary_max: Mapped[Optional[int]] = mapped_column(Integer)

    tech_stack: Mapped[Optional[str]] = mapped_column(Text)
    link: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)

    source_site: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    minio_key: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self) -> str:
        return f"<JobListing(company={self.company}, title={self.title})>"
