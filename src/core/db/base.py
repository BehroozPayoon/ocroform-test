from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger


class Base(DeclarativeBase):
    id: Mapped[BigInteger] = mapped_column(
        BigInteger(), primary_key=True, index=True)
