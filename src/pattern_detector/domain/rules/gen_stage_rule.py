"""Elixir GenStage / Broadway Producer-Consumer Pipeline Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GenStageRule(BasePatternRule):
    """Detects GenStage / Broadway data pipeline stages with backpressure."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GEN_STAGE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "use GenStage" in src or "use Broadway" in src or mod.find_function("handle_demand", 2):
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' implements backpressure-driven data processing pipeline (GenStage / Broadway)",
                        weight=0.85,
                        rule_code="GEN_STAGE_BROADWAY_PIPELINE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="gen_stage_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
