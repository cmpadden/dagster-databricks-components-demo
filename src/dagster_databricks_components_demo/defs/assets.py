import dagster as dg
from .constants import (
    RAW_TRANSACTIONS_DATA,
    RAW_CUSTOMERS_DATA,
    RAW_ACCOUNTS_DATA,
    PREPARED_TRANSACTIONS_DATA,
    PREPARED_CUSTOMERS_DATA,
    PREPARED_ACCOUNTS_DATA,
    S3_PATHS,
)

ASSET_OWNERS = ["bob@acme.com"]


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    s3_path = S3_PATHS["raw_transactions"]
    context.log.info(f"Writing {len(RAW_TRANSACTIONS_DATA)} transactions to {s3_path}")

    return dg.MaterializeResult(
        metadata={
            "records": len(RAW_TRANSACTIONS_DATA),
            "s3_path": s3_path,
            "file_format": "csv",
        }
    )


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    s3_path = S3_PATHS["raw_customers"]
    context.log.info(f"Writing {len(RAW_CUSTOMERS_DATA)} customers to {s3_path}")

    return dg.MaterializeResult(
        metadata={
            "records": len(RAW_CUSTOMERS_DATA),
            "s3_path": s3_path,
            "file_format": "csv",
        }
    )


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    s3_path = S3_PATHS["raw_accounts"]
    context.log.info(f"Writing {len(RAW_ACCOUNTS_DATA)} accounts to {s3_path}")

    return dg.MaterializeResult(
        metadata={
            "records": len(RAW_ACCOUNTS_DATA),
            "s3_path": s3_path,
            "file_format": "csv",
        }
    )


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_transactions], owners=ASSET_OWNERS)
def prepared_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    s3_path = S3_PATHS["prepared_transactions"]
    context.log.info(
        f"Processing and writing {len(PREPARED_TRANSACTIONS_DATA)} prepared transactions to {s3_path}"
    )
    context.log.info(
        "Applied transformations: category classification, large transaction flagging"
    )

    return dg.MaterializeResult(
        metadata={
            "records": len(PREPARED_TRANSACTIONS_DATA),
            "s3_path": s3_path,
            "file_format": "parquet",
            "transformations_applied": [
                "category_classification",
                "large_transaction_flag",
            ],
        }
    )


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_customers], owners=ASSET_OWNERS)
def prepared_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    s3_path = S3_PATHS["prepared_customers"]
    context.log.info(
        f"Processing and writing {len(PREPARED_CUSTOMERS_DATA)} prepared customers to {s3_path}"
    )
    context.log.info(
        "Applied transformations: days since signup calculation, premium flag"
    )

    return dg.MaterializeResult(
        metadata={
            "records": len(PREPARED_CUSTOMERS_DATA),
            "s3_path": s3_path,
            "file_format": "parquet",
            "transformations_applied": ["days_since_signup", "premium_flag"],
        }
    )


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_accounts], owners=ASSET_OWNERS)
def prepared_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    s3_path = S3_PATHS["prepared_accounts"]
    context.log.info(
        f"Processing and writing {len(PREPARED_ACCOUNTS_DATA)} prepared accounts to {s3_path}"
    )
    context.log.info(
        "Applied transformations: balance tier classification, days active calculation"
    )

    return dg.MaterializeResult(
        metadata={
            "records": len(PREPARED_ACCOUNTS_DATA),
            "s3_path": s3_path,
            "file_format": "parquet",
            "transformations_applied": ["balance_tier", "days_active"],
        }
    )
