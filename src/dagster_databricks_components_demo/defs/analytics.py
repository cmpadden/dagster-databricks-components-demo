import dagster as dg


@dg.asset(
    kinds={"looker"},
    owners=["chuck@acme.com"],
    deps=["account_performance", "customer_insights", "transactions"],
)
def analytics_dashboard(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...
