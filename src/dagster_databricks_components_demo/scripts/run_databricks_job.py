from collections.abc import Sequence
import dagster as dg

from databricks.sdk import WorkspaceClient
from dataclasses import dataclass

DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")

if __name__ == "__main__":
    databricks_job_id = 1000180891217799
    job_parameters = {
        source_file_prefix: "s3://acme-analytics/raw"
        destination_file_prefix: "s3://acme-analytics/reports"
    }

    client = WorkspaceClient(host=self.host, token=self.token)
    client.jobs.run_now_and_wait(
        job_id=databricks_job_id,
        job_parameters=job_parameters,
    )