"""Elixir Agent State Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AgentStateRule(BasePatternRule):
    """Detects Agent state holder processes in Elixir."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.AGENT_STATE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "use Agent" in src or "Agent.start_link" in src or "Agent.get_and_update" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' encapsulates state in an OTP Agent process (`use Agent`)",
                        weight=0.80,
                        rule_code="AGENT_STATE_MODULE",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="agent_state_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
