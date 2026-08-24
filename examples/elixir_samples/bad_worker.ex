defmodule Core.BadWorker do
  @moduledoc """
  Anti-patterns module demonstrating Let-It-Crash violations and atom vulnerabilities.
  """

  def unsafe_handler(dynamic_string) do
    # Atom table exhaustion vulnerability
    action_atom = String.to_atom(dynamic_string)

    # Unsupervised process spawn
    spawn(fn ->
      do_heavy_work(action_atom)
    end)
  end

  def defensive_rescue_antipattern(param) do
    try do
      parse_param(param)
    rescue
      _ -> nil
    end
  end

  defp do_heavy_work(_atom), do: :ok
  defp parse_param(_p), do: :ok
end
