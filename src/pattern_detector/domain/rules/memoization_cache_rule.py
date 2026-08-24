"""Elixir Memoization Cache Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MemoizationCacheRule(BasePatternRule):
    """Detects Cachex, ConCache, or memoization caching layers."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MEMOIZATION_CACHE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            src = mod.raw_source
            if "Cachex.fetch" in src or "Cachex.get" in src or "ConCache.get" in src:
                evidences = [
                    Evidence(
                        description=f"Module '{mod.name}' integrates memoization / caching layer (Cachex / ConCache) to prevent redundant computations",
                        weight=0.80,
                        rule_code="MEMOIZATION_CACHE_LAYER",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="cache_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
