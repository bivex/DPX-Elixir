"""Pattern metadata, catalog definitions, and architectural descriptions for Elixir / OTP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternCatalogEntry:
    """Catalog entry describing an Elixir / OTP pattern, idiom, or rule."""

    pattern_type: PatternType
    category: PatternCategory
    name: str
    description: str
    idiomatic_example: str


PATTERN_CATALOG: Mapping[PatternType, PatternCatalogEntry] = {
    # OTP Behaviours
    PatternType.GEN_SERVER: PatternCatalogEntry(
        pattern_type=PatternType.GEN_SERVER,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="GenServer Actor",
        description="Encapsulates state, process mailbox, synchronous calls, and asynchronous casts via `use GenServer`.",
        idiomatic_example="defmodule MyServer do\n  use GenServer\n  def init(args), do: {:ok, %{}}\n  def handle_call(:get, _from, state), do: {:reply, state, state}\nend",
    ),
    PatternType.SUPERVISOR: PatternCatalogEntry(
        pattern_type=PatternType.SUPERVISOR,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="Supervisor Tree",
        description="Hierarchical supervisor managing process life cycles and failure containment strategies (`:one_for_one`, `:one_for_all`, `:rest_for_one`).",
        idiomatic_example="defmodule MySup do\n  use Supervisor\n  def init(_), do: Supervisor.init([MyWorker], strategy: :one_for_one)\nend",
    ),
    PatternType.DYNAMIC_SUPERVISOR: PatternCatalogEntry(
        pattern_type=PatternType.DYNAMIC_SUPERVISOR,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="DynamicSupervisor",
        description="Manages a dynamic pool of on-demand worker processes started at runtime via `DynamicSupervisor.start_child/2`.",
        idiomatic_example="defmodule MyDynamicSup do\n  use DynamicSupervisor\n  def init(_), do: DynamicSupervisor.init(strategy: :one_for_one)\nend",
    ),
    PatternType.AGENT_STATE: PatternCatalogEntry(
        pattern_type=PatternType.AGENT_STATE,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="Agent State Holder",
        description="Lightweight process wrapper around state via `use Agent` with functional get/update semantics.",
        idiomatic_example="Agent.start_link(fn -> %{} end, name: __MODULE__)\nAgent.get(__MODULE__, &Map.get(&1, :key))",
    ),
    PatternType.TASK_ASYNC: PatternCatalogEntry(
        pattern_type=PatternType.TASK_ASYNC,
        category=PatternCategory.ACTOR_CONCURRENCY,
        name="Task Concurrency & Async Streams",
        description="Asynchronous background computation or parallel stream processing via `Task.async/await` and `Task.Supervisor`.",
        idiomatic_example="Task.async_stream(collection, &compute/1, max_concurrency: 8)",
    ),
    PatternType.GEN_STAGE: PatternCatalogEntry(
        pattern_type=PatternType.GEN_STAGE,
        category=PatternCategory.ACTOR_CONCURRENCY,
        name="GenStage / Broadway Producer-Consumer",
        description="Backpressure-driven stream data processing pipeline with Producer, ProducerConsumer, and Consumer stages.",
        idiomatic_example="defmodule MyProducer do\n  use GenStage\n  def handle_demand(demand, state), do: {:noreply, events, state}\nend",
    ),
    PatternType.APPLICATION: PatternCatalogEntry(
        pattern_type=PatternType.APPLICATION,
        category=PatternCategory.OTP_BEHAVIOUR,
        name="OTP Application Lifecycle",
        description="Top-level Elixir application entry point starting root supervision trees via `use Application`.",
        idiomatic_example="defmodule MyApp.Application do\n  use Application\n  def start(_type, _args), do: Supervisor.start_link(children, opts)\nend",
    ),

    # Functional Idioms & Structural
    PatternType.PROTOCOL_POLYMORPHISM: PatternCatalogEntry(
        pattern_type=PatternType.PROTOCOL_POLYMORPHISM,
        category=PatternCategory.FUNCTIONAL_IDIOM,
        name="Protocol Polymorphism",
        description="Open dynamic dispatch polymorphism via `defprotocol` and `defimpl` without inheritance.",
        idiomatic_example="defprotocol Printable do\n  def print(data)\nend\ndefimpl Printable, for: User do\n  def print(user), do: user.name\nend",
    ),
    PatternType.MACRO_METAPROGRAMMING: PatternCatalogEntry(
        pattern_type=PatternType.MACRO_METAPROGRAMMING,
        category=PatternCategory.STRUCTURAL,
        name="Macro DSL Metaprogramming",
        description="Compile-time AST code transformation and domain-specific language generation via `defmacro`, `quote`, and `unquote`.",
        idiomatic_example="defmacro __using__(opts) do\n  quote do\n    import unquote(__MODULE__)\n  end\nend",
    ),
    PatternType.PIPELINE_OPERATOR: PatternCatalogEntry(
        pattern_type=PatternType.PIPELINE_OPERATOR,
        category=PatternCategory.FUNCTIONAL_IDIOM,
        name="Pipeline Operator Transformation",
        description="Idiomatic Elixir data flow chaining using `|>` to compose pure functions linearly.",
        idiomatic_example="data |> transform() |> validate() |> persist()",
    ),
    PatternType.PLUG_PIPELINE: PatternCatalogEntry(
        pattern_type=PatternType.PLUG_PIPELINE,
        category=PatternCategory.STRUCTURAL,
        name="Plug Middleware Pipeline",
        description="Web request/response composition pipeline using `use Plug.Builder` or `use Plug.Router`.",
        idiomatic_example="plug :authenticate\nplug :fetch_session\nplug :dispatch",
    ),
    PatternType.ETS_REGISTRY: PatternCatalogEntry(
        pattern_type=PatternType.ETS_REGISTRY,
        category=PatternCategory.STRUCTURAL,
        name="Registry & ETS Process Lookup",
        description="Decentralized or local process name lookup and shared memory storage via `Registry` and `:ets` tables.",
        idiomatic_example="{:via, Registry, {MyApp.Registry, user_id}}",
    ),
    PatternType.FACADE_CONTEXT: PatternCatalogEntry(
        pattern_type=PatternType.FACADE_CONTEXT,
        category=PatternCategory.STRUCTURAL,
        name="Phoenix Context Facade",
        description="High-level public boundary module encapsulating database queries, business rules, and internal structs.",
        idiomatic_example="defmodule MyApp.Accounts do\n  def get_user!(id), do: Repo.get!(User, id)\nend",
    ),
    PatternType.ADAPTER_BEHAVIOUR: PatternCatalogEntry(
        pattern_type=PatternType.ADAPTER_BEHAVIOUR,
        category=PatternCategory.STRUCTURAL,
        name="Adapter Behaviour Contract",
        description="Defines interchangeable driver adapters using `@callback` declarations and `@behaviour` implementations.",
        idiomatic_example="@callback deliver(email, config) :: {:ok, term()} | {:error, term()}",
    ),
    PatternType.DECORATOR_BODY: PatternCatalogEntry(
        pattern_type=PatternType.DECORATOR_BODY,
        category=PatternCategory.STRUCTURAL,
        name="Function Decorator Macro",
        description="Wraps function bodies with telemetry spans, logging, or caching using `@decorate` macros.",
        idiomatic_example="@decorate trace(\"user.create\")\ndef create_user(params), do: ...",
    ),

    # Behavioral & Concurrency
    PatternType.COMMAND_TAGGED_TUPLE: PatternCatalogEntry(
        pattern_type=PatternType.COMMAND_TAGGED_TUPLE,
        category=PatternCategory.BEHAVIORAL,
        name="Command Tagged Tuple",
        description="Dispatches operations as tagged tuples `{:action, payload}` pattern matched in function heads or GenServer callbacks.",
        idiomatic_example="def handle_call({:transfer_funds, from, to, amount}, _from, state) do ... end",
    ),
    PatternType.PUB_SUB_PHOENIX: PatternCatalogEntry(
        pattern_type=PatternType.PUB_SUB_PHOENIX,
        category=PatternCategory.ACTOR_CONCURRENCY,
        name="Phoenix PubSub Broadcasting",
        description="Cluster-wide or local real-time event broadcasting and subscription via `Phoenix.PubSub`.",
        idiomatic_example="Phoenix.PubSub.broadcast(MyApp.PubSub, \"room:1\", {:new_msg, msg})",
    ),
    PatternType.WITH_MONADIC_PIPELINE: PatternCatalogEntry(
        pattern_type=PatternType.WITH_MONADIC_PIPELINE,
        category=PatternCategory.BEHAVIORAL,
        name="Monadic Railway 'with' Pipeline",
        description="Sequential error-handling pipeline using `with {:ok, ...} <- ... else ... end`.",
        idiomatic_example="with {:ok, user} <- fetch_user(id), {:ok, token} <- generate_token(user) do\n  {:ok, token}\nend",
    ),
    PatternType.STRATEGY_DISPATCH: PatternCatalogEntry(
        pattern_type=PatternType.STRATEGY_DISPATCH,
        category=PatternCategory.BEHAVIORAL,
        name="Strategy Dynamic Dispatch",
        description="Dynamically selects and executes strategy modules via `apply(module, func, args)` or behavior callbacks.",
        idiomatic_example="strategy_module.process(payload)",
    ),
    PatternType.CIRCUIT_BREAKER_FUSE: PatternCatalogEntry(
        pattern_type=PatternType.CIRCUIT_BREAKER_FUSE,
        category=PatternCategory.RESILIENCE,
        name="Circuit Breaker Resilience",
        description="Protects cascading failure across distributed nodes using Fuse / Circuit Breakers.",
        idiomatic_example=":fuse.run(:api_fuse, fn -> call_remote_api() end)",
    ),
    PatternType.STATE_MACHINE_STATEX: PatternCatalogEntry(
        pattern_type=PatternType.STATE_MACHINE_STATEX,
        category=PatternCategory.BEHAVIORAL,
        name="Finite State Machine (:gen_statem)",
        description="State machine pattern implemented via `:gen_statem` or state machine DSLs.",
        idiomatic_example="@behaviour :gen_statem\ndef callback_mode, do: :state_functions",
    ),
    PatternType.MEMOIZATION_CACHE: PatternCatalogEntry(
        pattern_type=PatternType.MEMOIZATION_CACHE,
        category=PatternCategory.BEHAVIORAL,
        name="Memoization / Cache Store",
        description="Caches computed values via Cachex, ConCache, or persistent memory.",
        idiomatic_example="Cachex.fetch(:my_cache, key, fn -> compute_expensive_data() end)",
    ),

    # Resilience & Safety Audits
    PatternType.DEFENSIVE_RESCUE_SMELL: PatternCatalogEntry(
        pattern_type=PatternType.DEFENSIVE_RESCUE_SMELL,
        category=PatternCategory.SAFETY,
        name="Defensive Rescue / Catch-All Smell",
        description="Catching all exceptions (`rescue _ -> nil`) hiding state corruption rather than letting processes fail and restart.",
        idiomatic_example="Avoid blanket `rescue _ -> nil`; let unexpected exceptions crash the process to restart via Supervisor.",
    ),
    PatternType.UNBOUNDED_PROCESS_SPAWN: PatternCatalogEntry(
        pattern_type=PatternType.UNBOUNDED_PROCESS_SPAWN,
        category=PatternCategory.SAFETY,
        name="Unsupervised Process Spawn",
        description="Calling `spawn/1` or `spawn_link/1` directly outside a supervision tree (use `Task.Supervisor` instead).",
        idiomatic_example="Use `Task.Supervisor.async_nolink/2` instead of raw `spawn/1`.",
    ),
    PatternType.BLOCKING_GEN_SERVER_CALL: PatternCatalogEntry(
        pattern_type=PatternType.BLOCKING_GEN_SERVER_CALL,
        category=PatternCategory.SAFETY,
        name="Blocking GenServer Call",
        description="Performing long synchronous network/file I/O or `:timer.sleep` inside `handle_call/3` risking actor mailbox timeouts.",
        idiomatic_example="Delegate heavy work to a background Task or use `GenServer.reply/2`.",
    ),
    PatternType.STRING_TO_ATOM_VULNERABILITY: PatternCatalogEntry(
        pattern_type=PatternType.STRING_TO_ATOM_VULNERABILITY,
        category=PatternCategory.SAFETY,
        name="Dynamic String.to_atom Vulnerability",
        description="Calling `String.to_atom/1` on external/untrusted parameters risking BEAM VM atom table exhaustion.",
        idiomatic_example="Use `String.to_existing_atom/1` or string keys in Maps instead.",
    ),
    PatternType.LARGE_MODULE_SRP: PatternCatalogEntry(
        pattern_type=PatternType.LARGE_MODULE_SRP,
        category=PatternCategory.PRINCIPLE,
        name="Single Responsibility (God Module)",
        description="Large monolith module defining excessive public functions (≥25 functions) mixing multiple domains.",
        idiomatic_example="Decompose into focused Phoenix Contexts or domain sub-modules.",
    ),
    PatternType.CYCLOMATIC_COMPLEXITY_KISS: PatternCatalogEntry(
        pattern_type=PatternType.CYCLOMATIC_COMPLEXITY_KISS,
        category=PatternCategory.PRINCIPLE,
        name="Keep It Simple (KISS)",
        description="Function with excessive pattern matching clauses or complex conditional cascades (≥10 clauses).",
        idiomatic_example="Decompose complex multi-clause functions into helper routines.",
    ),
    PatternType.DUPLICATE_CODE_DRY: PatternCatalogEntry(
        pattern_type=PatternType.DUPLICATE_CODE_DRY,
        category=PatternCategory.PRINCIPLE,
        name="Don't Repeat Yourself (DRY)",
        description="Duplicated function implementations across modules.",
        idiomatic_example="Extract shared logic into a common helper or macro.",
    ),
    PatternType.CIRCULAR_MODULE_DEPENDENCY: PatternCatalogEntry(
        pattern_type=PatternType.CIRCULAR_MODULE_DEPENDENCY,
        category=PatternCategory.PRINCIPLE,
        name="Circular Module Dependency",
        description="Cyclic cross-module function calls (ModuleA -> ModuleB -> ModuleA).",
        idiomatic_example="Decouple modules using events, behaviours, or a mediator service.",
    ),
    PatternType.SUPERVISOR_RESTART_INTENSITY: PatternCatalogEntry(
        pattern_type=PatternType.SUPERVISOR_RESTART_INTENSITY,
        category=PatternCategory.RESILIENCE,
        name="Supervisor Restart Storm Risk",
        description="Supervisor configured with dangerously high restart intensity in short period risking cascading node shutdown.",
        idiomatic_example="Use balanced restart thresholds (e.g. `max_restarts: 3, max_seconds: 5`).",
    ),
    PatternType.MISSING_BEHAVIOUR_CALLBACKS: PatternCatalogEntry(
        pattern_type=PatternType.MISSING_BEHAVIOUR_CALLBACKS,
        category=PatternCategory.PRINCIPLE,
        name="Missing Behaviour Callbacks",
        description="Module declares `@behaviour Module` but is missing required callback implementations.",
        idiomatic_example="Implement all required `@callback` functions.",
    ),
}
