defmodule Core.OrderServer do
  @moduledoc """
  Order processing stateful GenServer actor.
  """
  use GenServer
  @behaviour Plug

  defstruct [:id, :customer_id, :items, status: :pending, total: 0.0]

  @callback format_order(order :: map()) :: String.t()

  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    {:ok, %{orders: %{}, count: 0}}
  end

  @impl true
  def handle_call({:create_order, order_params}, _from, state) do
    order_id = "ord_#{state.count + 1}"
    order = %{id: order_id, params: order_params, status: :created}
    new_orders = Map.put(state.orders, order_id, order)
    {:reply, {:ok, order_id}, %{state | orders: new_orders, count: state.count + 1}}
  end

  @impl true
  def handle_call({:get_order, order_id}, _from, state) do
    case Map.get(state.orders, order_id) do
      nil -> {:reply, {:error, :not_found}, state}
      order -> {:reply, {:ok, order}, state}
    end
  end

  @impl true
  def handle_cast({:cancel_order, order_id}, state) do
    new_orders = Map.delete(state.orders, order_id)
    {:noreply, %{state | orders: new_orders}}
  end
end
