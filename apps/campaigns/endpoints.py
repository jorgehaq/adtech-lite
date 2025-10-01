from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.db import get_db
from apps.campaigns.models import Campaign
from pydantic import BaseModel

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

class CampaignCreate(BaseModel):
    name: str

@router.post("/")
def create_campaign(
    payload: CampaignCreate,
    db: Session = Depends(get_db),
    request: Request = None
):
    tenant_id = request.state.tenant_id
    campaign = Campaign(name=payload.name, tenant_id=tenant_id)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.get("/")
def list_campaigns(
    db: Session = Depends(get_db),
    request: Request = None
):
    tenant_id = request.state.tenant_id
    return db.query(Campaign).filter_by(tenant_id=tenant_id).all()
