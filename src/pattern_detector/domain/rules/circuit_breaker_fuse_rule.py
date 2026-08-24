"""Elixir Circuit Breaker Pattern Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class CircuitBreakerFuseRule(BasePatternRule):
    """Detects Circuit Breaker fault-tolerance patterns in Elixir."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CIRCUIT_BREAKER_FUSE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if ":fuse.run" in src or "Fuse.run" in src or "CircuitBreaker" in mod.name:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' incorporates Circuit Breaker fault-tolerance protection against downstream failures",
                        weight=0.85,
                        rule_code="CIRCUIT_BREAKER_RESILIENCE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="circuit_breaker_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
