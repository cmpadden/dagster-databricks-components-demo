"""Asset checks for data validation."""

import dagster as dg
from .assets import (
    raw_transactions,
    raw_customers,
    raw_accounts,
    prepared_transactions,
    prepared_customers,
    prepared_accounts,
)
from .constants import (
    RAW_TRANSACTIONS_DATA,
    RAW_CUSTOMERS_DATA,
    RAW_ACCOUNTS_DATA,
    PREPARED_TRANSACTIONS_DATA,
    PREPARED_CUSTOMERS_DATA,
    PREPARED_ACCOUNTS_DATA,
)


@dg.asset_check(asset=raw_transactions)
def raw_transactions_id_has_no_nulls():
    num_null_transaction_ids = sum(
        1 for txn in RAW_TRANSACTIONS_DATA if not txn.get("transaction_id")
    )
    return dg.AssetCheckResult(
        passed=bool(num_null_transaction_ids == 0),
        metadata={"null_transaction_ids": num_null_transaction_ids},
    )


@dg.asset_check(asset=raw_transactions)
def raw_transactions_amounts_are_positive():
    negative_amounts = sum(
        1 for txn in RAW_TRANSACTIONS_DATA if txn.get("amount", 0) <= 0
    )
    return dg.AssetCheckResult(
        passed=bool(negative_amounts == 0),
        metadata={"negative_amounts": negative_amounts},
    )


@dg.asset_check(asset=raw_customers)
def raw_customers_id_has_no_nulls():
    num_null_customer_ids = sum(
        1 for cust in RAW_CUSTOMERS_DATA if not cust.get("customer_id")
    )
    return dg.AssetCheckResult(
        passed=bool(num_null_customer_ids == 0),
        metadata={"null_customer_ids": num_null_customer_ids},
    )


@dg.asset_check(asset=raw_customers)
def raw_customers_emails_are_valid():
    invalid_emails = sum(
        1
        for cust in RAW_CUSTOMERS_DATA
        if not cust.get("email") or "@" not in cust.get("email", "")
    )
    return dg.AssetCheckResult(
        passed=bool(invalid_emails == 0), metadata={"invalid_emails": invalid_emails}
    )


@dg.asset_check(asset=raw_accounts)
def raw_accounts_id_has_no_nulls():
    num_null_account_ids = sum(
        1 for acc in RAW_ACCOUNTS_DATA if not acc.get("account_id")
    )
    return dg.AssetCheckResult(
        passed=bool(num_null_account_ids == 0),
        metadata={"null_account_ids": num_null_account_ids},
    )


@dg.asset_check(asset=raw_accounts)
def raw_accounts_balances_are_non_negative():
    negative_balances = sum(1 for acc in RAW_ACCOUNTS_DATA if acc.get("balance", 0) < 0)
    return dg.AssetCheckResult(
        passed=bool(negative_balances == 0),
        metadata={"negative_balances": negative_balances},
    )


@dg.asset_check(asset=prepared_transactions)
def prepared_transactions_have_categories():
    missing_categories = sum(
        1 for txn in PREPARED_TRANSACTIONS_DATA if not txn.get("category")
    )
    return dg.AssetCheckResult(
        passed=bool(missing_categories == 0),
        metadata={"missing_categories": missing_categories},
    )


@dg.asset_check(asset=prepared_transactions)
def prepared_transactions_large_flag_logic():
    incorrect_flags = sum(
        1
        for txn in PREPARED_TRANSACTIONS_DATA
        if (txn.get("amount", 0) > 1000) != txn.get("is_large_transaction", False)
    )
    return dg.AssetCheckResult(
        passed=bool(incorrect_flags == 0),
        metadata={"incorrect_large_transaction_flags": incorrect_flags},
    )


@dg.asset_check(asset=prepared_customers)
def prepared_customers_premium_flag_logic():
    incorrect_premium_flags = sum(
        1
        for cust in PREPARED_CUSTOMERS_DATA
        if (cust.get("segment") == "premium") != cust.get("is_premium", False)
    )
    return dg.AssetCheckResult(
        passed=bool(incorrect_premium_flags == 0),
        metadata={"incorrect_premium_flags": incorrect_premium_flags},
    )


@dg.asset_check(asset=prepared_customers)
def prepared_customers_days_since_signup_positive():
    negative_days = sum(
        1 for cust in PREPARED_CUSTOMERS_DATA if cust.get("days_since_signup", 0) < 0
    )
    return dg.AssetCheckResult(
        passed=bool(negative_days == 0),
        metadata={"negative_days_since_signup": negative_days},
    )


@dg.asset_check(asset=prepared_accounts)
def prepared_accounts_balance_tier_logic():
    incorrect_tiers = sum(
        1
        for acc in PREPARED_ACCOUNTS_DATA
        if not _is_balance_tier_correct(
            acc.get("balance", 0), acc.get("balance_tier", "")
        )
    )
    return dg.AssetCheckResult(
        passed=bool(incorrect_tiers == 0),
        metadata={"incorrect_balance_tiers": incorrect_tiers},
    )


@dg.asset_check(asset=prepared_accounts)
def prepared_accounts_days_active_positive():
    negative_days = sum(
        1 for acc in PREPARED_ACCOUNTS_DATA if acc.get("days_active", 0) < 0
    )
    return dg.AssetCheckResult(
        passed=bool(negative_days == 0),
        metadata={"negative_days_active": negative_days},
    )


def _is_balance_tier_correct(balance: float, tier: str) -> bool:
    """Helper function to validate balance tier logic."""
    if balance < 1000:
        return tier == "low"
    elif balance < 10000:
        return tier == "medium"
    else:
        return tier == "high"
