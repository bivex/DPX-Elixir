"""Elixir Unbounded Process Spawn Rule."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class UnboundedProcessSpawnRule(BasePatternRule):
    """Detects raw unsupervised process spawning (spawn/1, spawn_link/1) without a Supervisor."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNBOUNDED_PROCESS_SPAWN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                body = fn.full_body
                if re.search(r"\bspawn(?:_link|_monitor)?\s*\(", body) and "Task.Supervisor" not in body:
                    evidences = [
                        Evidence(
                            description=f"Safety Audit (Unsupervised Process): Function '{fn.id_str}' in '{mod.name}' calls raw `spawn/spawn_link`; use `Task.Supervisor` for fault tolerance and supervision",
                            weight=0.80,
                            rule_code="UNSUPERVISED_PROCESS_SPAWN",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}.{fn.id_str}",
                        target_kind="unsupervised_spawn_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
