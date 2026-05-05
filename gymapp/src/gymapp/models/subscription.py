from .base import Base, Mapped, mapped_column, String, relationship, ForeignKey

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
    from .payment import Payment


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_client: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    subscription_type: Mapped[str] = mapped_column(
        nullable=False, default="default_subscription"
    )
    subscription_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    subscription_price: Mapped[float] = mapped_column(nullable=False, default=100)

    client: Mapped["Client"] = relationship(back_populates="subscription")
    payments: Mapped[list["Payment"]] = relationship(back_populates="subscription")

    # active_subscriptions
