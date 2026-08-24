"""Elixir Supervisor Tree Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class SupervisorRule(BasePatternRule):
    """Detects OTP Supervisor trees in Elixir modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SUPERVISOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            evidences: list[Evidence] = []

            if "Supervisor" in mod.uses:
                evidences.append(
                    Evidence(
                        description=f"Module '{mod.name}' adopts OTP Supervisor behaviour (`use Supervisor`)",
                        weight=0.75,
                        rule_code="SUPERVISOR_USE_DECLARATION",
                        location=mod.location,
                    )
                )

            init_fn = mod.find_function("init", 1)
            if init_fn:
                body = init_fn.full_body
                if "Supervisor.init" in body or ":one_for_one" in body or ":one_for_all" in body or ":rest_for_one" in body:
                    strat = ":one_for_one"
                    for s in [":one_for_all", ":rest_for_one", ":one_for_one"]:
                        if s in body:
                            strat = s
                            break
                    evidences.append(
                        Evidence(
                            description=f"Defines supervisor child specifications and restart strategy '{strat}'",
                            weight=0.65,
                            rule_code="SUPERVISOR_INIT_STRATEGY",
                            location=init_fn.location or mod.location,
                        )
                    )

            if evidences:
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="supervisor_module",
                    evidences=evidences,
                    location=mod.location,
                )
                if det.confidence.score >= 0.50:
                    detections.append(det)

        return detections
