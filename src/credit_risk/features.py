from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureSet:
    name: str
    description: str
    numeric: tuple[str, ...]
    categorical: tuple[str, ...]

    @property
    def columns(self) -> list[str]:
        return list(self.numeric + self.categorical)


PLATFORM_INFORMED_FEATURES = FeatureSet(
    name="platform_informed",
    description="Borrower and loan features with LendingClub grade, sub-grade, and interest rate.",
    numeric=(
        "loan_amnt",
        "term",
        "int_rate",
        "annual_inc",
        "dti",
        "delinq_2yrs",
        "revol_util",
        "total_acc",
        "open_acc",
        "emp_length",
    ),
    categorical=(
        "grade",
        "sub_grade",
        "home_ownership",
        "verification_status",
        "purpose",
        "addr_state",
    ),
)


BORROWER_ONLY_FEATURES = FeatureSet(
    name="borrower_only",
    description="Borrower and loan features excluding LendingClub grade, sub-grade, and interest rate.",
    numeric=(
        "loan_amnt",
        "term",
        "annual_inc",
        "dti",
        "delinq_2yrs",
        "revol_util",
        "total_acc",
        "open_acc",
        "emp_length",
    ),
    categorical=(
        "home_ownership",
        "verification_status",
        "purpose",
        "addr_state",
    ),
)


def platform_informed_feature_set() -> FeatureSet:
    return PLATFORM_INFORMED_FEATURES


def borrower_only_feature_set() -> FeatureSet:
    return BORROWER_ONLY_FEATURES
