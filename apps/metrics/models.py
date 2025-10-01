from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from config.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    tenant_id = Column(Integer, nullable=False, index=True)
    type = Column(String(20), nullable=False)  # "impression" o "click"
    created_at = Column(DateTime, server_default=func.now(), index=True)

    def __repr__(self) -> str:
        return (
            f"<Event(id={self.id}, campaign_id={self.campaign_id}, "
            f"tenant_id={self.tenant_id}, type='{self.type}')>"
        )
