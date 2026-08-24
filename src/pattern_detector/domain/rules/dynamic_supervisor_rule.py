"""Elixir DynamicSupervisor Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DynamicSupervisorRule(BasePatternRule):
    """Detects DynamicSupervisor modules in Elixir."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DYNAMIC_SUPERVISOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "DynamicSupervisor" in mod.uses or "DynamicSupervisor.start_link" in mod.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' manages dynamic on-demand child processes (`use DynamicSupervisor`)",
                        weight=0.85,
                        rule_code="DYNAMIC_SUPERVISOR_MODULE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="dynamic_supervisor",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
