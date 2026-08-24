# 💧 DPX-Elixir: Hexagonal Architecture & Design Pattern Detector for Elixir / OTP

<p align="center">
  <img src="https://img.shields.io/badge/Language-Elixir%201.14--1.18%2B-blueviolet.svg?style=for-the-badge&logo=elixir" alt="Elixir" />
  <img src="https://img.shields.io/badge/OTP-25--27%2B-purple.svg?style=for-the-badge&logo=erlang" alt="OTP" />
  <img src="https://img.shields.io/badge/Architecture-Hexagonal%20Ports%20%26%20Adapters-blue.svg?style=for-the-badge" alt="Hexagonal" />
  <img src="https://img.shields.io/badge/Rules-30%20Patterns-success.svg?style=for-the-badge" alt="Rules" />
  <img src="https://img.shields.io/badge/Output-SARIF%20%7C%20HTML%20%7C%20JSON%20%7C%20Markdown-orange.svg?style=for-the-badge" alt="Outputs" />
</p>

---

## 📖 Overview

**DPX-Elixir** is a static analysis and software design pattern detection engine designed for **Elixir and OTP applications** (Elixir 1.14 - 1.18+ / OTP 25 - 27+).

Built on **Hexagonal Architecture (Ports and Adapters)** and **Domain-Driven Design (DDD)** principles, DPX-Elixir identifies OTP behaviours, actor concurrency models, functional pipelines, metaprogramming macros, and resilience / safety anti-patterns (`Let-It-Crash`, `String.to_atom` vulnerabilities, unsupervised process spawns, and blocking GenServer calls).

---

## 🔷 Catalog of 30 Supported Elixir / OTP Patterns & Rules

