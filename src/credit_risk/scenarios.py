from __future__ import annotations

import numpy as np
import pandas as pd


def deterministic_expected_loss_scenario(
    data: pd.DataFrame,
    *,
    pd_multiplier: float = 1.0,
    lgd_multiplier: float = 1.0,
    ead_multiplier: float = 1.0,
    pd_col: str = "predicted_pd",
    lgd_col: str = "lgd_estimate",
    ead_col: str = "ead_proxy",
) -> pd.DataFrame:
    """Apply deterministic PD/LGD/EAD shocks and return scenario fields."""
    out = data.copy()
    out["scenario_pd"] = np.minimum(out[pd_col] * pd_multiplier, 1.0)
    out["scenario_lgd"] = np.minimum(out[lgd_col] * lgd_multiplier, 1.0)
    out["scenario_ead"] = out[ead_col] * ead_multiplier
    out["scenario_expected_loss"] = out["scenario_pd"] * out["scenario_lgd"] * out["scenario_ead"]
    return out
