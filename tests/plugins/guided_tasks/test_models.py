"""Tests for the guided_tasks models module."""

from __future__ import annotations

import datetime as dt
import json

import pytest

from plugins.guided_tasks.models import (
    AcceptanceCriterion,
    FileChange,
    FinalReview,
    GuidedTask,
    PlannedStep,
    RiskLevel,
    TaskState,
    ValidationResult,
)


class TestPlannedStep:
    def test_valid_creation(self) -> None:
        step = PlannedStep(step_id="step-1", title="Write tests", description="Write unit tests", order=0)
        assert step.step_id == "step-1"
        assert step.title == "Write tests"
        assert step.description == "Write unit tests"
        assert step.order == 0

    def test_factory_create(self) -> None:
        step = PlannedStep.create("Write tests", "Write unit tests", order=0)
        assert step.step_id.startswith("step-")
        assert step.title == "Write tests"

    def test_rejects_empty_step_id(self) -> None:
        with pytest.raises(ValueError, match="step_id is required"):
            PlannedStep(step_id="", title="Test")

    def test_rejects_empty_title(self) -> None:
        with pytest.raises(ValueError, match="title is required"):
            PlannedStep(step_id="step-1", title="")

    def test_strips_whitespace(self) -> None:
        step = PlannedStep(step_id="  step-1  ", title="  Write tests  ", description="  Desc  ")
        assert step.step_id == "step-1"
        assert step.title == "Write tests"
        assert step.description == "Desc"

    def test_serialization_roundtrip(self) -> None:
        original = PlannedStep.create("Test", "Desc", order=1, estimated_duration_seconds=60)
        data = original.to_dict()
        restored = PlannedStep.from_dict(data)
        assert restored.step_id == original.step_id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.order == original.order
        assert restored.estimated_duration_seconds == original.estimated_duration_seconds


class TestFileChange:
    def test_valid_creation(self) -> None:
        change = FileChange(path="src/main.py", change_type="modify", reason="Fix bug")
        assert change.path == "src/main.py"
        assert change.change_type == "modify"
        assert change.reason == "Fix bug"
        assert change.new_path is None

    def test_move_requires_new_path(self) -> None:
        with pytest.raises(ValueError, match="new_path is required"):
            FileChange(path="src/old.py", change_type="move")

    def test_move_with_new_path(self) -> None:
        change = FileChange(path="src/old.py", change_type="move", new_path="src/new.py")
        assert change.new_path == "src/new.py"

    def test_rejects_empty_path(self) -> None:
        with pytest.raises(ValueError, match="path is required"):
            FileChange(path="", change_type="create")

    def test_rejects_invalid_change_type(self) -> None:
        with pytest.raises(ValueError, match="change_type must be one of"):
            FileChange(path="src/main.py", change_type="invalid")

    def test_serialization_roundtrip(self) -> None:
        original = FileChange(path="src/main.py", change_type="modify", reason="Fix", new_path=None)
        data = original.to_dict()
        restored = FileChange.from_dict(data)
        assert restored.path == original.path
        assert restored.change_type == original.change_type
        assert restored.reason == original.reason
        assert restored.new_path == original.new_path


class TestAcceptanceCriterion:
    def test_valid_creation(self) -> None:
        ac = AcceptanceCriterion(criterion_id="ac-1", description="Tests pass", satisfied=True, evidence="CI green")
        assert ac.criterion_id == "ac-1"
        assert ac.description == "Tests pass"
        assert ac.satisfied is True
        assert ac.evidence == "CI green"

    def test_factory_create(self) -> None:
        ac = AcceptanceCriterion.create("All tests pass")
        assert ac.criterion_id.startswith("ac-")
        assert ac.description == "All tests pass"
        assert ac.satisfied is False

    def test_rejects_empty_criterion_id(self) -> None:
        with pytest.raises(ValueError, match="criterion_id is required"):
            AcceptanceCriterion(criterion_id="", description="Test")

    def test_rejects_empty_description(self) -> None:
        with pytest.raises(ValueError, match="description is required"):
            AcceptanceCriterion(criterion_id="ac-1", description="")

    def test_serialization_roundtrip(self) -> None:
        original = AcceptanceCriterion.create("Tests pass")
        original.satisfied = True
        original.evidence = "CI log"
        data = original.to_dict()
        restored = AcceptanceCriterion.from_dict(data)
        assert restored.criterion_id == original.criterion_id
        assert restored.description == original.description
        assert restored.satisfied == original.satisfied
        assert restored.evidence == original.evidence


