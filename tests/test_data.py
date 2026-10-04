import pandas as pd

from credit_risk.data import parse_emp_length, parse_term_months


def test_parse_term_months_from_lendingclub_strings():
    assert parse_term_months("36 months") == 36
    assert parse_term_months("60 months") == 60


def test_parse_emp_length_from_lendingclub_strings():
    assert parse_emp_length("10+ years") == 10
    assert parse_emp_length("3 years") == 3


def test_parse_emp_length_preserves_less_than_one_year_and_missing_values():
    assert parse_emp_length("< 1 year") == 0
    assert pd.isna(parse_emp_length("N/A"))
    assert pd.isna(parse_emp_length(None))


def test_parse_helpers_support_series_inputs():
    terms = parse_term_months(pd.Series(["36 months", "60 months", None]))
    employment = parse_emp_length(pd.Series(["10+ years", "3 years", "< 1 year", None]))

    assert terms.iloc[:2].tolist() == [36, 60]
    assert pd.isna(terms.iloc[2])
    assert employment.iloc[:3].tolist() == [10, 3, 0]
    assert pd.isna(employment.iloc[3])
