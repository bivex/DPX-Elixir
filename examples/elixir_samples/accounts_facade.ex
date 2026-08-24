defmodule Core.Accounts do
  @moduledoc """
  Phoenix Context Facade boundary for user account management.
  """

  def get_user!(id), do: %{id: id, name: "Alice"}
  def list_users, do: [%{id: 1}, %{id: 2}]
  def create_user(attrs), do: {:ok, attrs}
  def update_user(user, attrs), do: {:ok, Map.merge(user, attrs)}
  def delete_user(user), do: {:ok, user}
  def change_user(user), do: {:ok, user}
end
