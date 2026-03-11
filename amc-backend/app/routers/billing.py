"""Billing router for Stripe subscription management."""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
import stripe
from typing import Optional

from app.core.database import get_db
from app.core.stripe_config import StripeConfig
from app.core.errors import AMCError, ValidationError
from app.core.security import get_current_user, UserContext
from app.models.user import User
from app.schemas.billing import (
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    SubscriptionStatus,
    TierInfo,
    MessageResponse
)
from app.services.billing import BillingService


router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("/pricing")
async def get_pricing() -> dict:
    """Get available pricing tiers."""
    return {
        "tiers": ["starter", "pro"],
        "details": {
            "starter": {
                "price_id": StripeConfig.STARTER_PRICE_ID or "price_starter_placeholder",
                "monthly_amount": 99.00,
                "currency": "USD",
                "display_name": "Starter",
                "features": [
                    "100 stored memories",
                    "Basic keyword search",
                    "1 agent",
                    "Email support"
                ]
            },
            "pro": {
                "price_id": StripeConfig.PRO_PRICE_ID or "price_pro_placeholder",
                "monthly_amount": 199.00,
                "currency": "USD",
                "display_name": "Pro",
                "features": [
                    "Unlimited memories",
                    "Semantic search with embeddings",
                    "5 agents",
                    "Priority support",
                    "Advanced analytics"
                ]
            }
        }
    }


@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a Stripe Checkout session for subscription purchase.

    - **tier**: Pricing tier to subscribe to (starter|pro)

    Returns a checkout URL to redirect the user to Stripe.
    """
    if not StripeConfig.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing not configured"
        )

    billing_service = BillingService(db)
    session = await billing_service.create_checkout_session(
        workspace_id=current_user.workspace_id,
        tier=request.tier
    )

    return CheckoutSessionResponse(
        checkout_url=session.url,
        session_id=session.id
    )


@router.get("/subscription", response_model=SubscriptionStatus)
async def get_subscription_status(
    current_user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current subscription status for the workspace."""
    billing_service = BillingService(db)
    status_data = await billing_service.get_subscription_status(
        workspace_id=current_user.workspace_id
    )

    return SubscriptionStatus(**status_data)


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="Stripe-Signature"),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Stripe webhook events for subscription lifecycle.

    Processes events:
    - customer.subscription.created: New subscription activated
    - customer.subscription.updated: Subscription modified/cancelled
    - customer.subscription.deleted: Subscription cancelled
    """
    if not StripeConfig.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing not configured"
        )

    payload = await request.body()
    webhook_secret = StripeConfig.get_webhook_secret()

    if webhook_secret:
        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, webhook_secret
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payload"
            )
        except stripe.error.SignatureVerificationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )
    else:
        # In development/test without webhook secret, parse directly
        import json
        event = json.loads(payload.decode())

    # Process event
    billing_service = BillingService(db)
    await billing_service.handle_subscription_webhook(
        event_type=event["type"],
        data=event["data"]
    )

    return MessageResponse(message="Webhook processed")


@router.get("/tiers", response_model=list[TierInfo])
async def get_tiers():
    """Get available pricing tiers information."""
    from app.core.stripe_config import TIER_PRICING

    tiers = []
    for tier_key, tier_config in TIER_PRICING.items():
        tiers.append(TierInfo(
            name=tier_key,
            monthly_amount_cents=tier_config["monthly_amount_cents"],
            display_name=tier_config["display_name"],
            features=tier_config["features"]
        ))

    return tiers
