"""
Handoff Protocol Types

Pydantic models for the Multi-Agent Handoff Protocol.
Implements the JSON schema defined in handoff-protocol-spec.md.

Task: LAB-004
Author: faintech-dev
Created: 2026-03-15
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class HandoffType(str, Enum):
    """Types of handoff between agents"""
    DELEGATION = "delegation"
    ESCALATION = "escalation"
    FALLBACK = "fallback"
    CONTINUATION = "continuation"


class TaskStatus(str, Enum):
    """Task status values"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    BLOCKED = "blocked"


class CyclingRisk(str, Enum):
    """Risk level for task cycling"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MessageState(str, Enum):
    """Handoff message delivery states"""
    PENDING = "pending"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"


class Priority(str, Enum):
    """Task priority levels"""
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class Artifact(BaseModel):
    """Represents a file, commit, PR, or URL artifact"""
    type: str = Field(..., description="Type: file, commit, pr, or url")
    path: str = Field(..., description="Path or URL to the artifact")
    description: str = Field(..., description="Description of the artifact")


class TaskContext(BaseModel):
    """Task information for handoff"""
    task_id: str = Field(..., description="Unique task identifier")
    project_id: str = Field(..., description="Project identifier")
    title: str = Field(..., description="Task title")
    status: TaskStatus = Field(..., description="Current task status")
    acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="List of acceptance criteria"
    )


class AgentInfo(BaseModel):
    """Agent information for handoff"""
    agent_id: str = Field(..., description="Agent identifier")
    role: str = Field(..., description="Agent role")
    session_id: Optional[str] = Field(None, description="Session identifier")
    reason: str = Field(..., description="Reason for handoff")


class ContextBlock(BaseModel):
    """Context block for handoff message"""
    summary: str = Field(..., description="Summary of work done")
    progress_percentage: int = Field(
        ...,
        ge=0,
        le=100,
        description="Progress percentage (0-100)"
    )
    blockers: list[str] = Field(
        default_factory=list,
        description="List of blockers"
    )
    decisions_made: list[str] = Field(
        default_factory=list,
        description="List of decisions made"
    )
    artifacts: list[Artifact] = Field(
        default_factory=list,
        description="List of artifacts created"
    )
    next_steps: list[str] = Field(
        default_factory=list,
        description="List of next steps"
    )


class RetryPolicy(BaseModel):
    """Retry policy for message delivery"""
    max_retries: int = Field(default=3, ge=0, description="Maximum retry attempts")
    backoff_seconds: int = Field(default=30, ge=0, description="Backoff time between retries")


class DeliveryConfig(BaseModel):
    """Delivery configuration for handoff message"""
    requires_acknowledgment: bool = Field(
        default=True,
        description="Whether acknowledgment is required"
    )
    ack_timeout_seconds: int = Field(
        default=300,
        ge=0,
        description="Timeout for acknowledgment"
    )
    retry_policy: RetryPolicy = Field(
        default_factory=RetryPolicy,
        description="Retry policy configuration"
    )


class Metadata(BaseModel):
    """Metadata for handoff tracking"""
    handoff_count: int = Field(default=1, ge=1, description="Number of handoffs")
    previous_agents: list[str] = Field(
        default_factory=list,
        description="List of previous agent IDs"
    )
    cycling_risk: CyclingRisk = Field(
        default=CyclingRisk.LOW,
        description="Cycling risk level"
    )
    priority: Priority = Field(
        default=Priority.P2,
        description="Task priority"
    )
    sla_deadline: Optional[datetime] = Field(
        None,
        description="SLA deadline (ISO-8601)"
    )

    def calculate_cycling_risk(self) -> CyclingRisk:
        """Calculate cycling risk based on handoff count and patterns"""
        if self.handoff_count >= 5:
            return CyclingRisk.HIGH
        elif self.handoff_count >= 3:
            return CyclingRisk.MEDIUM
        return CyclingRisk.LOW


class HandoffMessage(BaseModel):
    """
    Complete handoff message for multi-agent coordination.

    Implements the JSON schema from handoff-protocol-spec.md
    """
    protocol_version: str = Field(default="1.0", description="Protocol version")
    message_id: UUID = Field(
        default_factory=uuid4,
        description="Unique message identifier"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message timestamp (ISO-8601)"
    )
    handoff_type: HandoffType = Field(..., description="Type of handoff")

    task: TaskContext = Field(..., description="Task information")
    from_agent: AgentInfo = Field(..., description="Sending agent information")
    to_agent: AgentInfo = Field(..., description="Receiving agent information")
    context: ContextBlock = Field(..., description="Work context")
    metadata: Metadata = Field(
        default_factory=Metadata,
        description="Handoff metadata"
    )
    delivery: DeliveryConfig = Field(
        default_factory=DeliveryConfig,
        description="Delivery configuration"
    )

    # Internal state tracking
    _state: MessageState = MessageState.PENDING

    def check_cycling(self) -> bool:
        """
        Check if this handoff indicates task cycling.

        Returns True if cycling is detected (handoff should be blocked).
        """
        # Update cycling risk
        self.metadata.cycling_risk = self.metadata.calculate_cycling_risk()

        # Check for high cycling risk
        if self.metadata.cycling_risk == CyclingRisk.HIGH:
            return True

        # Check for repeated agent pair (same two agents passing back and forth)
        if len(self.metadata.previous_agents) >= 2:
            # If the receiving agent was in the previous agents list
            if self.to_agent.agent_id in self.metadata.previous_agents[-2:]:
                # And the sending agent is also in recent history
                if self.from_agent.agent_id in self.metadata.previous_agents[-2:]:
                    return True

        return False

    def to_json_dict(self) -> dict:
        """Convert to JSON-serializable dictionary"""
        return {
            "protocol_version": self.protocol_version,
            "message_id": str(self.message_id),
            "timestamp": self.timestamp.isoformat() + "Z",
            "handoff_type": self.handoff_type.value,
            "task": self.task.model_dump(),
            "from_agent": self.from_agent.model_dump(),
            "to_agent": self.to_agent.model_dump(),
            "context": self.context.model_dump(),
            "metadata": {
                **self.metadata.model_dump(),
                "sla_deadline": self.metadata.sla_deadline.isoformat() + "Z"
                    if self.metadata.sla_deadline else None
            },
            "delivery": self.delivery.model_dump()
        }

    class Config:
        json_schema_extra = {
            "example": {
                "protocol_version": "1.0",
                "message_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2026-03-15T14:00:00Z",
                "handoff_type": "delegation",
                "task": {
                    "task_id": "LAB-004",
                    "project_id": "faintech-lab",
                    "title": "Multi-Agent Coordination Protocol Prototype",
                    "status": "in_progress",
                    "acceptance_criteria": [
                        "Define JSON-based handoff protocol specification",
                        "Implement coordination prototype",
                        "Test handoff scenarios"
                    ]
                },
                "from_agent": {
                    "agent_id": "faintech-cto",
                    "role": "CTO",
                    "session_id": "session-cto-001",
                    "reason": "Implementation work delegated to Dev"
                },
                "to_agent": {
                    "agent_id": "faintech-dev",
                    "role": "Technical Lead",
                    "expected_action": "Implement protocol specification and prototype"
                },
                "context": {
                    "summary": "Protocol design complete, ready for implementation",
                    "progress_percentage": 20,
                    "blockers": [],
                    "decisions_made": [
                        "JSON-based format chosen",
                        "Four handoff types defined"
                    ],
                    "artifacts": [
                        {
                            "type": "file",
                            "path": "projects/meta-ai/docs/handoff-protocol-spec.md",
                            "description": "Initial protocol specification"
                        }
                    ],
                    "next_steps": [
                        "Create Python types",
                        "Implement handoff endpoint",
                        "Add test cases"
                    ]
                },
                "metadata": {
                    "handoff_count": 1,
                    "previous_agents": ["faintech-pm"],
                    "cycling_risk": "low",
                    "priority": "P1",
                    "sla_deadline": "2026-03-18T18:00:00Z"
                },
                "delivery": {
                    "requires_acknowledgment": True,
                    "ack_timeout_seconds": 300,
                    "retry_policy": {
                        "max_retries": 3,
                        "backoff_seconds": 30
                    }
                }
            }
        }
