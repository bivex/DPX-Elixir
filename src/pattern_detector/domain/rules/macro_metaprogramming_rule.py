"""Elixir Macro DSL Metaprogramming Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class MacroMetaprogrammingRule(BasePatternRule):
    """Detects compile-time AST macros and DSL extensions (`defmacro`, `__using__`)."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MACRO_METAPROGRAMMING

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            macros = [fn for fn in mod.functions.values() if fn.is_macro]
            using_macro = mod.find_function("__using__")

            if macros or using_macro:
                desc = f"Module '{mod.name}' defines {len(macros)} compile-time macro(s) for DSL metaprogramming"
                if using_macro:
                    desc += " and provides `__using__/1` macro injection"

                evidences = [
                    Evidence(
                        description=desc,
                        weight=0.80,
                        rule_code="MACRO_DSL_DEFINITION",
                        location=mod.location,
                    )
                ]
                det = self._create_detection(
                    target_name=mod.name,
                    target_kind="macro_module",
                    evidences=evidences,
                    location=mod.location,
                )
                detections.append(det)

        return detections
