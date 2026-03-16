"""
Tests for Handoff Protocol Types

Task: LAB-004
Author: faintech-dev
"""

import pytest
from datetime import datetime, timedelta
from uuid import UUID

from projects.meta_ai.src.coordination.types import (
    HandoffMessage,
    HandoffType,
    TaskContext,
    TaskStatus,
    AgentInfo,
    ContextBlock,
    Metadata,
    DeliveryConfig,
    CyclingRisk,
    Priority,
    Artifact,
)


class TestArtifact:
    """Tests for Artifact model"""

    def test_create_file_artifact(self):
        """Test creating a file artifact"""
        artifact = Artifact(
            type="file",
            path="projects/meta-ai/docs/handoff-protocol-spec.md",
            description="Protocol specification"
        )
        assert artifact.type == "file"
        assert artifact.path == "projects/meta-ai/docs/handoff-protocol-spec.md"

    def test_create_pr_artifact(self):
        """Test creating a PR artifact"""
        artifact = Artifact(
            type="pr",
            path="https://github.com/example/repo/pull/123",
            description="Feature PR"
        )
        assert artifact.type == "pr"


class TestTaskContext:
    """Tests for TaskContext model"""

    def test_create_task_context(self):
        """Test creating task context"""
        task = TaskContext(
            task_id="LAB-004",
            project_id="faintech-lab",
            title="Multi-Agent Coordination Protocol",
            status=TaskStatus.IN_PROGRESS,
            acceptance_criteria=["Define protocol", "Implement types"]
        )
        assert task.task_id == "LAB-004"
        assert task.status == TaskStatus.IN_PROGRESS
        assert len(task.acceptance_criteria) == 2


class TestAgentInfo:
    """Tests for AgentInfo model"""

    def test_create_agent_info(self):
        """Test creating agent info"""
        agent = AgentInfo(
            agent_id="faintech-dev",
            role="Technical Lead",
            session_id="session-001",
            reason="Task assignment"
        )
        assert agent.agent_id == "faintech-dev"
        assert agent.role == "Technical Lead"


class TestContextBlock:
    """Tests for ContextBlock model"""

    def test_create_context_block(self):
        """Test creating context block"""
        context = ContextBlock(
            summary="Protocol implementation started",
            progress_percentage=30,
            blockers=["Waiting for review"],
            decisions_made=["Using Pydantic for validation"],
            next_steps=["Add tests", "Implement endpoint"]
        )
        assert context.progress_percentage == 30
        assert len(context.blockers) == 1

    def test_progress_validation(self):
        """Test progress percentage validation"""
        with pytest.raises(ValueError):
            ContextBlock(
                summary="Test",
                progress_percentage=150  # Invalid: > 100
            )


class TestMetadata:
    """Tests for Metadata model"""

    def test_default_cycling_risk(self):
        """Test default cycling risk is low"""
        metadata = Metadata()
        assert metadata.cycling_risk == CyclingRisk.LOW

    def test_calculate_cycling_risk_low(self):
        """Test cycling risk calculation - low"""
        metadata = Metadata(handoff_count=1)
        assert metadata.calculate_cycling_risk() == CyclingRisk.LOW

    def test_calculate_cycling_risk_medium(self):
        """Test cycling risk calculation - medium"""
        metadata = Metadata(handoff_count=3)
        assert metadata.calculate_cycling_risk() == CyclingRisk.MEDIUM

    def test_calculate_cycling_risk_high(self):
        """Test cycling risk calculation - high"""
        metadata = Metadata(handoff_count=5)
        assert metadata.calculate_cycling_risk() == CyclingRisk.HIGH


