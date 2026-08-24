"""Elixir Plug Middleware Pipeline Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PlugPipelineRule(BasePatternRule):
    """Detects Plug middleware pipelines in Elixir web applications."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PLUG_PIPELINE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "use Plug.Builder" in src or "use Plug.Router" in src or "plug :" in src or "@behaviour Plug" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' coordinates HTTP connection middleware processing pipeline (`Plug`)",
                        weight=0.85,
                        rule_code="PLUG_MIDDLEWARE_PIPELINE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="plug_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
