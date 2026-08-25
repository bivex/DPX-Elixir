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

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
