"""Billing schemas for Stripe integration."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TierInfo(BaseModel):
    """Information about a pricing tier."""
    name: str = Field(..., description="Tier name (starter|pro)")
    monthly_amount_cents: int = Field(..., description="Monthly price in cents")
    display_name: str = Field(..., description="Human-readable tier name")
    features: List[str] = Field(default_factory=list, description="Tier features list")


class CheckoutSessionRequest(BaseModel):
    """Request to create a Stripe Checkout session for subscription purchase."""
    tier: str = Field(..., pattern="^(starter|pro)$", description="Pricing tier to subscribe to")


class CheckoutSessionResponse(BaseModel):
    """Response containing Stripe Checkout URL for subscription purchase."""
    checkout_url: str = Field(..., description="Stripe Checkout URL to redirect user to")
    session_id: str = Field(..., description="Stripe Checkout session ID")


class SubscriptionStatus(BaseModel):
    """Current subscription status for a workspace."""
    active: bool = Field(..., description="Whether subscription is active")
    tier: Optional[str] = Field(None, description="Current tier (starter|pro)")
    status: Optional[str] = Field(None, description="Stripe subscription status")
    cancel_at_period_end: bool = Field(default=False, description="If subscription will cancel at period end")
    current_period_end: Optional[datetime] = Field(None, description="Current billing period end")
    stripe_customer_id: Optional[str] = Field(None, description="Stripe customer ID")


class WebhookEvent(BaseModel):
    """Raw Stripe webhook event (for internal processing)."""
    event_type: str = Field(..., alias="type")
    data: dict = Field(..., alias="data")


class MessageResponse(BaseModel):
    """Generic success/error message."""
    message: str