| Category | Pattern / Rule | Rule Code | Description |
|---|---|---|---|
| **OTP Behaviours** | **GenServer Actor** | `GEN_SERVER` | State encapsulation, process mailboxes, synchronous calls & asynchronous casts (`use GenServer`). |
| **OTP Behaviours** | **Supervisor Tree** | `SUPERVISOR` | Process lifecycle containment and restart strategies (`:one_for_one`, `:one_for_all`, `:rest_for_one`). |
| **OTP Behaviours** | **DynamicSupervisor** | `DYNAMIC_SUPERVISOR` | Dynamic on-demand child worker process management (`use DynamicSupervisor`). |
| **OTP Behaviours** | **Agent State Holder** | `AGENT_STATE` | Functional state encapsulation via `use Agent` / `Agent.start_link`. |
| **OTP Behaviours** | **Task & Async Streams** | `TASK_ASYNC` | Asynchronous task computation and parallel data processing (`Task.async_stream`). |
| **OTP Behaviours** | **GenStage / Broadway** | `GEN_STAGE` | Backpressure stream data processing pipelines (Producer, Consumer). |
| **OTP Behaviours** | **Application Lifecycle** | `APPLICATION` | Top-level OTP application startup trees (`use Application`). |
| **Functional Idioms** | **Protocol Polymorphism** | `PROTOCOL_POLYMORPHISM` | Open dynamic polymorphism dispatch without inheritance (`defprotocol`, `defimpl`). |
| **Functional Idioms** | **Pipeline Operator** | `PIPELINE_OPERATOR` | Multi-stage functional data transformations chained via `|>`. |
| **Structural** | **Macro DSL Metaprogramming** | `MACRO_METAPROGRAMMING` | Compile-time AST transformation macros (`defmacro`, `quote`, `unquote`, `__using__`). |
| **Structural** | **Plug Middleware Pipeline** | `PLUG_PIPELINE` | Web connection pipelines (`use Plug.Builder`, `use Plug.Router`). |
| **Structural** | **Registry & ETS Lookup** | `ETS_REGISTRY` | Decentralized process lookup and shared ETS memory tables (`{:via, Registry, ...}`). |
| **Structural** | **Phoenix Context Facade** | `FACADE_CONTEXT` | Domain boundary facade encapsulating database queries and structs. |
| **Structural** | **Adapter Behaviour** | `ADAPTER_BEHAVIOUR` | Interchangeable driver adapters using `@callback` declarations. |
| **Structural** | **Function Decorator** | `DECORATOR_BODY` | Aspect-oriented function execution wrappers (`@decorate`). |
| **Behavioral** | **Command Tagged Tuple** | `COMMAND_TAGGED_TUPLE` | Tagged message dispatch tuples `{:action, payload}` in function heads / `handle_call`. |
| **Behavioral** | **Phoenix PubSub** | `PUB_SUB_PHOENIX` | Real-time cluster-wide topic event broadcasting (`Phoenix.PubSub.broadcast/3`). |
| **Behavioral** | **Monadic Railway 'with'** | `WITH_MONADIC_PIPELINE` | Railway-oriented error handling pipeline chains (`with {:ok, ...} <- ...`). |
| **Behavioral** | **Strategy Dispatch** | `STRATEGY_DISPATCH` | Dynamic strategy dispatch (`apply/3` or module delegation). |
| **Behavioral** | **Circuit Breaker** | `CIRCUIT_BREAKER_FUSE` | Fault-tolerance protection across downstream microservices (`:fuse.run`). |
| **Behavioral** | **Finite State Machine** | `STATE_MACHINE_STATEX` | State machine pattern via `:gen_statem`. |
| **Behavioral** | **Memoization Cache** | `MEMOIZATION_CACHE` | Value memoization via Cachex / ConCache. |
| **Safety & Let-It-Crash** | **Defensive Rescue Smell** | `DEFENSIVE_RESCUE_SMELL` | Swallowing errors (`rescue _ -> nil`) violating Let-It-Crash. |
| **Safety & Let-It-Crash** | **Unsupervised Process Spawn** | `UNBOUNDED_PROCESS_SPAWN` | Calling `spawn/1` outside a supervised tree (use `Task.Supervisor`). |
| **Safety & Let-It-Crash** | **Blocking GenServer Call** | `BLOCKING_GEN_SERVER_CALL` | Long I/O or sleep inside `handle_call/3` causing actor mailbox timeouts. |
| **Safety & Let-It-Crash** | **Dynamic String.to_atom** | `STRING_TO_ATOM_VULNERABILITY` | Calling `String.to_atom/1` on dynamic input risking atom table exhaustion (DoS). |
| **Quality & Principles** | **God Module (SRP)** | `LARGE_MODULE_SRP` | Modules defining excessive public functions (≥25 public defs). |
| **Quality & Principles** | **High Complexity (KISS)** | `CYCLOMATIC_COMPLEXITY_KISS` | Excessive pattern-matching clauses or branches (≥10 clauses). |
| **Quality & Principles** | **Duplicated Code (DRY)** | `DUPLICATE_CODE_DRY` | Duplicated function body logic across modules. |
| **Quality & Principles** | **Circular Dependency** | `CIRCULAR_MODULE_DEPENDENCY` | Cyclic cross-module dependencies (`A -> B -> A`). |

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/bivex/DPX-Elixir.git
cd DPX-Elixir
uv sync
```

### Usage

```bash
# Terminal scan with rich formatting
uv run dpx-elixir scan /path/to/elixir_app

# Generate interactive dark Semantic UI HTML dashboard
uv run dpx-elixir scan /path/to/elixir_app -H reports/dashboard.html

# Generate SARIF for GitHub Code Scanning
uv run dpx-elixir scan /path/to/elixir_app -S reports/security.sarif

# Export AI Context prompt for LLM refactoring
uv run dpx-elixir scan /path/to/elixir_app --llm
```

---

## 🏛️ Hexagonal Architecture

```
                    ┌──────────────────────────────┐
                    │    Inbound Drivers (CLI)     │
                    │   Typer CLI / REST / IDE     │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        Application Layer                             │
│       ScanningService ──────────────► DetectionService               │
└──────────────────┬─────────────────────────────────┬─────────────────┘
                   │                                 │
                   ▼                                 ▼
