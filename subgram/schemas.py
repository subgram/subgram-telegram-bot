from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from subgram.constants import EventType


class CheckoutPageResponse(BaseModel):
    subscription_uuid: UUID
    checkout_url: str


class SubscriptionStatusResponse(BaseModel):
    subscription_uuid: UUID
    status: str

    started_at: datetime | None
    ending_at: datetime | None
    cancelled_at: datetime | None
    
    user_has_access: bool
    can_be_purchased: bool
    can_be_cancelled: bool
    can_be_upgraded: bool


class CustomerEventObject(BaseModel):
    telegram_id: int
    name: str | None
    email: str | None
    language_code: str | None


class SubscriptionEventObject(BaseModel):
    status: SubscriptionStatusResponse
    customer: CustomerEventObject


class Event(BaseModel):
    event_id: int
    type: EventType
    object: SubscriptionEventObject