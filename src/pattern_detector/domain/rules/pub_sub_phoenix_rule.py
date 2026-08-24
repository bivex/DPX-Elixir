"""Elixir Phoenix PubSub Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class PubSubPhoenixRule(BasePatternRule):
    """Detects Publish/Subscribe event broadcasting using Phoenix.PubSub."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PUB_SUB_PHOENIX

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "Phoenix.PubSub.broadcast" in src or "Phoenix.PubSub.subscribe" in src or "PubSub.broadcast" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' coordinates real-time distributed Publish/Subscribe topic broadcasting (Phoenix.PubSub)",
                        weight=0.85,
                        rule_code="PHOENIX_PUBSUB_BROADCAST",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="pubsub_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
