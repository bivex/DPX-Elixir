"""Elixir Adapter Behaviour Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AdapterBehaviourRule(BasePatternRule):
    """Detects Adapter behaviour contracts defining @callback functions."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ADAPTER_BEHAVIOUR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if mod.callbacks:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' defines interchangeable Adapter Behaviour contract with {len(mod.callbacks)} callback(s) ({', '.join(mod.callbacks.keys())})",
                        weight=0.80,
                        rule_code="ADAPTER_BEHAVIOUR_CALLBACKS",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="adapter_behaviour_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
