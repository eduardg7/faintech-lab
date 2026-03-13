"""Billing router for Stripe subscription management."""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
import stripe
from typing import Optional

from app.core.database import get_db
from app.core.stripe_config import StripeConfig
from app.core.errors import AMCError, ValidationError
from app.routers.auth import get_current_user
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


@router.get(
    "/pricing",
    summary="Get pricing tiers",
    description="Returns available subscription tiers with features and pricing.",
    responses={
        200: {
            "description": "Pricing information for all tiers",
            "content": {
                "application/json": {
                    "example": {
                        "tiers": ["starter", "pro"],
                        "details": {
                            "starter": {
                                "price_id": "price_starter123",
                                "monthly_amount": 99.00,
                                "currency": "USD",
                                "display_name": "Starter",
                                "features": ["100 stored memories", "Basic keyword search"]
                            },
                            "pro": {
                                "price_id": "price_pro456",
                                "monthly_amount": 199.00,
                                "currency": "USD",
                                "display_name": "Pro",
                                "features": ["Unlimited memories", "Semantic search"]
                            }
                        }
                    }
                }
            }
        }
    }
)
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


@router.post(
    "/checkout",
    response_model=CheckoutSessionResponse,
    summary="Create Stripe checkout session",
    description="""
Create a Stripe Checkout session for subscription purchase.

## Authentication

Requires JWT Bearer token (user session). API keys are not supported.

## Flow

1. User selects a tier (starter/pro)
2. Frontend calls this endpoint
3. Redirect user to the returned `checkout_url`
4. User completes payment on Stripe
5. Stripe sends webhook to `/billing/webhook`
6. Subscription is activated

## Response

Returns a Stripe Checkout URL to redirect the user to.
""",
    responses={
        200: {
            "description": "Checkout session created",
            "content": {
                "application/json": {
                    "example": {
                        "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_...",
                        "session_id": "cs_test_abc123xyz"
                    }
                }
            }
        },
        401: {"description": "Authentication required"},
        503: {"description": "Billing not configured (missing Stripe keys)"}
    }
)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    current_user: User = Depends(get_current_user),
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


@router.get(
    "/subscription",
    response_model=SubscriptionStatus,
    summary="Get subscription status",
    description="""
Get current subscription status for the authenticated user's workspace.

## Authentication

Requires JWT Bearer token.

## Response Fields

- `tier`: Current subscription tier (starter/pro)
- `status`: Stripe subscription status (active/past_due/canceled)
- `current_period_end`: When current billing period ends
- `cancel_at_period_end`: Whether subscription will cancel at period end
""",
    responses={
        200: {
            "description": "Subscription status",
            "content": {
                "application/json": {
                    "example": {
                        "tier": "pro",
                        "status": "active",
                        "current_period_end": "2024-02-15T00:00:00Z",
                        "cancel_at_period_end": False
                    }
                }
            }
        },
        401: {"description": "Authentication required"}
    }
)
async def get_subscription_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current subscription status for the workspace."""
    billing_service = BillingService(db)
    status_data = await billing_service.get_subscription_status(
        workspace_id=current_user.workspace_id
    )

    return SubscriptionStatus(**status_data)


@router.post(
    "/webhook",
    summary="Handle Stripe webhook events",
    description="""
Handle Stripe webhook events for subscription lifecycle.

## Security

This endpoint requires signature verification via `STRIPE_WEBHOOK_SECRET`.
Requests without valid signatures are rejected to prevent forged events.

## Supported Events

| Event | Description |
|-------|-------------|
| `customer.subscription.created` | New subscription activated |
| `customer.subscription.updated` | Subscription modified/cancelled |
| `customer.subscription.deleted` | Subscription cancelled |

## Headers

- `Stripe-Signature`: Webhook signature from Stripe

## Local Testing

Use Stripe CLI to forward webhooks:
```bash
stripe listen --forward-to localhost:8000/v1/billing/webhook
```
""",
    responses={
        200: {"description": "Webhook processed successfully"},
        400: {"description": "Invalid payload or signature"},
        503: {"description": "Webhook verification not configured"}
    }
)
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

    Security: Requires STRIPE_WEBHOOK_SECRET to be configured. Webhooks are rejected
    without signature verification to prevent forged subscription lifecycle events.
    """
    if not StripeConfig.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Billing not configured"
        )

    webhook_secret = StripeConfig.get_webhook_secret()
    if not webhook_secret:
        # Reject webhooks entirely when secret is not configured
        # to prevent forged subscription events. Local test mode should configure
        # STRIPE_WEBHOOK_SECRET explicitly or use Stripe CLI forwarding.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook signature verification not configured - billing disabled"
        )

    payload = await request.body()

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
