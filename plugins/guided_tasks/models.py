"""Typed, serializable models for Harness Guided Tasks.

This module defines the contractual data structures for guided tasks. It uses
only the Python standard library — no Pydantic, no external dependencies.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import uuid
from typing import Any, Literal, Optional


# ─── Literal types ────────────────────────────────────────────────────────────

TaskState = Literal[
    "draft",
    "planned",
    "awaiting_approval",
    "approved",
    "running",
    "validation",
    "review",
    "completed",
    "failed",
    "cancelled",
]

RiskLevel = Literal["low", "moderate", "high", "critical"]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _utc_now() -> dt.datetime:
    """Return current UTC time with timezone info."""
    return dt.datetime.now(dt.timezone.utc)


def _normalize_utc(value: Any) -> dt.datetime:
    """Normalize a datetime-like value to an aware UTC datetime.

    Accepts:
    - datetime (naive or aware) → assumes UTC if naive
    - ISO-8601 string (with or without 'Z')
    - None → returns utc_now()
    """
    if value is None:
        return _utc_now()
    if isinstance(value, dt.datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=dt.timezone.utc)
        return value.astimezone(dt.timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return _utc_now()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = dt.datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    raise TypeError(f"Cannot normalize {type(value).__name__} to UTC datetime")


def _serialize_utc(value: dt.datetime) -> str:
    """Serialize a UTC datetime to ISO-8601 with 'Z' suffix."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    utc = value.astimezone(dt.timezone.utc)
    return utc.isoformat().replace("+00:00", "Z")


def _generate_id(prefix: str = "") -> str:
    """Generate a stable, unique ID."""
    suffix = uuid.uuid4().hex[:12]
    return f"{prefix}{suffix}" if prefix else suffix


# ─── Core Models ──────────────────────────────────────────────────────────────

