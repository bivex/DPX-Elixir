"""Elixir Task Concurrency & Async Stream Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class TaskAsyncRule(BasePatternRule):
    """Detects Task concurrency and Task.async_stream parallel processing."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TASK_ASYNC

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            for fn in mod.functions.values():
                body = fn.full_body
                if "Task.async_stream" in body or "Task.async(" in body or "Task.Supervisor.async" in body:
                    evidences = [
                        Evidence(
                            description=f"Function '{fn.id_str}' coordinates asynchronous parallel tasks / streams via Task module",
                            weight=0.80,
                            rule_code="TASK_ASYNC_CONCURRENCY",
                            location=fn.location or mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=f"{mod.name}.{fn.id_str}",
                        target_kind="task_async_function",
                        evidences=evidences,
                        location=fn.location or mod.location,
                    )
                    detections.append(det)

        return detections
