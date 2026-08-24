"""Elixir Tagged Tuple Command Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CommandTaggedTupleRule(BasePatternRule):
    """Detects Command Pattern via tagged tuple message pattern matching."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMMAND_TAGGED_TUPLE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            handle_call_fn = mod.find_function("handle_call", 3)
            if handle_call_fn and len(handle_call_fn.clauses) >= 2:
                evidences = [
                    Evidence(
                        description=f"Function handle_call/3 in '{mod.name}' pattern matches on {len(handle_call_fn.clauses)} distinct Command tagged tuples",
                        weight=0.75,
                        rule_code="COMMAND_TAGGED_TUPLE_DISPATCH",
                        location=handle_call_fn.location or mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=f"{mod.name}.handle_call/3",
                    target_kind="command_dispatcher",
                    evidences=evidences,
                    location=handle_call_fn.location or mod.location,
                )
                detections.append(det)

        return detections