@dataclasses.dataclass
class PlannedStep:
    """A single planned step within a guided task."""

    step_id: str
    title: str
    description: str = ""
    order: int = 0
    estimated_duration_seconds: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.step_id or not self.step_id.strip():
            raise ValueError("PlannedStep.step_id is required and cannot be empty")
        if not self.title or not self.title.strip():
            raise ValueError("PlannedStep.title is required and cannot be empty")
        self.step_id = self.step_id.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()

    @classmethod
    def create(cls, title: str, description: str = "", order: int = 0,
               estimated_duration_seconds: Optional[int] = None) -> "PlannedStep":
        """Factory to create a step with an auto-generated ID."""
        return cls(
            step_id=_generate_id("step-"),
            title=title,
            description=description,
            order=order,
            estimated_duration_seconds=estimated_duration_seconds,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "title": self.title,
            "description": self.description,
            "order": self.order,
            "estimated_duration_seconds": self.estimated_duration_seconds,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlannedStep":
        return cls(
            step_id=data["step_id"],
            title=data["title"],
            description=data.get("description", ""),
            order=data.get("order", 0),
            estimated_duration_seconds=data.get("estimated_duration_seconds"),
        )


@dataclasses.dataclass
class FileChange:
    """A file that may be changed as part of a guided task."""

    path: str
    change_type: Literal["create", "modify", "delete", "move"]
    reason: str = ""
    new_path: Optional[str] = None  # used when change_type == "move"

    def __post_init__(self) -> None:
        if not self.path or not self.path.strip():
            raise ValueError("FileChange.path is required and cannot be empty")
        self.path = self.path.strip()
        
        valid_change_types = {"create", "modify", "delete", "move"}
        if self.change_type not in valid_change_types:
            raise ValueError(
                f"FileChange.change_type must be one of {sorted(valid_change_types)}, got '{self.change_type}'"
            )
        
        if self.change_type == "move":
            if not self.new_path or not self.new_path.strip():
                raise ValueError("FileChange.new_path is required when change_type is 'move'")
            self.new_path = self.new_path.strip()
        self.reason = self.reason.strip()

    def to_dict(self) -> dict[str, Any]:
        result = {
            "path": self.path,
            "change_type": self.change_type,
            "reason": self.reason,
        }
        if self.new_path is not None:
            result["new_path"] = self.new_path
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FileChange":
        return cls(
            path=data["path"],
            change_type=data["change_type"],
            reason=data.get("reason", ""),
            new_path=data.get("new_path"),
        )


@dataclasses.dataclass
class AcceptanceCriterion:
    """A single acceptance criterion for a guided task."""

    criterion_id: str
    description: str
    satisfied: bool = False
    evidence: str = ""

    def __post_init__(self) -> None:
        if not self.criterion_id or not self.criterion_id.strip():
            raise ValueError("AcceptanceCriterion.criterion_id is required and cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("AcceptanceCriterion.description is required and cannot be empty")
        self.criterion_id = self.criterion_id.strip()
        self.description = self.description.strip()
        self.evidence = self.evidence.strip()

    @classmethod
    def create(cls, description: str) -> "AcceptanceCriterion":
        """Factory to create a criterion with an auto-generated ID."""
        return cls(criterion_id=_generate_id("ac-"), description=description)

    def to_dict(self) -> dict[str, Any]:
        return {
            "criterion_id": self.criterion_id,
            "description": self.description,
            "satisfied": self.satisfied,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AcceptanceCriterion":
        return cls(
            criterion_id=data["criterion_id"],
            description=data["description"],
            satisfied=data.get("satisfied", False),
            evidence=data.get("evidence", ""),
        )


@dataclasses.dataclass
class ValidationResult:
    """Result of a validation check against an acceptance criterion or task requirement."""

    validation_id: str
    target_id: str  # criterion_id or step_id
    target_type: Literal["criterion", "step", "task"]
    passed: bool
    message: str = ""
    details: dict[str, Any] = dataclasses.field(default_factory=dict)
    validated_at: dt.datetime = dataclasses.field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.validation_id or not self.validation_id.strip():
            raise ValueError("ValidationResult.validation_id is required and cannot be empty")
        if not self.target_id or not self.target_id.strip():
            raise ValueError("ValidationResult.target_id is required and cannot be empty")
        
        valid_target_types = {"criterion", "step", "task"}
        if self.target_type not in valid_target_types:
            raise ValueError(
                f"ValidationResult.target_type must be one of {sorted(valid_target_types)}, got '{self.target_type}'"
            )
        
        self.validation_id = self.validation_id.strip()
        self.target_id = self.target_id.strip()
        self.message = self.message.strip()
        self.validated_at = _normalize_utc(self.validated_at)

    @classmethod
    def create(cls, target_id: str, target_type: Literal["criterion", "step", "task"],
               passed: bool, message: str = "", details: Optional[dict[str, Any]] = None) -> "ValidationResult":
        """Factory to create a validation result with an auto-generated ID."""
        return cls(
            validation_id=_generate_id("val-"),
            target_id=target_id,
            target_type=target_type,
            passed=passed,
            message=message,
            details=details or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "target_id": self.target_id,
            "target_type": self.target_type,
            "passed": self.passed,
            "message": self.message,
            "details": self.details,
            "validated_at": _serialize_utc(self.validated_at),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ValidationResult":
        return cls(
            validation_id=data["validation_id"],
            target_id=data["target_id"],
            target_type=data["target_type"],
            passed=data["passed"],
            message=data.get("message", ""),
            details=data.get("details", {}),
            validated_at=data.get("validated_at"),
        )


@dataclasses.dataclass
class FinalReview:
    """Final review summary for a completed or cancelled task."""

    reviewer: str
    decision: Literal["approved", "rejected", "needs_revision"]
    summary: str
    notes: str = ""
    reviewed_at: dt.datetime = dataclasses.field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.reviewer or not self.reviewer.strip():
            raise ValueError("FinalReview.reviewer is required and cannot be empty")
        if not self.summary or not self.summary.strip():
            raise ValueError("FinalReview.summary is required and cannot be empty")
        
        valid_decisions = {"approved", "rejected", "needs_revision"}
        if self.decision not in valid_decisions:
            raise ValueError(
                f"FinalReview.decision must be one of {sorted(valid_decisions)}, got '{self.decision}'"
            )
        
        self.reviewer = self.reviewer.strip()
        self.summary = self.summary.strip()
        self.notes = self.notes.strip()
        self.reviewed_at = _normalize_utc(self.reviewed_at)

    def to_dict(self) -> dict[str, Any]:
        return {
            "reviewer": self.reviewer,
            "decision": self.decision,
            "summary": self.summary,
            "notes": self.notes,
            "reviewed_at": _serialize_utc(self.reviewed_at),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FinalReview":
        return cls(
            reviewer=data["reviewer"],
            decision=data["decision"],
            summary=data["summary"],
            notes=data.get("notes", ""),
            reviewed_at=data.get("reviewed_at"),
        )


# ─── Main Task Model ──────────────────────────────────────────────────────────

@dataclasses.dataclass
class GuidedTask:
    """A guided task with full identity, lineage, plan, risk, acceptance criteria,
    validation results, final review, and state machine."""

    # Identity & lineage
    task_id: str
    title: str
    objective: str
    parent_task_id: Optional[str] = None
    root_task_id: Optional[str] = None  # top-most ancestor
    created_by: str = "system"
    created_at: dt.datetime = dataclasses.field(default_factory=_utc_now)
    updated_at: dt.datetime = dataclasses.field(default_factory=_utc_now)

    # Plan
    steps: list[PlannedStep] = dataclasses.field(default_factory=list)
    file_changes: list[FileChange] = dataclasses.field(default_factory=list)

    # Risk & acceptance
    risk_level: RiskLevel = "moderate"
    acceptance_criteria: list[AcceptanceCriterion] = dataclasses.field(default_factory=list)

    # Validation & review
    validation_results: list[ValidationResult] = dataclasses.field(default_factory=list)
    final_review: Optional[FinalReview] = None

    # State machine
    state: TaskState = "draft"

    # Metadata
    metadata: dict[str, Any] = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        # Validate required fields
        if not self.task_id or not self.task_id.strip():
            raise ValueError("GuidedTask.task_id is required and cannot be empty")
        if not self.title or not self.title.strip():
            raise ValueError("GuidedTask.title is required and cannot be empty")
        if not self.objective or not self.objective.strip():
            raise ValueError("GuidedTask.objective is required and cannot be empty")

        self.task_id = self.task_id.strip()
        self.title = self.title.strip()
        self.objective = self.objective.strip()
        if self.parent_task_id is not None:
            self.parent_task_id = self.parent_task_id.strip() or None
        if self.root_task_id is not None:
            self.root_task_id = self.root_task_id.strip() or None
        self.created_by = self.created_by.strip()
        if not self.created_by:
            raise ValueError("GuidedTask.created_by cannot be empty after stripping whitespace")
        self.created_at = _normalize_utc(self.created_at)
        self.updated_at = _normalize_utc(self.updated_at)

        # Validate state
        valid_states: set[TaskState] = {
            "draft", "planned", "awaiting_approval", "approved",
            "running", "validation", "review", "completed", "failed", "cancelled"
        }
        if self.state not in valid_states:
            raise ValueError(f"Invalid state: {self.state}. Must be one of {sorted(valid_states)}")

        # Validate risk level
        valid_risks: set[RiskLevel] = {"low", "moderate", "high", "critical"}
        if self.risk_level not in valid_risks:
            raise ValueError(f"Invalid risk_level: {self.risk_level}. Must be one of {sorted(valid_risks)}")

    @classmethod
    def create(cls, title: str, objective: str, created_by: str = "system",
               parent_task_id: Optional[str] = None, root_task_id: Optional[str] = None,
               risk_level: RiskLevel = "moderate") -> "GuidedTask":
        """Factory to create a new task with auto-generated IDs and timestamps."""
        task_id = _generate_id("task-")
        now = _utc_now()
        root_id = root_task_id if root_task_id is not None else parent_task_id
        return cls(
            task_id=task_id,
            title=title,
            objective=objective,
            parent_task_id=parent_task_id,
            root_task_id=root_id,
            created_by=created_by,
            created_at=now,
            updated_at=now,
            risk_level=risk_level,
            state="draft",
        )

    def add_step(self, title: str, description: str = "",
                 estimated_duration_seconds: Optional[int] = None) -> PlannedStep:
        """Add a planned step with auto-assigned order."""
        order = len(self.steps)
        step = PlannedStep.create(
            title=title,
            description=description,
            order=order,
            estimated_duration_seconds=estimated_duration_seconds,
        )
        self.steps.append(step)
        self._touch()
        return step

    def add_file_change(self, path: str, change_type: Literal["create", "modify", "delete", "move"],
                        reason: str = "", new_path: Optional[str] = None) -> FileChange:
        """Add a file change."""
        change = FileChange(path=path, change_type=change_type, reason=reason, new_path=new_path)
        self.file_changes.append(change)
        self._touch()
        return change

    def add_acceptance_criterion(self, description: str) -> AcceptanceCriterion:
        """Add an acceptance criterion."""
        criterion = AcceptanceCriterion.create(description=description)
        self.acceptance_criteria.append(criterion)
        self._touch()
        return criterion

    def add_validation_result(self, target_id: str, target_type: Literal["criterion", "step", "task"],
                              passed: bool, message: str = "",
                              details: Optional[dict[str, Any]] = None) -> ValidationResult:
        """Add a validation result."""
        result = ValidationResult.create(target_id, target_type, passed, message, details)
        self.validation_results.append(result)
        self._touch()
        return result

    def set_final_review(self, reviewer: str, decision: Literal["approved", "rejected", "needs_revision"],
                         summary: str, notes: str = "") -> FinalReview:
        """Set the final review."""
        review = FinalReview(reviewer=reviewer, decision=decision, summary=summary, notes=notes)
        self.final_review = review
        self._touch()
        return review

    def transition_to(self, new_state: TaskState) -> None:
        """Transition to a new state with basic validation.

        This is a lightweight state machine — more complex transitions
        (with guards, hooks, etc.) will be added in the runtime plugin.
        """
        valid_transitions: dict[TaskState, set[TaskState]] = {
            "draft": {"planned", "cancelled"},
            "planned": {"awaiting_approval", "draft", "cancelled"},
            "awaiting_approval": {"approved", "planned", "cancelled"},
            "approved": {"running", "awaiting_approval", "cancelled"},
            "running": {"validation", "failed", "cancelled"},
            "validation": {"review", "running", "failed", "cancelled"},
            "review": {"completed", "validation", "failed", "cancelled"},
            "completed": set(),
            "failed": {"planned", "cancelled"},
            "cancelled": set(),
        }
        allowed = valid_transitions.get(self.state, set())
        if new_state not in allowed:
            raise ValueError(
                f"Invalid state transition: {self.state} → {new_state}. "
                f"Allowed from {self.state}: {sorted(allowed)}"
            )
        self.state = new_state
        self._touch()

    def _touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = _utc_now()

    # ─── Serialization ──────────────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict suitable for JSON."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "objective": self.objective,
            "parent_task_id": self.parent_task_id,
            "root_task_id": self.root_task_id,
            "created_by": self.created_by,
            "created_at": _serialize_utc(self.created_at),
            "updated_at": _serialize_utc(self.updated_at),
            "steps": [s.to_dict() for s in self.steps],
            "file_changes": [fc.to_dict() for fc in self.file_changes],
            "risk_level": self.risk_level,
            "acceptance_criteria": [ac.to_dict() for ac in self.acceptance_criteria],
            "validation_results": [vr.to_dict() for vr in self.validation_results],
            "final_review": self.final_review.to_dict() if self.final_review else None,
            "state": self.state,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GuidedTask":
        """Reconstruct from a dict (as produced by to_dict)."""
        task = cls(
            task_id=data["task_id"],
            title=data["title"],
            objective=data["objective"],
            parent_task_id=data.get("parent_task_id"),
            root_task_id=data.get("root_task_id"),
            created_by=data.get("created_by", "system"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            steps=[PlannedStep.from_dict(s) for s in data.get("steps", [])],
            file_changes=[FileChange.from_dict(fc) for fc in data.get("file_changes", [])],
            risk_level=data.get("risk_level", "moderate"),
            acceptance_criteria=[AcceptanceCriterion.from_dict(ac) for ac in data.get("acceptance_criteria", [])],
            validation_results=[ValidationResult.from_dict(vr) for vr in data.get("validation_results", [])],
            final_review=FinalReview.from_dict(data["final_review"]) if data.get("final_review") else None,
            state=data.get("state", "draft"),
            metadata=data.get("metadata", {}),
        )
        return task

    # ─── JSON Helpers ────────────────────────────────────────────────────────

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "GuidedTask":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))

    # ─── Lineage Helpers ────────────────────────────────────────────────────

    def is_root(self) -> bool:
        """Return True if this task has no parent."""
        return self.parent_task_id is None

    def lineage_ids(self) -> list[str]:
        """Return the chain of task IDs from root to this task based only on IDs
        stored in this object (no store lookup).

        Returns, in order, without duplicates:
        - root_task_id, when present;
        - parent_task_id, when present and different from root_task_id;
        - task_id (always last).
        """
        ids: list[str] = []
        seen: set[str] = set()

        if self.root_task_id and self.root_task_id not in seen:
            ids.append(self.root_task_id)
            seen.add(self.root_task_id)

        if self.parent_task_id and self.parent_task_id not in seen:
            ids.append(self.parent_task_id)
            seen.add(self.parent_task_id)

        if self.task_id not in seen:
            ids.append(self.task_id)
            seen.add(self.task_id)

        return ids


__all__ = [
    "TaskState",
    "RiskLevel",
    "PlannedStep",
    "FileChange",
    "AcceptanceCriterion",
    "ValidationResult",
    "FinalReview",
    "GuidedTask",
]