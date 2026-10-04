import pandas as pd

from credit_risk.data import create_default_flag, filter_resolved_loans


def test_target_definition_mapping():
    loans = pd.DataFrame(
        {
            "loan_status": [
                "Fully Paid",
                "Charged Off",
                "Default",
                "Current",
            ]
        }
    )

    out = create_default_flag(loans)

    assert out.loc[0, "default_flag"] == 0
    assert out.loc[1, "default_flag"] == 1
    assert out.loc[2, "default_flag"] == 1
    assert pd.isna(out.loc[3, "default_flag"])


def test_filter_resolved_loans():
    loans = create_default_flag(pd.DataFrame({"loan_status": ["Fully Paid", "Current", "Default"]}))

    resolved = filter_resolved_loans(loans)

    assert len(resolved) == 2
    assert set(resolved["loan_status"]) == {"Fully Paid", "Default"}
