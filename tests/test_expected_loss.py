import numpy as np

from credit_risk.expected_loss import calculate_expected_loss, portfolio_summary


def test_expected_loss_formula_and_bounds():
    pd_values = np.array([0.1, 0.2, 0.5])
    lgd_values = np.array([0.4, 0.6, 1.0])
    ead_values = np.array([100.0, 200.0, 300.0])

    expected_loss = calculate_expected_loss(pd_values, lgd_values, ead_values)

    np.testing.assert_allclose(expected_loss, [4.0, 24.0, 150.0])
    assert (expected_loss >= 0).all()
    assert (expected_loss <= ead_values).all()


def test_portfolio_summary_matches_sum(sample_loans):
    summary = portfolio_summary(sample_loans)

    assert summary["loan_count"] == 3
    assert summary["total_expected_loss"] == sample_loans["expected_loss_prelim"].sum()
    assert summary["total_ead"] == sample_loans["ead_proxy"].sum()
    assert summary["expected_loss_rate"] == sample_loans["expected_loss_prelim"].sum() / sample_loans["ead_proxy"].sum()
