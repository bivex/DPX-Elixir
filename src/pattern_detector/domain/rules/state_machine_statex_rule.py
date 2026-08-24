"""Elixir State Machine (:gen_statem) Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StateMachineStatexRule(BasePatternRule):
    """Detects finite state machines in Elixir (@behaviour :gen_statem)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STATE_MACHINE_STATEX

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            if ":gen_statem" in mod.behaviours or "gen_statem" in mod.behaviours or mod.find_function("callback_mode"):
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' implements Finite State Machine behaviour (`@behaviour :gen_statem`)",
                        weight=0.85,
                        rule_code="GEN_STATEM_ELIXIR",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="state_machine_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
