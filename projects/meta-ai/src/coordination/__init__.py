"""
Multi-Agent Coordination Protocol

This module implements the handoff protocol for coordinating task handoffs
between multiple AI agents in the Faintech OS ecosystem.

Task: LAB-004
Spec: projects/meta-ai/docs/handoff-protocol-spec.md
"""

from .types import (
    HandoffMessage,
    HandoffType,
    TaskContext,
    AgentInfo,
    ContextBlock,
    Artifact,
    Metadata,
    DeliveryConfig,
    MessageState,
    CyclingRisk,
)

__all__ = [
    "HandoffMessage",
    "HandoffType",
    "TaskContext",
    "AgentInfo",
    "ContextBlock",
    "Artifact",
    "Metadata",
    "DeliveryConfig",
    "MessageState",
    "CyclingRisk",
]
