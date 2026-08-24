"""Rule catalog registration for Elixir / OTP pattern detector."""

from __future__ import annotations

from pattern_detector.domain.rules.adapter_behaviour_rule import AdapterBehaviourRule
from pattern_detector.domain.rules.agent_state_rule import AgentStateRule
from pattern_detector.domain.rules.application_rule import ApplicationRule
from pattern_detector.domain.rules.base import BasePatternRule, PatternRule
from pattern_detector.domain.rules.blocking_gen_server_call_rule import BlockingGenServerCallRule
from pattern_detector.domain.rules.circular_dependency_rule import CircularDependencyRule
from pattern_detector.domain.rules.circuit_breaker_fuse_rule import CircuitBreakerFuseRule
from pattern_detector.domain.rules.command_tagged_tuple_rule import CommandTaggedTupleRule
from pattern_detector.domain.rules.cyclomatic_complexity_kiss_rule import CyclomaticComplexityKissRule
from pattern_detector.domain.rules.decorator_body_rule import DecoratorBodyRule
from pattern_detector.domain.rules.defensive_rescue_smell_rule import DefensiveRescueSmellRule
from pattern_detector.domain.rules.duplicate_code_dry_rule import DuplicateCodeDryRule
from pattern_detector.domain.rules.dynamic_supervisor_rule import DynamicSupervisorRule
from pattern_detector.domain.rules.ets_registry_rule import EtsRegistryRule
from pattern_detector.domain.rules.facade_context_rule import FacadeContextRule
from pattern_detector.domain.rules.gen_server_rule import GenServerRule
from pattern_detector.domain.rules.gen_stage_rule import GenStageRule
from pattern_detector.domain.rules.large_module_srp_rule import LargeModuleSrpRule
from pattern_detector.domain.rules.macro_metaprogramming_rule import MacroMetaprogrammingRule
from pattern_detector.domain.rules.memoization_cache_rule import MemoizationCacheRule
from pattern_detector.domain.rules.pipeline_operator_rule import PipelineOperatorRule
from pattern_detector.domain.rules.plug_pipeline_rule import PlugPipelineRule
from pattern_detector.domain.rules.protocol_polymorphism_rule import ProtocolPolymorphismRule
from pattern_detector.domain.rules.pub_sub_phoenix_rule import PubSubPhoenixRule
from pattern_detector.domain.rules.state_machine_statex_rule import StateMachineStatexRule
from pattern_detector.domain.rules.strategy_dispatch_rule import StrategyDispatchRule
from pattern_detector.domain.rules.string_to_atom_vulnerability_rule import StringToAtomVulnerabilityRule
from pattern_detector.domain.rules.supervisor_rule import SupervisorRule
from pattern_detector.domain.rules.task_async_rule import TaskAsyncRule
from pattern_detector.domain.rules.unbounded_process_spawn_rule import UnboundedProcessSpawnRule
from pattern_detector.domain.rules.with_monadic_pipeline_rule import WithMonadicPipelineRule

DEFAULT_RULES: list[PatternRule] = [
    # OTP Behaviours (7)
    GenServerRule(),
    SupervisorRule(),
    DynamicSupervisorRule(),
    AgentStateRule(),
    TaskAsyncRule(),
    GenStageRule(),
    ApplicationRule(),

    # Functional Idioms & Structural (8)
    ProtocolPolymorphismRule(),
    MacroMetaprogrammingRule(),
    PipelineOperatorRule(),
    PlugPipelineRule(),
    EtsRegistryRule(),
    FacadeContextRule(),
    AdapterBehaviourRule(),
    DecoratorBodyRule(),

    # Behavioral & Concurrency (7)
    CommandTaggedTupleRule(),
    PubSubPhoenixRule(),
    WithMonadicPipelineRule(),
    StrategyDispatchRule(),
    CircuitBreakerFuseRule(),
    StateMachineStatexRule(),
    MemoizationCacheRule(),

    # Resilience, SOLID & Safety Audits (8)
    DefensiveRescueSmellRule(),
    UnboundedProcessSpawnRule(),
    BlockingGenServerCallRule(),
    StringToAtomVulnerabilityRule(),
    LargeModuleSrpRule(),
    CyclomaticComplexityKissRule(),
    DuplicateCodeDryRule(),
    CircularDependencyRule(),
]

__all__ = [
    "BasePatternRule",
    "PatternRule",
    "DEFAULT_RULES",
    "GenServerRule",
    "SupervisorRule",
    "DynamicSupervisorRule",
    "AgentStateRule",
    "TaskAsyncRule",
    "GenStageRule",
    "ApplicationRule",
    "ProtocolPolymorphismRule",
    "MacroMetaprogrammingRule",
    "PipelineOperatorRule",
    "PlugPipelineRule",
    "EtsRegistryRule",
    "FacadeContextRule",
    "AdapterBehaviourRule",
    "DecoratorBodyRule",
    "CommandTaggedTupleRule",
    "PubSubPhoenixRule",
    "WithMonadicPipelineRule",
    "StrategyDispatchRule",
    "CircuitBreakerFuseRule",
    "StateMachineStatexRule",
    "MemoizationCacheRule",
    "DefensiveRescueSmellRule",
    "UnboundedProcessSpawnRule",
    "BlockingGenServerCallRule",
    "StringToAtomVulnerabilityRule",
    "LargeModuleSrpRule",
    "CyclomaticComplexityKissRule",
    "DuplicateCodeDryRule",
    "CircularDependencyRule",
]