class TestHandoffMessage:
    """Tests for HandoffMessage model"""

    @pytest.fixture
    def valid_handoff(self):
        """Create a valid handoff message for testing"""
        return HandoffMessage(
            handoff_type=HandoffType.DELEGATION,
            task=TaskContext(
                task_id="LAB-004",
                project_id="faintech-lab",
                title="Multi-Agent Coordination Protocol",
                status=TaskStatus.IN_PROGRESS
            ),
            from_agent=AgentInfo(
                agent_id="faintech-cto",
                role="CTO",
                reason="Delegating implementation to Dev"
            ),
            to_agent=AgentInfo(
                agent_id="faintech-dev",
                role="Technical Lead",
                reason="Implement types and endpoint"
            ),
            context=ContextBlock(
                summary="Protocol spec complete",
                progress_percentage=20
            )
        )

    def test_create_handoff_message(self, valid_handoff):
        """Test creating a handoff message"""
        assert valid_handoff.protocol_version == "1.0"
        assert valid_handoff.handoff_type == HandoffType.DELEGATION
        assert isinstance(valid_handoff.message_id, UUID)

    def test_to_json_dict(self, valid_handoff):
        """Test JSON serialization"""
        json_dict = valid_handoff.to_json_dict()

        assert json_dict["protocol_version"] == "1.0"
        assert json_dict["handoff_type"] == "delegation"
        assert json_dict["task"]["task_id"] == "LAB-004"
        assert "timestamp" in json_dict
        assert "Z" in json_dict["timestamp"]  # ISO-8601 with Z

    def test_check_cycling_low_risk(self, valid_handoff):
        """Test cycling detection - low risk"""
        is_cycling = valid_handoff.check_cycling()
        assert is_cycling is False
        assert valid_handoff.metadata.cycling_risk == CyclingRisk.LOW

    def test_check_cycling_high_risk(self, valid_handoff):
        """Test cycling detection - high risk"""
        valid_handoff.metadata.handoff_count = 5
        is_cycling = valid_handoff.check_cycling()
        assert is_cycling is True
        assert valid_handoff.metadata.cycling_risk == CyclingRisk.HIGH

    def test_check_cycling_repeated_agents(self, valid_handoff):
        """Test cycling detection - repeated agent pair"""
        valid_handoff.metadata.previous_agents = ["faintech-dev", "faintech-cto"]
        valid_handoff.from_agent.agent_id = "faintech-dev"
        valid_handoff.to_agent.agent_id = "faintech-cto"

        is_cycling = valid_handoff.check_cycling()
        # Should detect cycling when same two agents pass task back and forth
        assert is_cycling is True

    def test_different_handoff_types(self, valid_handoff):
        """Test different handoff types"""
        # Delegation
        valid_handoff.handoff_type = HandoffType.DELEGATION
        assert valid_handoff.handoff_type == HandoffType.DELEGATION

        # Escalation
        valid_handoff.handoff_type = HandoffType.ESCALATION
        assert valid_handoff.handoff_type == HandoffType.ESCALATION

        # Fallback
        valid_handoff.handoff_type = HandoffType.FALLBACK
        assert valid_handoff.handoff_type == HandoffType.FALLBACK

        # Continuation
        valid_handoff.handoff_type = HandoffType.CONTINUATION
        assert valid_handoff.handoff_type == HandoffType.CONTINUATION


class TestHandoffTypes:
    """Tests for different handoff type scenarios"""

    def test_delegation_handoff(self):
        """Test delegation handoff scenario"""
        handoff = HandoffMessage(
            handoff_type=HandoffType.DELEGATION,
            task=TaskContext(
                task_id="LAB-004",
                project_id="faintech-lab",
                title="Coordination Protocol",
                status=TaskStatus.TODO
            ),
            from_agent=AgentInfo(
                agent_id="faintech-pm",
                role="PM",
                reason="Backend work requires Dev expertise"
            ),
            to_agent=AgentInfo(
                agent_id="faintech-dev",
                role="Technical Lead",
                reason="Implement protocol"
            ),
            context=ContextBlock(
                summary="Ready for implementation",
                progress_percentage=0
            )
        )
        assert handoff.handoff_type == HandoffType.DELEGATION

    def test_escalation_handoff(self):
        """Test escalation handoff scenario"""
        handoff = HandoffMessage(
            handoff_type=HandoffType.ESCALATION,
            task=TaskContext(
                task_id="LAB-004",
                project_id="faintech-lab",
                title="Coordination Protocol",
                status=TaskStatus.BLOCKED
            ),
            from_agent=AgentInfo(
                agent_id="faintech-dev",
                role="Technical Lead",
                reason="Architectural decision requires CEO approval"
            ),
            to_agent=AgentInfo(
                agent_id="faintech-ceo",
                role="CEO",
                reason="Approve architecture decision"
            ),
            context=ContextBlock(
                summary="Blocked on auth strategy decision",
                progress_percentage=40,
                blockers=["Missing architectural decision on auth strategy"]
            )
        )
        assert handoff.handoff_type == HandoffType.ESCALATION
        assert len(handoff.context.blockers) > 0

    def test_continuation_handoff(self):
        """Test continuation handoff scenario (shift handoff)"""
        handoff = HandoffMessage(
            handoff_type=HandoffType.CONTINUATION,
            task=TaskContext(
                task_id="LAB-004",
                project_id="faintech-lab",
                title="Coordination Protocol",
                status=TaskStatus.IN_PROGRESS
            ),
            from_agent=AgentInfo(
                agent_id="faintech-dev",
                role="Technical Lead",
                session_id="session-day-shift",
                reason="Shift handoff - task in progress"
            ),
            to_agent=AgentInfo(
                agent_id="faintech-dev",
                role="Technical Lead",
                session_id="session-night-shift",
                reason="Continue implementation"
            ),
            context=ContextBlock(
                summary="Types implemented, tests pending",
                progress_percentage=60,
                next_steps=["Add tests", "Implement endpoint"]
            )
        )
        assert handoff.handoff_type == HandoffType.CONTINUATION
