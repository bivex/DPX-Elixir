"""Tests for Scanning and Detection Services in DPX-Elixir."""

from __future__ import annotations

from pattern_detector.bootstrap.container import create_container


def test_scanning_service_memory():
    sources = {
        "lib/order_service.ex": """
        defmodule OrderService do
          use GenServer
          def init(args), do: {:ok, args}
          def handle_call(:status, _from, state), do: {:reply, state, state}
          def handle_cast(:reset, _state), do: {:noreply, %{}}
        end
        """
    }
    container = create_container()
    scanner = container.get_scanner()
    report = scanner.scan_sources(sources)

    assert report.scanned_files_count == 1
    assert report.total_detections_count >= 1
    assert any(d.pattern_type.value == "gen_server" for d in report.detections)
