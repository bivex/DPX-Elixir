"""Domain Code Model for Elixir / OTP Static Architecture and Pattern Analysis."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Sequence

from pattern_detector.domain.value_objects import SourceLocation


@dataclass
class FunctionClauseModel:
    """Represents a single pattern-matching clause of an Elixir function."""

    params: list[str] = field(default_factory=list)
    guard: str = ""
    body: str = ""
    line: int = 1


@dataclass
class FunctionModel:
    """Represents an Elixir function definition (`def`, `defp`, `defmacro`, `defmacrop`)."""

    name: str
    arity: int
    is_public: bool = True
    is_macro: bool = False
    clauses: list[FunctionClauseModel] = field(default_factory=list)
    doc: str = ""
    cyclomatic_complexity: int = 1
    calls: list[tuple[str, str, int]] = field(default_factory=list)  # [(module, func, arity), ...]
    has_with: bool = False
    has_pipe: bool = False
    has_rescue: bool = False
    has_spawn: bool = False
    has_gen_call: bool = False
    location: SourceLocation | None = None

    @property
    def id_str(self) -> str:
        return f"{self.name}/{self.arity}"

    @property
    def full_body(self) -> str:
        return "\n".join(c.body for c in self.clauses)


@dataclass
class StructFieldModel:
    """Represents a field in an Elixir struct (`defstruct [...]`)."""

    name: str
    default_val: str = ""


@dataclass
class StructModel:
    """Represents an Elixir struct definition in a module."""

    fields: list[StructFieldModel] = field(default_factory=list)
    location: SourceLocation | None = None


@dataclass
class CallbackModel:
    """Represents an Elixir behaviour callback definition (`@callback ...`)."""

    name: str
    arity: int
    spec_str: str = ""
    location: SourceLocation | None = None


@dataclass
class ModuleModel:
    """Represents an Elixir module (`defmodule Name do ... end`)."""

    name: str
    file_path: str
    uses: list[str] = field(default_factory=list)  # e.g. ["GenServer", "Supervisor", "Plug.Builder"]
    behaviours: list[str] = field(default_factory=list)  # e.g. ["Plug", ":gen_statem"]
    aliases: dict[str, str] = field(default_factory=dict)
    imports: list[str] = field(default_factory=list)
    struct: StructModel | None = None
    callbacks: dict[str, CallbackModel] = field(default_factory=dict)
    functions: dict[str, FunctionModel] = field(default_factory=dict)  # "name/arity" -> FunctionModel
    is_protocol: bool = False
    is_implementation: bool = False
    for_type: str = ""  # For defimpl Protocol, for: Type
    raw_source: str = ""
    location: SourceLocation | None = None

    def find_function(self, name: str, arity: int | None = None) -> FunctionModel | None:
        if arity is not None:
            return self.functions.get(f"{name}/{arity}")
        for fn_id, fn in self.functions.items():
            if fn.name == name:
                return fn
        return None

    def has_public_function(self, name: str, arity: int | None = None) -> bool:
        fn = self.find_function(name, arity)
        return fn is not None and fn.is_public


@dataclass
class CodeModel:
    """Aggregated semantic domain model of an Elixir codebase or application."""

    modules: dict[str, ModuleModel] = field(default_factory=dict)
    project_path: str = ""

    def all_modules(self) -> list[ModuleModel]:
        return list(self.modules.values())

    def all_functions(self) -> list[FunctionModel]:
        res = []
        for m in self.modules.values():
            res.extend(m.functions.values())
        return res

    def find_module(self, name: str) -> ModuleModel | None:
        return self.modules.get(name)

    # -------------------------------------------------------------------------
    # Cross-Module Dependency Graph
    # -------------------------------------------------------------------------

    def build_module_dependency_graph(self) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = {mod_name: set() for mod_name in self.modules}

        for mod_name, mod in self.modules.items():
            for fn in mod.functions.values():
                for call_mod, call_fn, _ in fn.calls:
                    if call_mod and call_mod in self.modules and call_mod != mod_name:
                        graph[mod_name].add(call_mod)

        return graph

    def find_circular_dependencies(self, max_depth: int = 8, max_cycles: int = 50) -> list[list[str]]:
        graph = self.build_module_dependency_graph()
        cycles: list[list[str]] = []
        visited: set[str] = set()

        def _dfs(current: str, path: list[str], path_set: set[str]) -> None:
            if len(cycles) >= max_cycles:
                return
            path.append(current)
            path_set.add(current)

            for neighbor in sorted(graph.get(current, set())):
                if neighbor == path[0] and len(path) > 1:
                    canonical = tuple(path)
                    rotations = [canonical[i:] + canonical[:i] for i in range(len(canonical))]
                    min_rot = list(min(rotations))
                    if min_rot not in cycles:
                        cycles.append(min_rot)
                elif neighbor not in path_set and neighbor not in visited and len(path) < max_depth:
                    _dfs(neighbor, path, path_set)

            path.pop()
            path_set.remove(current)

        for node in sorted(graph.keys()):
            _dfs(node, [], set())
            visited.add(node)

        return cycles
