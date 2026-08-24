"""Domain value objects for the Elixir/OTP Pattern Detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(str, Enum):
    """Broad classification of Elixir design patterns, OTP behaviours, idioms, and safety rules."""

    OTP_BEHAVIOUR = "otp_behaviour"
    ACTOR_CONCURRENCY = "actor_concurrency"
    FUNCTIONAL_IDIOM = "functional_idiom"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    RESILIENCE = "resilience"
    PRINCIPLE = "principle"
    SAFETY = "safety"


class PatternType(str, Enum):
    """Specific Elixir/OTP design pattern, behaviour, and architecture smell identifiers."""

    # OTP Behaviours
    GEN_SERVER = "gen_server"
    SUPERVISOR = "supervisor"
    DYNAMIC_SUPERVISOR = "dynamic_supervisor"
    AGENT_STATE = "agent_state"
    TASK_ASYNC = "task_async"
    GEN_STAGE = "gen_stage"
    APPLICATION = "application"

    # Functional Idioms & Structural
    PROTOCOL_POLYMORPHISM = "protocol_polymorphism"
    MACRO_METAPROGRAMMING = "macro_metaprogramming"
    PIPELINE_OPERATOR = "pipeline_operator"
    PLUG_PIPELINE = "plug_pipeline"
    ETS_REGISTRY = "ets_registry"
    FACADE_CONTEXT = "facade_context"
    ADAPTER_BEHAVIOUR = "adapter_behaviour"
    DECORATOR_BODY = "decorator_body"

    # Behavioral & Concurrency
    COMMAND_TAGGED_TUPLE = "command_tagged_tuple"
    PUB_SUB_PHOENIX = "pub_sub_phoenix"
    WITH_MONADIC_PIPELINE = "with_monadic_pipeline"
    STRATEGY_DISPATCH = "strategy_dispatch"
    CIRCUIT_BREAKER_FUSE = "circuit_breaker_fuse"
    STATE_MACHINE_STATEX = "state_machine_statex"
    MEMOIZATION_CACHE = "memoization_cache"

    # Resilience, SOLID & Safety Audits
    DEFENSIVE_RESCUE_SMELL = "defensive_rescue_smell"
    UNBOUNDED_PROCESS_SPAWN = "unbounded_process_spawn"
    BLOCKING_GEN_SERVER_CALL = "blocking_gen_server_call"
    STRING_TO_ATOM_VULNERABILITY = "string_to_atom_vulnerability"
    LARGE_MODULE_SRP = "large_module_srp"
    CYCLOMATIC_COMPLEXITY_KISS = "cyclomatic_complexity_kiss"
    DUPLICATE_CODE_DRY = "duplicate_code_dry"
    CIRCULAR_MODULE_DEPENDENCY = "circular_module_dependency"
    SUPERVISOR_RESTART_INTENSITY = "supervisor_restart_intensity"
    MISSING_BEHAVIOUR_CALLBACKS = "missing_behaviour_callbacks"


class ConfidenceLevel(str, Enum):
    """Categorical confidence rating for a pattern detection."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

    @classmethod
    def from_score(cls, score: float) -> ConfidenceLevel:
        if score >= 0.85:
            return cls.VERY_HIGH
        if score >= 0.70:
            return cls.HIGH
        if score >= 0.50:
            return cls.MEDIUM
        return cls.LOW


@dataclass(frozen=True)
class SourceLocation:
    """Represents a precise location in an Elixir source code file (.ex / .exs)."""

    file_path: str
    line: int = 1
    column: int = 1
    end_line: int | None = None
    end_column: int | None = None

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column}"


@dataclass(frozen=True)
class Evidence:
    """A single piece of heuristic evidence supporting a pattern detection."""

    description: str
    weight: float
    rule_code: str
    location: SourceLocation | None = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Evidence weight must be between 0.0 and 1.0, got {self.weight}")


@dataclass(frozen=True)
class Confidence:
    """Aggregated confidence score computed from multiple pieces of evidence."""

    score: float
    level: ConfidenceLevel = field(init=False)

    def __post_init__(self) -> None:
        clamped = max(0.0, min(1.0, self.score))
        object.__setattr__(self, "score", clamped)
        object.__setattr__(self, "level", ConfidenceLevel.from_score(clamped))

    @classmethod
    def from_evidences(cls, evidences: list[Evidence]) -> Confidence:
        if not evidences:
            return cls(0.0)
        complement_product = 1.0
        for ev in evidences:
            complement_product *= (1.0 - ev.weight)
        return cls(1.0 - complement_product)

    @property
    def percentage_str(self) -> str:
        return f"{int(self.score * 100)}%"
