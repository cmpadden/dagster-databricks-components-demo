from collections.abc import Sequence
import dagster as dg

from databricks.sdk import WorkspaceClient


class DatabricksWorkspaceConfig(dg.Model):
    host: str
    token: str

    def get_client(self):
        return WorkspaceClient(host=self.host, token=self.token)


class DatabricksJobComponent(dg.Component, dg.Model, dg.Resolvable):
    """Run Databricks jobs from Dagster and attach corresponding assets."""

    job_id: int
    job_parameters: dict[str, str] | None = None
    workspace_config: DatabricksWorkspaceConfig
    asset_specs: Sequence[dg.ResolvedAssetSpec]

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        @dg.multi_asset(name=f"databricks_job_{self.job_id}", specs=self.asset_specs)
        def _asset(context: dg.AssetExecutionContext):
            self.execute(context)

        return dg.Definitions(assets=[_asset])

    def execute(self, context: dg.AssetExecutionContext):
        context.log.info(f"Running databricks job: {self.job_id}")
        wc = self.workspace_config.get_client()
        return wc.jobs.run_now_and_wait(
            job_id=self.job_id,
            job_parameters=self.job_parameters,
        )
