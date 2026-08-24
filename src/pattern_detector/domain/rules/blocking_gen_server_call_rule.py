"""Elixir Blocking GenServer Call Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BlockingGenServerCallRule(BasePatternRule):
    """Detects blocking I/O or sleep inside handle_call/3."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BLOCKING_GEN_SERVER_CALL

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            handle_call_fn = mod.find_function("handle_call", 3)
            if handle_call_fn:
                body = handle_call_fn.full_body
                if ":timer.sleep(" in body or "Process.sleep(" in body or "HTTPoison." in body or "Req.get!(" in body or "File.read!(" in body:
                    evidences = [
                        Evidence(
                            description=f"Safety Audit (Blocked Actor): Function handle_call/3 in '{mod.name}' performs blocking I/O / sleep; delegate work asynchronously to prevent actor mailbox timeouts",
                            weight=0.85,
                            rule_code="BLOCKED_GEN_SERVER_HANDLE_CALL",
                            location=handle_call_fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}.handle_call/3",
                        target_kind="blocked_handle_call",
                        evidences=evidences,
                        location=handle_call_fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
