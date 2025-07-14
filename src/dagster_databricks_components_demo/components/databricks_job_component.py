from collections.abc import Sequence
import dagster as dg

from databricks.sdk import WorkspaceClient


class DatabricksWorkspaceConfig(dg.Model):
    host: str
    token: str

    def workspace_client(self):
        return WorkspaceClient(host=host, token=token)


class DatabricksJobComponent(dg.Component, dg.Model, dg.Resolvable):
    """Run Databricks jobs from Dagster and attach corresponding assets."""

    job_id: int
    workspace_config: DatabricksWorkspaceConfig
    asset_specs: Sequence[dg.ResolvedAssetSpec]

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        @dg.multi_asset(name=f"databricks_job_{self.job_id}", specs=self.asset_specs)
        def _asset(context: dg.AssetExecutionContext):
            self.execute(resolved_script_path, context)

        return dg.Definitions(assets=[_asset])

    def execute(self, job_id: str, context: dg.AssetExecutionContext):
        context.log.info(f"Running databricks job: {job_id}")
        return subprocess.run(["sh", str(resolved_script_path)], check=True)
