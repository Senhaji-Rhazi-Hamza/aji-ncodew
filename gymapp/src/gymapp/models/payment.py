from .base import Base, Mapped, mapped_column, String, relationship, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .client import Client
    from .subscription import Subscription

class Payment(Base):
    __tablename__ = "payments"

    id:              Mapped[int]   = mapped_column(primary_key=True, autoincrement=True)
    id_client:       Mapped[int]   = mapped_column(ForeignKey("clients.id"),       nullable=False)
    id_subscription: Mapped[int]   = mapped_column(ForeignKey("subscriptions.id"), nullable=False)
    payment_date:    Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    amount:          Mapped[float] = mapped_column(nullable=False)

    client:       Mapped["Client"]       = relationship(back_populates="payments")
    subscription: Mapped["Subscription"] = relationship(back_populates="payments")