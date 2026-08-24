"""Elixir Single Responsibility (God Module) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class LargeModuleSrpRule(BasePatternRule):
    """Detects God Modules in Elixir (excessive public functions ≥25)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LARGE_MODULE_SRP

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            public_fns = [fn for fn in mod.functions.values() if fn.is_public]
            total_fns = len(mod.functions)

            if len(public_fns) >= 25 or total_fns >= 35:
                evidences = [
                    Evidence(
                        description=f"SRP Violation (God Module): Module '{mod.name}' defines {len(public_fns)} public functions and {total_fns} routines, indicating multiple mixed domain responsibilities",
                        weight=0.85,
                        rule_code="SRP_GOD_MODULE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="god_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
