"""Elixir Function Decorator Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DecoratorBodyRule(BasePatternRule):
    """Detects function decorator macros (@decorate) in Elixir."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DECORATOR_BODY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "@decorate" in mod.raw_source or "use Decorator" in mod.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' applies transparent Aspect/Decorator wrappers around function execution (`@decorate`)",
                        weight=0.80,
                        rule_code="FUNCTION_DECORATOR_MACRO",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="decorator_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
