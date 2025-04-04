from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from mixins import IdIntPkMixin
from base import Base


class UserProfile(IdIntPkMixin, Base):
    user_id: Mapped[str] = mapped_column(
        String, unique=True, index=True
    )  # ID пользователя из Keycloak
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
