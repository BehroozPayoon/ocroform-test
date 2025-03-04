from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, String, Date

from src.core.db import Base, TimestampMixin


class BalanceResult(Base, TimestampMixin):

    __tablename__ = "balance_results"

    balance_type: Mapped[str] = mapped_column(
        String(length=100), default="DAILY")
    balance_date: Mapped[date] = mapped_column(Date(), nullable=False)
    balance: Mapped[float] = mapped_column(Float(), default=0.0)
    source_file: Mapped[str] = mapped_column(String(1000), nullable=False)
