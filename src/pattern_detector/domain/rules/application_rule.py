"""Elixir Application Lifecycle Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ApplicationRule(BasePatternRule):
    """Detects Elixir OTP Application entry point modules (`use Application`)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.APPLICATION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if "Application" in mod.uses or (mod.find_function("start", 2) and "Application" in mod.name):
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' coordinates top-level application startup lifecycle (`use Application`)",
                        weight=0.85,
                        rule_code="APPLICATION_OTP_STARTUP",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="application_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
