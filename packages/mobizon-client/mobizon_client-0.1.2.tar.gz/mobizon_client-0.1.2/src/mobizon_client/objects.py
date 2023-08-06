from datetime import datetime
from decimal import Decimal
from typing import NamedTuple


class Balance(NamedTuple):
    balance: Decimal
    currency: str

    @classmethod
    def restore(cls, payload: dict):
        return cls(
            currency=payload.get('currency'),
            balance=Decimal(payload.get('balance')).quantize(Decimal('0.00'))
        )


class MessageInfo(NamedTuple):
    campaign_id: str
    message_id: str
    status: int

    @classmethod
    def restore(cls, payload: dict):
        return cls(
            campaign_id=payload.get('campaignId'),
            message_id=payload.get('messageId'),
            status=payload.get('status'),
        )


class MessageStatus(NamedTuple):
    message_id: str
    segment_count: int
    status: str
    created_at: datetime
    last_updated_at: datetime

    @classmethod
    def restore(cls, payload: dict):
        return cls(
            message_id=payload.get('id'),
            segment_count=payload.get('segNum'),
            status=payload.get('status'),
            created_at=datetime.strptime(payload.get('startSendTs'), '%Y-%m-%d %H:%M:%S'),
            last_updated_at=datetime.strptime(payload.get('statusUpdateTs'), '%Y-%m-%d %H:%M:%S'),
        )
