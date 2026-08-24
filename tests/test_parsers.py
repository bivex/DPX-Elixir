"""Tests for Native Elixir Parser Adapter."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_elixir_parser_adapter import NativeElixirParserAdapter


def test_parse_elixir_module():
    source = """
    defmodule MyApp.OrderServer do
      use GenServer
      @behaviour Plug

      defstruct [:id, :status, total: 0.0]

      @callback process_order(order :: map()) :: :ok

      def start_link(opts) do
        GenServer.start_link(__MODULE__, opts, name: __MODULE__)
      end

      def init(state) do
        {:ok, state}
      end

      def handle_call({:get_order, id}, _from, state) do
        {:reply, state, state}
      end
    end
    """
    parser = NativeElixirParserAdapter()
    model = parser.parse_sources({"lib/my_app/order_server.ex": source})

    assert "MyApp.OrderServer" in model.modules
    mod = model.modules["MyApp.OrderServer"]
    assert "GenServer" in mod.uses
    assert "Plug" in mod.behaviours
    assert mod.struct is not None
    assert len(mod.struct.fields) == 3
    assert "start_link/1" in mod.functions
    assert "handle_call/3" in mod.functions
    assert len(mod.callbacks) == 1


def test_parse_protocol_and_implementation():
    source = """
    defprotocol MyApp.Json do
      def to_json(data)
    end

    defimpl MyApp.Json, for: MyApp.User do
      def to_json(user) do
        Jason.encode!(user)
      end
    end
    """
    parser = NativeElixirParserAdapter()
    model = parser.parse_sources({"lib/my_app/json.ex": source})

    assert "MyApp.Json" in model.modules
    assert model.modules["MyApp.Json"].is_protocol is True

    impl_name = [m for m in model.modules.values() if m.is_implementation][0]
    assert impl_name.for_type == "MyApp.User"