class TestValidationResult:
    def test_valid_creation(self) -> None:
        vr = ValidationResult(
            validation_id="val-1",
            target_id="ac-1",
            target_type="criterion",
            passed=True,
            message="All good",
        )
        assert vr.validation_id == "val-1"
        assert vr.target_id == "ac-1"
        assert vr.target_type == "criterion"
        assert vr.passed is True

    def test_factory_create(self) -> None:
        vr = ValidationResult.create("ac-1", "criterion", True, "Passed", {"detail": "value"})
        assert vr.validation_id.startswith("val-")
        assert vr.target_id == "ac-1"
        assert vr.target_type == "criterion"
        assert vr.passed is True
        assert vr.details == {"detail": "value"}

    def test_rejects_empty_validation_id(self) -> None:
        with pytest.raises(ValueError, match="validation_id is required"):
            ValidationResult(validation_id="", target_id="ac-1", target_type="criterion", passed=True)

    def test_rejects_empty_target_id(self) -> None:
        with pytest.raises(ValueError, match="target_id is required"):
            ValidationResult(validation_id="val-1", target_id="", target_type="criterion", passed=True)

    def test_rejects_invalid_target_type(self) -> None:
        with pytest.raises(ValueError, match="target_type must be one of"):
            ValidationResult(
                validation_id="val-1",
                target_id="ac-1",
                target_type="invalid",
                passed=True,
            )

    def test_normalizes_utc_timestamp(self) -> None:
        # Naive datetime should be treated as UTC
        naive = dt.datetime(2024, 1, 15, 12, 0, 0)
        vr = ValidationResult(
            validation_id="val-1",
            target_id="ac-1",
            target_type="criterion",
            passed=True,
            validated_at=naive,
        )
        assert vr.validated_at.tzinfo is not None
        assert vr.validated_at.tzinfo.utcoffset(vr.validated_at) == dt.timedelta(0)

    def test_serialization_roundtrip(self) -> None:
        original = ValidationResult.create("ac-1", "criterion", True, "OK")
        data = original.to_dict()
        restored = ValidationResult.from_dict(data)
        assert restored.validation_id == original.validation_id
        assert restored.target_id == original.target_id
        assert restored.target_type == original.target_type
        assert restored.passed == original.passed
        assert restored.message == original.message
        assert restored.validated_at == original.validated_at


class TestFinalReview:
    def test_valid_creation(self) -> None:
        review = FinalReview(
            reviewer="alice",
            decision="approved",
            summary="LGTM",
            notes="Ready to merge",
        )
        assert review.reviewer == "alice"
        assert review.decision == "approved"
        assert review.summary == "LGTM"
        assert review.notes == "Ready to merge"

    def test_rejects_empty_reviewer(self) -> None:
        with pytest.raises(ValueError, match="reviewer is required"):
            FinalReview(reviewer="", decision="approved", summary="OK")

    def test_rejects_empty_summary(self) -> None:
        with pytest.raises(ValueError, match="summary is required"):
            FinalReview(reviewer="alice", decision="approved", summary="")

    def test_rejects_invalid_decision(self) -> None:
        with pytest.raises(ValueError, match="decision must be one of"):
            FinalReview(reviewer="alice", decision="invalid", summary="OK")

    def test_serialization_roundtrip(self) -> None:
        original = FinalReview(reviewer="alice", decision="approved", summary="Good", notes="Nice")
        data = original.to_dict()
        restored = FinalReview.from_dict(data)
        assert restored.reviewer == original.reviewer
        assert restored.decision == original.decision
        assert restored.summary == original.summary
        assert restored.notes == original.notes
        assert restored.reviewed_at == original.reviewed_at


