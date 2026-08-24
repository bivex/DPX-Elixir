"""High-performance Native Elixir AST & CST Parser Adapter implementing ParserPort."""

from __future__ import annotations

import os
import re
from pathlib import Path

from pattern_detector.domain.code_model import (
    CallbackModel,
    CodeModel,
    FunctionClauseModel,
    FunctionModel,
    ModuleModel,
    StructFieldModel,
    StructModel,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


class NativeElixirParserAdapter(ParserPort):
    """High-performance native Elixir parser supporting Elixir 1.14 - 1.18+ syntax."""

    def parse_sources(self, sources: dict[str, str]) -> CodeModel:
        model = CodeModel()
        for file_path, source_text in sources.items():
            modules = self.parse_file(file_path, source_text)
            for mod in modules:
                model.modules[mod.name] = mod
        return model

    def parse_file(self, file_path: str, source_text: str) -> list[ModuleModel]:
        clean_text = self._strip_comments(source_text)
        modules: list[ModuleModel] = []

        # Match defmodule, defprotocol, defimpl
        mod_pattern = re.compile(
            r"\b(defmodule|defprotocol|defimpl)\s+([a-zA-Z0-9_.]+)(?:,\s*for:\s*([a-zA-Z0-9_.]+))?\s+do\b",
            re.MULTILINE,
        )

        pos = 0
        while pos < len(clean_text):
            m = mod_pattern.search(clean_text, pos)
            if not m:
                break

            kind = m.group(1)
            raw_name = m.group(2)
            for_type = m.group(3) or ""
            name = f"{raw_name}.{for_type}" if kind == "defimpl" and for_type else raw_name
            line_no = clean_text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no, column=1)

            # Find matching 'end' for this 'do'
            body, end_pos = self._extract_do_end_block(clean_text, m.end())
            pos = end_pos + 1

            mod = ModuleModel(
                name=name,
                file_path=file_path,
                raw_source=body,
                is_protocol=(kind == "defprotocol"),
                is_implementation=(kind == "defimpl"),
                for_type=for_type,
                location=loc,
            )

            # 1. 'use' directives: use GenServer, use Supervisor
            mod.uses = self._parse_uses(body)

            # 2. '@behaviour' declarations
            mod.behaviours = self._parse_behaviours(body)

            # 3. '@callback' declarations
            mod.callbacks = self._parse_callbacks(body, file_path)

            # 4. 'defstruct'
            mod.struct = self._parse_struct(body, file_path)

            # 5. Functions & Macros
            mod.functions = self._parse_functions(body, file_path)

            modules.append(mod)

        # If file defines no explicit defmodule, treat as script / single module
        if not modules and clean_text.strip():
            fallback_name = Path(file_path).stem
            loc = SourceLocation(file_path=file_path, line=1, column=1)
            mod = ModuleModel(
                name=fallback_name,
                file_path=file_path,
                raw_source=clean_text,
                location=loc,
            )
            mod.uses = self._parse_uses(clean_text)
            mod.behaviours = self._parse_behaviours(clean_text)
            mod.callbacks = self._parse_callbacks(clean_text, file_path)
            mod.functions = self._parse_functions(clean_text, file_path)
            modules.append(mod)

        return modules

    # -------------------------------------------------------------------------
    # Parsing Helpers
    # -------------------------------------------------------------------------

    def _strip_comments(self, text: str) -> str:
        lines = []
        for line in text.splitlines():
            clean_line = re.sub(r"#(?=(?:[^\"\']*[\"\'][^\"\']*[\"\'])*[^\"\']*$).*", "", line)
            lines.append(clean_line)
        return "\n".join(lines)

    def _extract_do_end_block(self, text: str, start_pos: int) -> tuple[str, int]:
        depth = 1
        i = start_pos
        tokens = re.finditer(r"\b(do|fn|end)\b", text[start_pos:])

        for token in tokens:
            word = token.group(1)
            if word in ("do", "fn"):
                depth += 1
            elif word == "end":
                depth -= 1
                if depth == 0:
                    end_idx = start_pos + token.start()
                    return text[start_pos:end_idx], start_pos + token.end()

        return text[start_pos:], len(text)

    def _parse_uses(self, text: str) -> list[str]:
        uses = []
        for m in re.finditer(r"\buse\s+([a-zA-Z0-9_.]+)", text):
            uses.append(m.group(1))
        return uses

    def _parse_behaviours(self, text: str) -> list[str]:
        behaviours = []
        for m in re.finditer(r"@(?:behaviour|behavior)\s+([a-zA-Z0-9_.:]+)", text):
            behaviours.append(m.group(1))
        return behaviours

    def _parse_callbacks(self, text: str, file_path: str) -> dict[str, CallbackModel]:
        callbacks = {}
        pattern = re.compile(r"@callback\s+([a-zA-Z0-9_!?]+)\s*\(([^)]*)\)", re.MULTILINE)
        for m in pattern.finditer(text):
            cb_name = m.group(1)
            args_raw = m.group(2)
            arity = len(self._split_top_level_comma(args_raw))
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)
            callbacks[f"{cb_name}/{arity}"] = CallbackModel(name=cb_name, arity=arity, location=loc)
        return callbacks

    def _parse_struct(self, text: str, file_path: str) -> StructModel | None:
        m = re.search(r"\bdefstruct\s+(?:\[(.*?)\]|\%\{(.*?)\}|([a-zA-Z0-9_:, \t\n]+))", text, re.DOTALL)
        if m:
            fields_str = m.group(1) or m.group(2) or m.group(3) or ""
            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)
            fields = []
            for item in fields_str.split(","):
                item = item.strip().strip(":[]{}")
                if not item:
                    continue
                if ":" in item:
                    f_name = item.split(":")[0].strip()
                    fields.append(StructFieldModel(name=f_name))
                else:
                    fields.append(StructFieldModel(name=item))
            return StructModel(fields=fields, location=loc)
        return None

    def _split_top_level_comma(self, text: str) -> list[str]:
        if not text.strip():
            return []
        items = []
        current = []
        depth = 0
        in_string = False
        quote_char = ""
        escape = False

        for c in text:
            if escape:
                escape = False
                current.append(c)
                continue
            if c == "\\" and in_string:
                escape = True
                current.append(c)
                continue
            if c in ('"', "'") and not in_string:
                in_string = True
                quote_char = c
                current.append(c)
            elif c == quote_char and in_string:
                in_string = False
                current.append(c)
            elif not in_string:
                if c in ("(", "{", "[", "<"):
                    depth += 1
                    current.append(c)
                elif c in (")", "}", "]", ">"):
                    depth -= 1
                    current.append(c)
                elif c == "," and depth == 0:
                    items.append("".join(current).strip())
                    current = []
                else:
                    current.append(c)
            else:
                current.append(c)

        if current:
            items.append("".join(current).strip())
        return [it for it in items if it]

    def _parse_functions(self, text: str, file_path: str) -> dict[str, FunctionModel]:
        functions: dict[str, FunctionModel] = {}

        # Matches def, defp, defmacro, defmacrop
        fn_pattern = re.compile(
            r"\b(def|defp|defmacro|defmacrop)\s+([a-zA-Z0-9_!?]+)(?:\s*\(([\s\S]*?)\)|\s+([^\s,do\n]+))?(?:\s+when\s+([^\n,]+))?(?:,\s*do:\s*([^\n]+)|\s+do\b)",
            re.MULTILINE,
        )

        pos = 0
        while pos < len(text):
            m = fn_pattern.search(text, pos)
            if not m:
                break

            kind = m.group(1)
            name = m.group(2)
            args_raw = m.group(3) or m.group(4) or ""
            args_list = self._split_top_level_comma(args_raw)
            arity = len(args_list)
            guard = m.group(5) or ""
            one_liner_body = m.group(6)

            line_no = text[:m.start()].count("\n") + 1
            loc = SourceLocation(file_path=file_path, line=line_no)

            if one_liner_body is not None:
                body = one_liner_body
                pos = m.end()
            else:
                body, end_pos = self._extract_do_end_block(text, m.end())
                pos = end_pos + 1

            fn_id = f"{name}/{arity}"
            is_pub = kind in ("def", "defmacro")
            is_mac = kind in ("defmacro", "defmacrop")

            # Invocations: Module.func(
            call_matches = re.findall(r"\b([A-Z][a-zA-Z0-9_.]*)\.([a-zA-Z0-9_!?]+)\s*\(", body)
            calls = [(c[0], c[1], 0) for c in call_matches]

            has_with = "with " in body and "<-" in body
            has_pipe = "|>" in body
            has_rescue = "rescue " in body or "catch " in body
            has_spawn = "spawn(" in body or "spawn_link(" in body
            has_gen_call = "GenServer.call(" in body or "GenServer.cast(" in body
            complexity = 1 + body.count("case ") + body.count("cond ") + body.count("if ") + body.count("with ")

            clause = FunctionClauseModel(
                params=args_list,
                guard=guard,
                body=body,
                line=line_no,
            )

            if fn_id in functions:
                functions[fn_id].clauses.append(clause)
                functions[fn_id].cyclomatic_complexity += 1
                functions[fn_id].calls.extend(calls)
            else:
                functions[fn_id] = FunctionModel(
                    name=name,
                    arity=arity,
                    is_public=is_pub,
                    is_macro=is_mac,
                    clauses=[clause],
                    cyclomatic_complexity=complexity,
                    calls=calls,
                    has_with=has_with,
                    has_pipe=has_pipe,
                    has_rescue=has_rescue,
                    has_spawn=has_spawn,
                    has_gen_call=has_gen_call,
                    location=loc,
                )

        return functions
