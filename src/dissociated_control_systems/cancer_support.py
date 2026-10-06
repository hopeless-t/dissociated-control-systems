"""Fail-closed support classification for the synthetic DCS cancer twin.

This module does not decide treatment or estimate clinical risk. It only models
whether a synthetic forecast is structurally supported enough to be emitted at
all, or must be marked unsupported / uncertain.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SupportStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    SEMANTICS_UNKNOWN = "SEMANTICS_UNKNOWN"
    OUT_OF_SUPPORT = "OUT_OF_SUPPORT"
    TRANSITION_UNRESOLVED = "TRANSITION_UNRESOLVED"
    FORECAST_UNDERSPECIFIED = "FORECAST_UNDERSPECIFIED"
    UNCERTAIN = "UNCERTAIN"


@dataclass(frozen=True)
class SupportEvidence:
    semantic_contract_valid: bool
    feature_support_valid: bool
    transition_residual_valid: bool
    future_intervention_declared: bool
    model_family_supported: bool
    predictive_uncertainty_acceptable: bool


def classify_support(evidence: SupportEvidence) -> SupportStatus:
    """Classify forecast support with semantic and structural gates first.

    Ordering is intentional:
    1. invalid meaning cannot be repaired by model confidence;
    2. missing future intervention semantics makes a counterfactual incomplete;
    3. state-space / transition support failures are distinct from uncertainty;
    4. numerical uncertainty is evaluated only after structural support passes.
    """

    if not evidence.semantic_contract_valid:
        return SupportStatus.SEMANTICS_UNKNOWN
    if not evidence.future_intervention_declared:
        return SupportStatus.FORECAST_UNDERSPECIFIED
    if not evidence.feature_support_valid or not evidence.model_family_supported:
        return SupportStatus.OUT_OF_SUPPORT
    if not evidence.transition_residual_valid:
        return SupportStatus.TRANSITION_UNRESOLVED
    if not evidence.predictive_uncertainty_acceptable:
        return SupportStatus.UNCERTAIN
    return SupportStatus.SUPPORTED


def permits_confident_forecast(evidence: SupportEvidence) -> bool:
    return classify_support(evidence) is SupportStatus.SUPPORTED
