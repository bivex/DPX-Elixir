"""Elixir Protocol Polymorphism Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ProtocolPolymorphismRule(BasePatternRule):
    """Detects defprotocol and defimpl polymorphic dispatch contracts in Elixir."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROTOCOL_POLYMORPHISM

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if mod.is_protocol:
                evidences = [
                    Evidence(
                        description=f"Protocol '{mod.name}' defines extensible polymorphism contract via defprotocol",
                        weight=0.85,
                        rule_code="PROTOCOL_DEFINITION",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="protocol_definition",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

            elif mod.is_implementation:
                target_str = f" for {mod.for_type}" if mod.for_type else ""
                evidences = [
                    Evidence(
                        description=f"Implementation '{mod.name}' provides concrete protocol implementation{target_str}",
                        weight=0.85,
                        rule_code="PROTOCOL_IMPLEMENTATION",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="protocol_implementation",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
