from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Prefixes(Base):
    __tablename__ = "prefixes"

    id = mapped_column(Integer, primary_key=True)
    associated_name = mapped_column(String, nullable=False, unique=True)
    prefix = mapped_column(String, nullable=False, unique=True)
