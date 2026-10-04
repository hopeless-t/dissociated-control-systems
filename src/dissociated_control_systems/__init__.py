"""Dissociated Control Systems research primitives."""

from .curriculum import CurriculumTask, choose_curriculum_task
from .meta_loop import (
    ObservationOption,
    choose_observation,
    effective_pressure,
    expected_cascade_cost,
    learning_velocity,
    two_tier_break_even_stop_probability,
)
from .physical_envelope import (
    SupportPair,
    contact_compression,
    envelope_scale,
    load_fraction,
    solve_vertical_support_pair,
)
from .representation_budget import (
    RepresentationOption,
    choose_minimal_sufficient_representation,
    should_expand_representation,
)
from .skill_compiler import (
    CompiledSkill,
    replay_is_economical,
    select_compiled_skill,
)
from .state_model import (
    SubsystemState,
    coarse_observation,
    dissociation_index,
    equivalence_class,
    expressed_capability,
    rich_observation,
)

__all__ = [
    "CompiledSkill",
    "CurriculumTask",
    "ObservationOption",
    "RepresentationOption",
    "SubsystemState",
    "SupportPair",
    "choose_curriculum_task",
    "choose_minimal_sufficient_representation",
    "choose_observation",
    "coarse_observation",
    "contact_compression",
    "dissociation_index",
    "effective_pressure",
    "envelope_scale",
    "equivalence_class",
    "expected_cascade_cost",
    "expressed_capability",
    "learning_velocity",
    "load_fraction",
    "replay_is_economical",
    "rich_observation",
    "select_compiled_skill",
    "should_expand_representation",
    "solve_vertical_support_pair",
    "two_tier_break_even_stop_probability",
]
