import dagster as dg


@dg.asset(kinds={"s3", "csv"})
def raw_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "csv"})
def raw_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "csv"})
def raw_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...

@dg.asset(kinds={"s3", "parquet"}, deps=[raw_transactions])
def prepared_transactions(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_customers])
def prepared_customers(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...


@dg.asset(kinds={"s3", "parquet"}, deps=[raw_accounts])
def prepared_accounts(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...
