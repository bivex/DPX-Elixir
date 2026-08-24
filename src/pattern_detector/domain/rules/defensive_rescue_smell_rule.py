"""Elixir Defensive Rescue Smell Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DefensiveRescueSmellRule(BasePatternRule):
    """Detects defensive rescue _ -> nil violating Elixir's Let-It-Crash philosophy."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DEFENSIVE_RESCUE_SMELL

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                if re.search(r"rescue\s+(_\s*->\s*(?:nil|:ok|false|%\{\}|\[\])|_e\s*->\s*(?:nil|:ok|false))", fn.full_body):
                    evidences = [
                        Evidence(
                            description=f"Let-It-Crash Violation: Function '{fn.id_str}' in '{mod.name}' defensively swallows errors (`rescue _ -> nil`); let processes fail fast and restart cleanly via Supervisor",
                            weight=0.85,
                            rule_code="DEFENSIVE_RESCUE_SWALLOW",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}.{fn.id_str}",
                        target_kind="defensive_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
