"""Elixir Railway Monadic 'with' Pipeline Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class WithMonadicPipelineRule(BasePatternRule):
    """Detects Railway Monadic error-handling pipeline chains (`with {:ok, ...} <- ...`)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.WITH_MONADIC_PIPELINE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                if "with " in fn.full_body and "<-" in fn.full_body:
                    arrow_count = fn.full_body.count("<-")
                    if arrow_count >= 2:
                        evidences = [
                            Evidence(
                                description=f"Function '{fn.id_str}' implements Railway-oriented Monadic pipeline with {arrow_count} sequential pattern matches (`with`)",
                                weight=0.80,
                                rule_code="WITH_RAILWAY_PIPELINE",
                                location=fn.location or mod.location,
                            )
                        ]
                        det = self._create_detection(
                            target_name=f"{mod.name}.{fn.id_str}",
                            target_kind="railway_pipeline_function",
                            evidences=evidences,
                            location=fn.location or mod.location,
                        )
                        detections.append(det)

        return detections
