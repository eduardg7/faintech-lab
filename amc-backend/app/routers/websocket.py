"""WebSocket router for real-time updates.

Provides WebSocket endpoints for:
- Real-time memory notifications
- Agent activity updates
- Ping/pong keepalive

Usage:
    Connect: ws://host/v1/ws?token=<jwt_token>

    Messages received:
    - {"type": "memory_created", "timestamp": "...", "data": {...}}
    - {"type": "memory_updated", "timestamp": "...", "data": {...}}
    - {"type": "memory_deleted", "timestamp": "...", "data": {"memory_id": "..."}}
    - {"type": "agent_activity", "timestamp": "...", "data": {...}}
    - {"type": "pong", "timestamp": "..."}

    Messages to send:
    - {"type": "ping"} -> responds with pong
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends

from app.core.websocket import connection_manager
from app.core.logging import get_logger
from app.routers.auth import get_current_auth_context, AuthContext

logger = get_logger("amc.websocket")

router = APIRouter(tags=["WebSocket"])


# Keepalive interval in seconds
KEEPALIVE_INTERVAL = 30


async def get_auth_from_token(token: Optional[str] = None) -> Optional[AuthContext]:
    """Extract auth context from token for WebSocket connection.

    Since WebSocket doesn't support standard auth headers,
    we accept the token as a query parameter.
    """
    if not token:
        return None

    try:
        # Use the existing auth validation
        from app.core.security import decode_token
        from app.core.database import get_db
        from app.models.user import User
        from sqlalchemy import select

        payload = decode_token(token)
        if not payload:
            return None

        user_id = payload.get("sub")
        workspace_id = payload.get("workspace_id")

        if not user_id or not workspace_id:
            return None

        return AuthContext(
            user_id=user_id,
            workspace_id=workspace_id,
            is_api_key=False,
        )
    except Exception as e:
        logger.warning(
            "websocket_auth_failed",
            extra={"extra": {"error": str(e)}},
        )
        return None


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None, description="JWT token for authentication"),
):
    """WebSocket endpoint for real-time updates.

    Authentication:
        Pass JWT token as query parameter: /ws?token=<your_jwt_token>

    Protocol:
        - Server sends: {"type": "event_type", "timestamp": "...", "data": {...}}
        - Client sends: {"type": "ping"} for keepalive
        - Server responds to ping with: {"type": "pong", "timestamp": "..."}

    Event types:
        - memory_created: New memory added to workspace
        - memory_updated: Memory updated
        - memory_deleted: Memory deleted
        - agent_activity: Agent activity update
    """
    # Authenticate
    auth_context = await get_auth_from_token(token)

    if not auth_context:
        await websocket.close(code=4001, reason="Unauthorized: Invalid or missing token")
        return

    workspace_id = auth_context.workspace_id
    user_id = auth_context.user_id

    # Connect
    await connection_manager.connect(websocket, workspace_id, user_id)

    try:
        # Send connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "workspace_id": workspace_id,
                "message": "Successfully connected to AMC real-time updates",
            }
        }))

        # Start keepalive task
        keepalive_task = asyncio.create_task(
            send_keepalive(websocket, workspace_id)
        )

        # Message handling loop
        while True:
            try:
                # Wait for messages with timeout
                message = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=60.0  # Check for disconnect every 60s
                )

                # Parse and handle the message
                await handle_client_message(websocket, message, workspace_id)

            except asyncio.TimeoutError:
                # No message received, check if connection is still alive
                continue

    except WebSocketDisconnect:
        logger.info(
            "websocket_client_disconnected",
            extra={"extra": {"workspace_id": workspace_id}},
        )
    except Exception as e:
        logger.error(
            "websocket_error",
            extra={"extra": {"error": str(e), "workspace_id": workspace_id}},
        )
    finally:
        keepalive_task.cancel()
        await connection_manager.disconnect(websocket)


async def handle_client_message(websocket: WebSocket, message: str, workspace_id: str):
    """Handle incoming messages from WebSocket clients."""
    try:
        data = json.loads(message)
        message_type = data.get("type", "unknown")

        if message_type == "ping":
            # Respond with pong
            await websocket.send_text(json.dumps({
                "type": "pong",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {}
            }))
        elif message_type == "subscribe":
            # Future: Support for subscribing to specific events/agents
            await websocket.send_text(json.dumps({
                "type": "subscribed",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {"message": "Subscription acknowledged"}
            }))
        else:
            # Unknown message type
            await websocket.send_text(json.dumps({
                "type": "error",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {"message": f"Unknown message type: {message_type}"}
            }))

    except json.JSONDecodeError:
        await websocket.send_text(json.dumps({
            "type": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"message": "Invalid JSON format"}
        }))


async def send_keepalive(websocket: WebSocket, workspace_id: str):
    """Send periodic keepalive pings to maintain connection.

    This is server-initiated keepalive to detect dead connections.
    """
    while True:
        try:
            await asyncio.sleep(KEEPALIVE_INTERVAL)

            # Send a server ping
            await websocket.send_text(json.dumps({
                "type": "server_ping",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {}
            }))

        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.debug(
                "keepalive_failed",
                extra={"extra": {"error": str(e), "workspace_id": workspace_id}},
            )
            break


@router.get("/ws/stats")
async def get_websocket_stats(
    auth_context: AuthContext = Depends(get_current_auth_context),
):
    """Get WebSocket connection statistics.

    Requires authentication. Returns connection counts per workspace.
    """
    stats = connection_manager.get_stats()
    return {
        "success": True,
        "data": stats,
    }
