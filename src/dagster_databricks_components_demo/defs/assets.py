import dagster as dg

ASSET_OWNERS = ["bob@acme.com"]


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "csv"}, owners=ASSET_OWNERS)
def raw_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...

@dg.asset(kinds={"s3", "parquet"}, deps=[raw_transactions], owners=ASSET_OWNERS)
def prepared_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_customers], owners=ASSET_OWNERS)
def prepared_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_accounts], owners=ASSET_OWNERS)
def prepared_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...
