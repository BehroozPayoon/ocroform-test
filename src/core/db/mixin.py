from datetime import datetime

from sqlalchemy import DateTime, func, FetchedValue
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class TimestampMixin(DeclarativeBase):

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(),
                                                 server_default=FetchedValue())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(),
                                                 server_default=FetchedValue(),
                                                 server_onupdate=FetchedValue())
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=FetchedValue(), nullable=True)
