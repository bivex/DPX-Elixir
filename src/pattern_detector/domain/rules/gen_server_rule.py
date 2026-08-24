"""Elixir GenServer Actor Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GenServerRule(BasePatternRule):
    """Detects OTP GenServer actors in Elixir modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GEN_SERVER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            evidences: list[Evidence] = []

            if "GenServer" in mod.uses:
                evidences.append(
                    Evidence(
                        description=f"Module '{mod.name}' explicitly adopts OTP GenServer actor behaviour (`use GenServer`)",
                        weight=0.75,
                        rule_code="GEN_SERVER_USE_DECLARATION",
                        location=mod.location,
                    )
                )

            callbacks_found = []
            for cb_name, arity in [("init", 1), ("handle_call", 3), ("handle_cast", 2), ("handle_info", 2), ("handle_continue", 2), ("terminate", 2)]:
                if mod.find_function(cb_name, arity):
                    callbacks_found.append(f"{cb_name}/{arity}")

            if len(callbacks_found) >= 2:
                evidences.append(
                    Evidence(
                        description=f"Implements {len(callbacks_found)} core GenServer callback(s) ({', '.join(callbacks_found)})",
                        weight=0.60,
                        rule_code="GEN_SERVER_CALLBACKS",
                        location=mod.location,
                    )
                )

            start_link_fn = mod.find_function("start_link")
            if start_link_fn:
                evidences.append(
                    Evidence(
                        description=f"Provides canonical starter function '{start_link_fn.id_str}'",
                        weight=0.40,
                        rule_code="GEN_SERVER_START_LINK",
                        location=start_link_fn.location or mod.location,
                    )
                )

            if evidences:
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="genserver_module",
                    evidences=evidences,
                    location=mod.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
