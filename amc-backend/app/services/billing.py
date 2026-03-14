"""Billing service for Stripe integration."""
import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.stripe_config import StripeConfig, TIER_PRICING, get_tier_for_price_id
from app.core.errors import AMCError, NotFoundError
from app.models.workspace import Workspace


class BillingService:
    """Service for handling Stripe billing operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.stripe = StripeConfig.get_client()

    async def get_workspace_by_stripe_customer_id(
        self,
        stripe_customer_id: str
    ) -> Optional[Workspace]:
        """Find workspace by Stripe customer ID."""
        query = select(Workspace).where(
            Workspace.stripe_customer_id == stripe_customer_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_checkout_session(
        self,
        workspace_id: str,
        tier: str
    ) -> stripe.checkout.Session:
        """
        Create a Stripe Checkout session for subscription purchase.

        Args:
            workspace_id: Internal workspace ID
            tier: Pricing tier (starter|pro)

        Returns:
            Stripe Checkout session object

        Raises:
            AMCError: If Stripe not configured or invalid tier
        """
        # Validate tier
        if tier not in TIER_PRICING:
            raise AMCError(
                message=f"Invalid tier: {tier}",
                code="invalid_tier",
                status_code=400
            )

        # Get workspace
        query = select(Workspace).where(Workspace.id == workspace_id)
        result = await self.db.execute(query)
        workspace = result.scalar_one_or_none()
        if not workspace:
            raise NotFoundError(f"Workspace not found: {workspace_id}")

        # Get or create Stripe customer
        if workspace.stripe_customer_id:
            customer_id = workspace.stripe_customer_id
        else:
            # Create new Stripe customer
            customer = self.stripe.customers.create(
                email=workspace.slug,  # Use slug as identifier
                metadata={"workspace_id": workspace_id}
            )
            customer_id = customer.id
            workspace.stripe_customer_id = customer_id
            await self.db.flush()

        # Get price ID for tier from configured Stripe price IDs
        if tier == "starter":
            price_id = StripeConfig.STARTER_PRICE_ID
        elif tier == "pro":
            price_id = StripeConfig.PRO_PRICE_ID
        else:
            # This should not happen due to validation above
            raise AMCError(
                message=f"Unknown tier: {tier}",
                code="invalid_tier",
                status_code=400
            )

        if not price_id:
            raise AMCError(
                message=f"Stripe price ID not configured for tier: {tier}",
                code="stripe_not_configured",
                status_code=500
            )

        # Create checkout session
        try:
            session = self.stripe.checkout.sessions.create(
                customer=customer_id,
                mode="subscription",
                payment_method_types=["card"],
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                success_url=f"{StripeConfig.get_frontend_url()}/billing?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{StripeConfig.get_frontend_url()}/billing?canceled=true",
                metadata={"workspace_id": workspace_id, "tier": tier}
            )
            return session
        except stripe.error.StripeError as e:
            raise AMCError(
                message=f"Stripe error: {str(e)}",
                code="stripe_error",
                status_code=500
            )

    async def get_subscription_status(
        self,
        workspace_id: str
    ) -> dict:
        """
        Get subscription status for a workspace.

        Args:
            workspace_id: Internal workspace ID

        Returns:
            Dict with subscription status details
        """
        query = select(Workspace).where(Workspace.id == workspace_id)
        result = await self.db.execute(query)
        workspace = result.scalar_one_or_none()
        if not workspace:
            raise NotFoundError(f"Workspace not found: {workspace_id}")

        # If no Stripe subscription, return default status
        if not workspace.stripe_subscription_id:
            return {
                "active": False,
                "tier": None,
                "status": None,
                "cancel_at_period_end": False,
                "current_period_end": None,
                "stripe_customer_id": workspace.stripe_customer_id
            }

        # Fetch subscription from Stripe
        try:
            subscription = self.stripe.subscriptions.retrieve(
                workspace.stripe_subscription_id
            )

            # Map Stripe status to active flag
            is_active = subscription.status in [
                "active", "trialing", "past_due"
            ]

            # Get tier from price
            tier = None
            if subscription.items and subscription.items.data:
                price_id = subscription.items.data[0].price.id
                tier = get_tier_for_price_id(price_id)

            return {
                "active": is_active,
                "tier": tier,
                "status": subscription.status,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "current_period_end": subscription.current_period_end,
                "stripe_customer_id": workspace.stripe_customer_id
            }
        except stripe.error.StripeError as e:
            raise AMCError(
                message=f"Stripe error: {str(e)}",
                code="stripe_error",
                status_code=500
            )

    async def handle_subscription_webhook(self, event_type: str, data: dict):
        """
        Handle Stripe subscription webhook events.

        Args:
            event_type: Stripe event type
            data: Event data payload
        """
        if event_type == "customer.subscription.created":
            await self._handle_subscription_created(data)
        elif event_type == "customer.subscription.updated":
            await self._handle_subscription_updated(data)
        elif event_type == "customer.subscription.deleted":
            await self._handle_subscription_deleted(data)
        # Other events can be logged but not processed

    async def _handle_subscription_created(self, data: dict):
        """Handle new subscription creation."""
        subscription = data.get("object", {})
        customer_id = subscription.get("customer")

        # Find workspace by Stripe customer ID
        workspace = await self.get_workspace_by_stripe_customer_id(customer_id)
        if workspace:
            workspace.stripe_subscription_id = subscription.get("id")
            # Tier would be set based on price in full implementation
            await self.db.commit()

    async def _handle_subscription_updated(self, data: dict):
        """Handle subscription updates (cancellation, tier change, etc.)."""
        subscription = data.get("object", {})
        customer_id = subscription.get("customer")

        workspace = await self.get_workspace_by_stripe_customer_id(customer_id)
        if workspace:
            workspace.stripe_subscription_id = subscription.get("id")
            # Update tier based on price if needed
            await self.db.commit()

    async def _handle_subscription_deleted(self, data: dict):
        """Handle subscription deletion (cancellation)."""
        subscription = data.get("object", {})
        customer_id = subscription.get("customer")

        workspace = await self.get_workspace_by_stripe_customer_id(customer_id)
        if workspace:
            workspace.stripe_subscription_id = None
            # Keep stripe_customer_id but clear subscription
            await self.db.commit()
