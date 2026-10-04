from credit_risk.expected_loss import concentration_summary, segment_summary


def test_segment_summary_preserves_total_expected_loss(sample_loans):
    grouped = segment_summary(sample_loans, "grade")

    assert grouped["total_expected_loss"].sum() == sample_loans["expected_loss_prelim"].sum()


def test_concentration_summary_top_group(sample_loans):
    summary = concentration_summary(sample_loans, shares=(1 / 3,))

    assert summary.loc[0, "loan_count"] == 1
    assert summary.loc[0, "total_expected_loss"] == sample_loans["expected_loss_prelim"].max()
