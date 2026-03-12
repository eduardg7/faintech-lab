"""Stripe configuration and client initialization."""
import os
from typing import Optional
import stripe

from app.core.errors import AMCError


class StripeConfig:
    """Stripe configuration and pricing constants."""

    # Pricing tiers (in cents)
    STARTER_PRICE_ID = os.getenv("STRIPE_STARTER_PRICE_ID")  # $99/mo
    PRO_PRICE_ID = os.getenv("STRIPE_PRO_PRICE_ID")  # $199/mo

    @classmethod
    def get_client(cls) -> stripe.StripeClient:
        """Get configured Stripe client."""
        api_key = os.getenv("STRIPE_SECRET_KEY")
        if not api_key:
            raise AMCError(
                message="Stripe not configured",
                code="stripe_not_configured",
                status_code=500
            )
        return stripe.StripeClient(api_key=api_key)

    @classmethod
    def is_configured(cls) -> bool:
        """Check if Stripe is properly configured."""
        return bool(os.getenv("STRIPE_SECRET_KEY"))

    @classmethod
    def get_webhook_secret(cls) -> Optional[str]:
        """Get Stripe webhook secret for signature verification."""
        return os.getenv("STRIPE_WEBHOOK_SECRET")

    @classmethod
    def get_frontend_url(cls) -> str:
        """Get frontend URL for Stripe checkout success/cancel redirects."""
        return os.getenv("FRONTEND_URL", "http://localhost:3000")


# Pricing tier definitions
TIER_PRICING = {
    "starter": {
        "price_id": "STRIPE_STARTER_PRICE_ID",
        "monthly_amount_cents": 9900,
        "display_name": "Starter",
        "features": ["100 memories", "Basic search", "1 agent"]
    },
    "pro": {
        "price_id": "STRIPE_PRO_PRICE_ID",
        "monthly_amount_cents": 19900,
        "display_name": "Pro",
        "features": ["Unlimited memories", "Semantic search", "5 agents", "Priority support"]
    }
}


def get_tier_for_price_id(price_id: str) -> Optional[str]:
    """Map Stripe price ID to tier name."""
    for tier, config in TIER_PRICING.items():
        if config["price_id"] == price_id:
            return tier
    return None
