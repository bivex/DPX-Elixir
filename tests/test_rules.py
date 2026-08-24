"""Tests for Elixir Design Pattern and Safety Rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_elixir_parser_adapter import NativeElixirParserAdapter
from pattern_detector.domain.rules.defensive_rescue_smell_rule import DefensiveRescueSmellRule
from pattern_detector.domain.rules.gen_server_rule import GenServerRule
from pattern_detector.domain.rules.pipeline_operator_rule import PipelineOperatorRule
from pattern_detector.domain.rules.string_to_atom_vulnerability_rule import StringToAtomVulnerabilityRule
from pattern_detector.domain.rules.supervisor_rule import SupervisorRule
from pattern_detector.domain.rules.with_monadic_pipeline_rule import WithMonadicPipelineRule


def test_detect_gen_server_and_supervisor():
    sources = {
        "lib/worker.ex": """
        defmodule Worker do
          use GenServer
          def init(args), do: {:ok, args}
          def handle_call(:get, _from, state), do: {:reply, state, state}
          def handle_cast({:set, val}, state), do: {:noreply, val}
        end
        """,
        "lib/supervisor.ex": """
        defmodule MySupervisor do
          use Supervisor
          def init(_) do
            Supervisor.init([Worker], strategy: :one_for_one)
          end
        end
        """,
    }
    parser = NativeElixirParserAdapter()
    model = parser.parse_sources(sources)

    gs_dets = GenServerRule().detect(model)
    assert len(gs_dets) == 1
    assert gs_dets[0].target_name == "Worker"

    sup_dets = SupervisorRule().detect(model)
    assert len(sup_dets) == 1
    assert sup_dets[0].target_name == "MySupervisor"


def test_detect_pipelines_and_safety_smells():
    source = """
    defmodule PipelineExample do
      def process(data) do
        data
        |> parse()
        |> validate()
        |> transform()
        |> persist()
      end

      def railway(user_id) do
        with {:ok, user} <- find_user(user_id),
             {:ok, token} <- generate_token(user) do
          {:ok, token}
        end
      end

      def bad_func(input) do
        atom = String.to_atom(input)
        try do
          do_work(atom)
        rescue
          _ -> nil
        end
      end
    end
    """
    parser = NativeElixirParserAdapter()
    model = parser.parse_sources({"lib/example.ex": source})

    pipes = PipelineOperatorRule().detect(model)
    assert len(pipes) == 1

    railways = WithMonadicPipelineRule().detect(model)
    assert len(railways) == 1

    rescues = DefensiveRescueSmellRule().detect(model)
    assert len(rescues) == 1

    atoms = StringToAtomVulnerabilityRule().detect(model)
    assert len(atoms) == 1
