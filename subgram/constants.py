from enum import Enum

class EventType(str, Enum):
    SUBSCRIPTION_STARTED = "subscription.started"
    SUBSCRIPTION_RENEWED = "subscription.renewed"
    SUBSCRIPTION_RENEW_FAILED = "subscription.renew_failed"
    SUBSCRIPTION_CANCELLED = "subscription.cancelled"
    SUBSCRIPTION_UPGRADED = "subscription.upgraded"

