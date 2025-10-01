from sqlalchemy import Column, Integer, String, DateTime, func
from config.db import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    tenant_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Campaign(id={self.id}, name='{self.name}', tenant_id={self.tenant_id})>"
