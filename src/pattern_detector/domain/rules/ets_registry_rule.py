"""Elixir Registry & ETS Shared Memory Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class EtsRegistryRule(BasePatternRule):
    """Detects Registry process lookup and :ets shared memory tables."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ETS_REGISTRY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "Registry.start_link" in src or "{:via, Registry" in src or ":ets.new(" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' utilizes Registry / :ets shared memory for zero-copy concurrent process lookup and caching",
                        weight=0.80,
                        rule_code="ETS_REGISTRY_LOOKUP",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="registry_ets_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
