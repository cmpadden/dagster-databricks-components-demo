from collections.abc import Sequence
import dagster as dg

from databricks.sdk import WorkspaceClient
from dataclasses import dataclass


@dataclass
class DatabricksWorkspaceConfig(dg.Resolvable):
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
        # replace default attributes
        specs = [
            spec.replace_attributes(
                description=f"{spec.key.to_escaped_user_string()} produced by Databricks job {self.job_id}"
            )
            if not spec.description
            else spec
            for spec in self.asset_specs
        ]

        # merge default attributes
        specs = [
            spec.merge_attributes(
                metadata={
                    "databricks_job_id": self.job_id,
                    "databricks_host": self.workspace_config.host,
                    "databricks_job_parameters": self.job_parameters,
                },
                kinds={"databricks"},
            )
            for spec in specs
        ]

        @dg.multi_asset(name=f"databricks_job_{self.job_id}", specs=specs)
        def _asset(context: dg.AssetExecutionContext):
            run = self.execute(context)
            yield dg.MaterializeResult(
                metadata={
                    "start_time": run.start_time,
                    "end_time": run.end_time,
                    "job_run_id": run.job_run_id,
                }
            )

        return dg.Definitions(assets=[_asset])

    def execute(self, context: dg.AssetExecutionContext):
        context.log.info(f"Running databricks job: {self.job_id}")
        client = self.workspace_config.get_client()
        return client.jobs.run_now_and_wait(
            job_id=self.job_id,
            job_parameters=self.job_parameters,
        )
