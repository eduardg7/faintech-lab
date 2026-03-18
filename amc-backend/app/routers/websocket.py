"""WebSocket Router Stub.

Placeholder for WebSocket functionality. Currently returns 501 Not Implemented.
"""

from fastapi import APIRouter

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket):
    """WebSocket endpoint placeholder."""
    await websocket.close(code=1003, reason="Not Implemented")
