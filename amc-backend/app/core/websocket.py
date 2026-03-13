"""WebSocket Connection Manager for real-time updates.

Provides real-time notifications for:
- New memories added
- Memory updates
- Agent activity

Architecture:
- ConnectionManager handles client connections per workspace
- Broadcast functions for different event types
- Ping/pong for connection keepalive
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from fastapi import WebSocket, WebSocketDisconnect
from app.core.logging import get_logger

logger = get_logger("amc.websocket")


class ConnectionManager:
    """Manages WebSocket connections organized by workspace.

    Each workspace has its own set of connections to ensure
    proper isolation and targeted broadcasts.
    """

    def __init__(self):
        # workspace_id -> set of WebSocket connections
        self._connections: Dict[str, set[WebSocket]] = {}
        # Track connection metadata
        self._metadata: Dict[WebSocket, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, workspace_id: str, user_id: Optional[str] = None):
        """Accept and register a new WebSocket connection.

        Args:
            websocket: The WebSocket connection
            workspace_id: The workspace this connection belongs to
            user_id: Optional user ID for tracking
        """
        await websocket.accept()

        async with self._lock:
            if workspace_id not in self._connections:
                self._connections[workspace_id] = set()
            self._connections[workspace_id].add(websocket)
            self._metadata[websocket] = {
                "workspace_id": workspace_id,
                "user_id": user_id,
                "connected_at": datetime.now(timezone.utc),
            }

        logger.info(
            "websocket_connected",
            extra={
                "extra": {
                    "workspace_id": workspace_id,
                    "user_id": user_id,
                    "total_connections": self._count_connections(),
                }
            },
        )

    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        async with self._lock:
            metadata = self._metadata.pop(websocket, None)
            if metadata:
                workspace_id = metadata.get("workspace_id")
                if workspace_id and workspace_id in self._connections:
                    self._connections[workspace_id].discard(websocket)
                    if not self._connections[workspace_id]:
                        del self._connections[workspace_id]

        logger.info(
            "websocket_disconnected",
            extra={
                "extra": {
                    "total_connections": self._count_connections(),
                }
            },
        )

    def _count_connections(self) -> int:
        """Count total active connections."""
        return sum(len(conns) for conns in self._connections.values())

    async def broadcast_to_workspace(
        self,
        workspace_id: str,
        event_type: str,
        data: Dict[str, Any]
    ) -> int:
        """Broadcast a message to all connections in a workspace.

        Args:
            workspace_id: Target workspace
            event_type: Type of event (e.g., 'memory_created', 'memory_updated')
            data: Event payload

        Returns:
            Number of connections that received the message
        """
        message = json.dumps({
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        })

        delivered = 0
        connections = self._connections.get(workspace_id, set()).copy()

        for websocket in connections:
            try:
                await websocket.send_text(message)
                delivered += 1
            except Exception as e:
                logger.warning(
                    "websocket_send_failed",
                    extra={"extra": {"error": str(e)}},
                )

        logger.debug(
            "broadcast_sent",
            extra={
                "extra": {
                    "workspace_id": workspace_id,
                    "event_type": event_type,
                    "delivered": delivered,
                }
            },
        )

        return delivered

    async def broadcast_memory_created(self, workspace_id: str, memory_data: Dict[str, Any]):
        """Broadcast when a new memory is created."""
        await self.broadcast_to_workspace(workspace_id, "memory_created", memory_data)

    async def broadcast_memory_updated(self, workspace_id: str, memory_data: Dict[str, Any]):
        """Broadcast when a memory is updated."""
        await self.broadcast_to_workspace(workspace_id, "memory_updated", memory_data)

    async def broadcast_memory_deleted(self, workspace_id: str, memory_id: str):
        """Broadcast when a memory is deleted."""
        await self.broadcast_to_workspace(workspace_id, "memory_deleted", {"memory_id": memory_id})

    async def broadcast_agent_activity(
        self,
        workspace_id: str,
        agent_id: str,
        activity_type: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Broadcast agent activity updates."""
        await self.broadcast_to_workspace(
            workspace_id,
            "agent_activity",
            {
                "agent_id": agent_id,
                "activity_type": activity_type,
                "details": details or {},
            }
        )

    def get_workspace_connections(self, workspace_id: str) -> int:
        """Get the number of active connections for a workspace."""
        return len(self._connections.get(workspace_id, set()))

    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        return {
            "total_connections": self._count_connections(),
            "workspaces": {
                workspace_id: len(conns)
                for workspace_id, conns in self._connections.items()
            },
        }


# Global connection manager instance
connection_manager = ConnectionManager()
