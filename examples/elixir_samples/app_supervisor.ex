defmodule Core.AppSupervisor do
  @moduledoc """
  Root Application Supervisor.
  """
  use Supervisor

  def start_link(init_arg) do
    Supervisor.start_link(__MODULE__, init_arg, name: __MODULE__)
  end

  @impl true
  def init(_init_arg) do
    children = [
      {Core.OrderServer, []},
      {DynamicSupervisor, strategy: :one_for_one, name: Core.DynamicWorkerSupervisor}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end