class TestGuidedTask:
    def test_valid_creation_via_factory(self) -> None:
        task = GuidedTask.create("Add feature X", "Implement feature X", created_by="alice", risk_level="high")
        assert task.task_id.startswith("task-")
        assert task.title == "Add feature X"
        assert task.objective == "Implement feature X"
        assert task.created_by == "alice"
        assert task.risk_level == "high"
        assert task.state == "draft"
        assert task.parent_task_id is None
        assert task.root_task_id is None
        assert isinstance(task.created_at, dt.datetime)
        assert isinstance(task.updated_at, dt.datetime)
        assert task.created_at.tzinfo is not None
        assert task.updated_at.tzinfo is not None

    def test_valid_creation_direct(self) -> None:
        task = GuidedTask(
            task_id="task-1",
            title="Task",
            objective="Do something",
            parent_task_id="parent-1",
            root_task_id="root-1",
            created_by="bob",
        )
        assert task.task_id == "task-1"
        assert task.parent_task_id == "parent-1"
        assert task.root_task_id == "root-1"

    def test_rejects_empty_task_id(self) -> None:
        with pytest.raises(ValueError, match="task_id is required"):
            GuidedTask(task_id="", title="T", objective="O")

    def test_rejects_empty_title(self) -> None:
        with pytest.raises(ValueError, match="title is required"):
            GuidedTask(task_id="t-1", title="", objective="O")

    def test_rejects_empty_objective(self) -> None:
        with pytest.raises(ValueError, match="objective is required"):
            GuidedTask(task_id="t-1", title="T", objective="")

    def test_rejects_invalid_state(self) -> None:
        with pytest.raises(ValueError, match="Invalid state"):
            GuidedTask(task_id="t-1", title="T", objective="O", state="invalid")

    def test_rejects_invalid_risk_level(self) -> None:
        with pytest.raises(ValueError, match="Invalid risk_level"):
            GuidedTask(task_id="t-1", title="T", objective="O", risk_level="extreme")

    def test_add_step(self) -> None:
        task = GuidedTask.create("T", "O")
        step = task.add_step("Step 1", "First step", 30)
        assert len(task.steps) == 1
        assert step.step_id.startswith("step-")
        assert step.title == "Step 1"
        assert step.order == 0

    def test_add_file_change(self) -> None:
        task = GuidedTask.create("T", "O")
        change = task.add_file_change("src/main.py", "modify", "Fix bug")
        assert len(task.file_changes) == 1
        assert change.path == "src/main.py"
        assert change.change_type == "modify"

    def test_add_acceptance_criterion(self) -> None:
        task = GuidedTask.create("T", "O")
        ac = task.add_acceptance_criterion("Tests pass")
        assert len(task.acceptance_criteria) == 1
        assert ac.description == "Tests pass"
        assert ac.satisfied is False

    def test_add_validation_result(self) -> None:
        task = GuidedTask.create("T", "O")
        vr = task.add_validation_result("ac-1", "criterion", True, "Passed")
        assert len(task.validation_results) == 1
        assert vr.target_id == "ac-1"
        assert vr.target_type == "criterion"
        assert vr.passed is True

    def test_set_final_review(self) -> None:
        task = GuidedTask.create("T", "O")
        review = task.set_final_review("alice", "approved", "Good work", "Ready")
        assert task.final_review is not None
        assert task.final_review.reviewer == "alice"
        assert task.final_review.decision == "approved"

    def test_state_transitions(self) -> None:
        task = GuidedTask.create("T", "O")
        assert task.state == "draft"

        task.transition_to("planned")
        assert task.state == "planned"

        task.transition_to("awaiting_approval")
        assert task.state == "awaiting_approval"

        task.transition_to("approved")
        assert task.state == "approved"

        task.transition_to("running")
        assert task.state == "running"

        task.transition_to("validation")
        assert task.state == "validation"

        task.transition_to("review")
        assert task.state == "review"

        task.transition_to("completed")
        assert task.state == "completed"

    def test_invalid_state_transition(self) -> None:
        task = GuidedTask.create("T", "O")
        with pytest.raises(ValueError, match="Invalid state transition"):
            task.transition_to("approved")  # draft -> approved not allowed

    def test_touch_updates_timestamp(self) -> None:
        task = GuidedTask.create("T", "O")
        original = task.updated_at
        import time
        time.sleep(0.01)
        task.add_step("New step")
        assert task.updated_at > original

    def test_serialization_roundtrip(self) -> None:
        task = GuidedTask.create("Feature", "Implement feature", created_by="alice", risk_level="high")
        task.add_step("Write code", "Write the implementation")
        task.add_step("Write tests", "Write unit tests")
        task.add_file_change("src/feature.py", "create", "New feature")
        task.add_acceptance_criterion("All tests pass")
        task.add_acceptance_criterion("No lint errors")
        task.add_validation_result("ac-1", "criterion", True, "CI green")
        task.set_final_review("bob", "approved", "Ready", "Ship it")
        task.transition_to("planned")

        data = task.to_dict()
        restored = GuidedTask.from_dict(data)

        assert restored.task_id == task.task_id
        assert restored.title == task.title
        assert restored.objective == task.objective
        assert restored.parent_task_id == task.parent_task_id
        assert restored.root_task_id == task.root_task_id
        assert restored.created_by == task.created_by
        assert restored.risk_level == task.risk_level
        assert restored.state == task.state
        assert len(restored.steps) == len(task.steps)
        assert len(restored.file_changes) == len(task.file_changes)
        assert len(restored.acceptance_criteria) == len(task.acceptance_criteria)
        assert len(restored.validation_results) == len(task.validation_results)
        assert restored.final_review is not None
        assert restored.final_review.reviewer == task.final_review.reviewer
        assert restored.created_at == task.created_at
        assert restored.updated_at == task.updated_at

    def test_json_roundtrip(self) -> None:
        task = GuidedTask.create("JSON Test", "Test JSON serialization")
        task.add_step("Step 1")
        json_str = task.to_json()
        restored = GuidedTask.from_json(json_str)
        assert restored.task_id == task.task_id
        assert restored.title == task.title

    def test_lineage_preservation(self) -> None:
        parent = GuidedTask.create("Parent", "Parent task")
        child = GuidedTask.create("Child", "Child task", parent_task_id=parent.task_id, root_task_id=parent.task_id)

        data = child.to_dict()
        restored = GuidedTask.from_dict(data)

        assert restored.parent_task_id == parent.task_id
        assert restored.root_task_id == parent.task_id

    def test_list_isolation(self) -> None:
        """Mutating a list on one instance must not affect another."""
        task1 = GuidedTask.create("T1", "O1")
        task2 = GuidedTask.create("T2", "O2")
        task1.add_step("Step for task1")
        assert len(task1.steps) == 1
        assert len(task2.steps) == 0

    def test_timestamp_normalization_from_dict(self) -> None:
        """ISO strings with 'Z' or offset should normalize to UTC."""
        now = dt.datetime.now(dt.timezone.utc)
        iso_with_z = now.isoformat().replace("+00:00", "Z")
        task = GuidedTask.from_dict({
            "task_id": "t-1",
            "title": "T",
            "objective": "O",
            "created_at": iso_with_z,
            "updated_at": iso_with_z,
        })
        assert task.created_at.tzinfo is not None
        assert task.updated_at.tzinfo is not None

    def test_default_factory_lists_are_independent(self) -> None:
        """Each instance gets its own list, not a shared mutable default."""
        task1 = GuidedTask(task_id="t-1", title="T1", objective="O1")
        task2 = GuidedTask(task_id="t-2", title="T2", objective="O2")
        task1.steps.append(PlannedStep(step_id="s-1", title="Step"))
        assert len(task2.steps) == 0

    def test_rejects_empty_created_by(self) -> None:
        with pytest.raises(ValueError, match="created_by cannot be empty"):
            GuidedTask(task_id="t-1", title="T", objective="O", created_by="   ")

    def test_lineage_root_task(self) -> None:
        """Root task returns only its own task_id."""
        task = GuidedTask.create("Root", "Root task")
        assert task.lineage_ids() == [task.task_id]

    def test_lineage_direct_child(self) -> None:
        """Direct child returns root_task_id, parent_task_id, task_id."""
        parent = GuidedTask.create("Parent", "Parent task")
        child = GuidedTask.create("Child", "Child task", parent_task_id=parent.task_id, root_task_id=parent.task_id)
        # root_task_id == parent_task_id, so no duplicate
        assert child.lineage_ids() == [parent.task_id, child.task_id]

    def test_lineage_root_and_parent_distinct(self) -> None:
        """When root_task_id and parent_task_id differ, both appear without duplication."""
        root = GuidedTask.create("Root", "Root task")
        parent = GuidedTask.create("Parent", "Parent task", parent_task_id=root.task_id, root_task_id=root.task_id)
        child = GuidedTask.create("Child", "Child task", parent_task_id=parent.task_id, root_task_id=root.task_id)
        assert child.lineage_ids() == [root.task_id, parent.task_id, child.task_id]

    def test_lineage_no_duplicate_ids(self) -> None:
        """Same ID appearing in multiple fields must not be duplicated in output."""
        root = GuidedTask.create("Root", "Root task")
        # parent_task_id == root_task_id == root.task_id
        child = GuidedTask.create("Child", "Child task", parent_task_id=root.task_id, root_task_id=root.task_id)
        lineage = child.lineage_ids()
        # root.task_id appears only once
        assert lineage.count(root.task_id) == 1
        assert child.task_id in lineage
        assert len(lineage) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])