from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Table, Column, Integer, String, Date, ForeignKey, Boolean)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, metadata


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50), unique=True, index=True, nullable=False),
    Column("username", String(50), nullable=False),
    Column("hashed_password", String(1024), nullable=False),
    Column("date_of_birth", Date(), nullable=True),
    Column("phone_number", String(20), nullable=True),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),

)

file = Table(
    "file",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("link_download", String(), nullable=False),
    Column("author_id", Integer, ForeignKey("user.id")),
)

class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[str] = mapped_column(Date(), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True,
                                            nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
