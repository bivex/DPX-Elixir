"""Elixir Strategy Dynamic Dispatch Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StrategyDispatchRule(BasePatternRule):
    """Detects Strategy pattern dynamic module invocation (`apply/3` or `module.function(...)`)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STRATEGY_DISPATCH

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                body = fn.full_body
                if "apply(" in body or re.search(r"\b[a-z_][a-zA-Z0-9_]*_module\.[a-zA-Z0-9_]+\(", body) or re.search(r"\b[a-z_][a-zA-Z0-9_]*_adapter\.[a-zA-Z0-9_]+\(", body):
                    evidences = [
                        Evidence(
                            description=f"Function '{fn.id_str}' dynamically dispatches behavior to pluggable Strategy/Adapter modules",
                            weight=0.75,
                            rule_code="STRATEGY_DYNAMIC_DISPATCH",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}.{fn.id_str}",
                        target_kind="strategy_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
