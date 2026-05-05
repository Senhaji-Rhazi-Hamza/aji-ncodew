from .base import Base, Mapped, mapped_column, String, relationship, object_session
from datetime import timedelta, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .subscription import Subscription
    from .payment import Payment


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    Tel: Mapped[str | None]
    mail: Mapped[str | None]

    subscription: Mapped["Subscription"] = relationship(back_populates="client")
    payments: Mapped[list["Payment"]] = relationship(back_populates="client")

    @property
    def total_payments_amount(self):
        return sum([payment.amount for payment in self.payments])

    # subscribe

    def subscribe(self):
        from .subscription import Subscription

        if self.subscription is None:
            session = object_session(self)
            return Subscription.create(session=session, id_client=self.id)  # type: ignore
        else:
            raise Exception("Client can't have 2 subscriptions")

    # due_amount
    def get_due_amount_for_my_sub(self):

        months_due = (
            int((datetime.today() - self.subscription.subscription_date).days / 30) + 1
        )
        return (
            months_due * self.subscription.subscription_price
            - self.total_payments_amount
        )

    # pay_subscription
    def pay_subscription(self, amount):
        from .payment import Payment

        amount_to_pay = self.get_due_amount_for_my_sub()
        if amount <= amount_to_pay:
            session = object_session(self)
            return Payment.create(session=session, id_client=self.id, id_subscription=self.subscription.id, amount=amount)  # type: ignore
        return None
