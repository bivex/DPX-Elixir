"""Tests for Elixir Domain Models and Value Objects."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel, ModuleModel, FunctionModel
from pattern_detector.domain.value_objects import (
    Confidence,
    ConfidenceLevel,
    Evidence,
    SourceLocation,
)


def test_confidence_calculation():
    evidences = [
        Evidence(description="Found GenServer behaviour", weight=0.8, rule_code="GEN_SERVER_USE"),
        Evidence(description="Implements handle_call", weight=0.5, rule_code="GEN_SERVER_CALL"),
    ]
    conf = Confidence.from_evidences(evidences)
    # Expected: 1.0 - (1 - 0.8) * (1 - 0.5) = 1.0 - (0.2 * 0.5) = 0.90
    assert abs(conf.score - 0.90) < 1e-4
    assert conf.level == ConfidenceLevel.VERY_HIGH
    assert conf.percentage_str == "90%"


def test_source_location_str():
    loc = SourceLocation(file_path="lib/my_app/worker.ex", line=42, column=5)
    assert str(loc) == "lib/my_app/worker.ex:42:5"


def test_circular_dependency_detection():
    model = CodeModel()

    mod_a = ModuleModel(name="ModuleA", file_path="lib/a.ex")
    fn_a = FunctionModel(name="call_b", arity=0, calls=[("ModuleB", "do_something", 0)])
    mod_a.functions["call_b/0"] = fn_a

    mod_b = ModuleModel(name="ModuleB", file_path="lib/b.ex")
    fn_b = FunctionModel(name="call_a", arity=0, calls=[("ModuleA", "do_something", 0)])
    mod_b.functions["call_a/0"] = fn_b

    model.modules["ModuleA"] = mod_a
    model.modules["ModuleB"] = mod_b

    cycles = model.find_circular_dependencies()
    assert len(cycles) == 1
    assert set(cycles[0]) == {"ModuleA", "ModuleB"}
