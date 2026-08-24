"""Elixir Phoenix Context Facade Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class FacadeContextRule(BasePatternRule):
    """Detects Phoenix Context boundary facade modules."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACADE_CONTEXT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for mod in model.all_modules():
            # Domain Contexts (e.g. MyApp.Accounts, MyApp.Catalog) without GenServer
            if not mod.uses and not mod.behaviours:
                public_fns = [fn for fn in mod.functions.values() if fn.is_public]
                crud_names = [fn.name for fn in public_fns if any(fn.name.startswith(p) for p in ("get_", "list_", "create_", "update_", "delete_", "change_"))]
                if len(crud_names) >= 4:
                    evidences = [
                        Evidence(
                            description=f"Module '{mod.name}' serves as a Phoenix Context Facade encapsulating business operations ({', '.join(crud_names[:4])})",
                            weight=0.80,
                            rule_code="PHOENIX_CONTEXT_FACADE",
                            location=mod.location,
                        )
                    ]
                    det = self._create_detection(
                        target_name=mod.name,
                        target_kind="context_facade_module",
                        evidences=evidences,
                        location=mod.location,
                    )
                    detections.append(det)

        return detections
