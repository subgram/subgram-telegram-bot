from uuid import UUID
from pydantic import BaseModel


class CheckoutPageResponse(BaseModel):
    subscription_uuid: UUID
    checkout_url: str