┌──────────────────────────────────────┐  ┌────────────────────────────┐
│             Domain Layer             │  │   Outbound Ports           │
│  - Value Objects (PatternType, etc.) │  │  - SourceProviderPort      │
│  - CodeModel (Module, Function)      │  │  - ParserPort              │
│  - Detection & DetectionReport       │  │  - ReportFormatterPort    │
│  - 30 Pattern & Safety Rules         │  │  - ResultRepositoryPort    │
└──────────────────────────────────────┘  └──────────┬─────────────────┘
                                                     │
                                                     ▼
                                  ┌────────────────────────────────────┐
                                  │       Outbound Adapters            │
                                  │  - NativeElixirParserAdapter       │
                                  │  - HtmlReportFormatter (Dark UI)   │
                                  │  - SarifReportFormatter (v2.1.0)   │
                                  │  - Json / Markdown Formatters      │
                                  └────────────────────────────────────┘
```

---

## 🌐 The DPX Suite Family

Static architectural analysis, design pattern detection, and observability HUDs across languages:

| Engine | Target Ecosystem | Focus / Paradigm | GoF Coverage |
|---|---|---|:---:|
| [**DPX-CSharp**](https://github.com/bivex/DPX-CSharp) | C# 10–13 / .NET 6–9+ | CQRS, MediatR, Channels, Async Safety, HUD | **23/23 (100%)** |
| [**DPX-TypeScript**](https://github.com/bivex/DPX-TypeScript) | TypeScript 5.x / JavaScript ES2022+ | Type-Level & Async Safety, Middleware, HUD | **23/23 (100%)** |
| [**DPX-Rust**](https://github.com/bivex/DPX-Rust) | Rust (2015–2024 Editions) | Typestate, RAII/Drop, Actors, Safety Guard | **23/23 (100%)** |
| [**DPX-Go**](https://github.com/bivex/DPX-Go) | Go (1.18–1.24+) | Concurrency Idioms, Pipelines, Clean Arch | **23/23 (100%)** |
| [**DPX-Py**](https://github.com/bivex/DPX-Py) | Python (3.8–3.13+) | Multi-Paradigm Hexagonal Pattern Engine | **23/23 (100%)** |
| [**DPX-Php**](https://github.com/bivex/DPX-Php) | PHP (7.4–8.4+) | GoF Patterns, SOLID, PSR-15/Laravel Pipelines | **23/23 (100%)** |
| [**DPX-Haskell**](https://github.com/bivex/DPX-Haskell) | Haskell (GHC 9.2–9.10+) | Typeclasses, Monads, STM, Space Leaks | Functional Idioms |
| [**DPX-OCaml**](https://github.com/bivex/DPX-OCaml) | OCaml (4.14–5.3+ / Multicore) | Modules, Functors, Lwt Concurrency, Multicore | Functional Idioms |
| [**DPX-Elixir**](https://github.com/bivex/DPX-Elixir) | Elixir / OTP (1.14–1.18+) | GenServer, Supervisors, Dynamic Supervisor | Actor & Fault Tolerance |
| [**DPX-Erlang**](https://github.com/bivex/DPX-Erlang) | Erlang / OTP (20–27+) | OTP Behaviors, Supervision Trees, Actors | Actor & Fault Tolerance |
| [**DPX-C**](https://github.com/bivex/DPX-C) | Pure C (C89, C99, C11, C17, C23) | Opaque Structs, Function Pointers, Memory Safety | Structs & Memory |
| [**DPX-Cpp**](https://github.com/bivex/DPX-Cpp) | C++ (C++14 / 17 / 20) | Hexagonal DDD Pattern Engine (ANTLR4) | **23/23 (100%)** |
| [**DPX-Java**](https://github.com/bivex/DPX-Java) | Java (Java 8–21+) | Spring / Quarkus DDD Pattern Engine (ANTLR4) | **23/23 (100%)** |
| [**DPX**](https://github.com/bivex/DPX) | Meta / Multi-Engine | Unified Architecture Discovery Standard | Multi-Engine |


---

## 📄 License

MIT © bivex
