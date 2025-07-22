# Dagster Databricks Components Demo

This project demonstrates how to use Dagster Components to interface with Databricks and create a unified view of your data platform. It showcases how components make it easy to orchestrate Databricks jobs while maintaining full visibility and lineage tracking within Dagster's single pane of glass.

## Overview

The demo includes:

- **Custom Databricks Job Component**: A reusable component that wraps Databricks jobs as Dagster assets
- **Asset Specifications**: Declarative asset definitions with proper lineage and metadata
- **Cross-Platform Integration**: Seamless connection between Dagster orchestration and Databricks execution
- **Unified Monitoring**: View all your data assets and their dependencies in one place

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Dagster UI    │    │   Databricks     │    │   Data Assets   │
│                 │    │   Workspace      │    │                 │
│ • Asset Lineage │◄──►│ • Job Execution  │◄──►│ • S3 Buckets    │
│ • Monitoring    │    │ • Compute        │    │ • Tables        │
│ • Scheduling    │    │ • Notebooks      │    │ • Reports       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Features

- **Databricks Job Integration**: Execute Databricks jobs directly from Dagster with full parameter passing
- **Asset Lineage**: Track data dependencies across your entire pipeline
- **Metadata Enrichment**: Automatically capture job run information, timing, and parameters
- **Environment Configuration**: Secure credential management using environment variables
- **Declarative Components**: Define your data pipelines using YAML configuration

## Project Structure

```
dagster-databricks-components-demo/
├── src/
│   └── dagster_databricks_components_demo/
│       ├── components/
│       │   └── databricks_job_component.py    # Custom Databricks component
│       ├── defs/
│       │   └── databricks_job_hello_world/
│       │       └── defs.yaml                  # Component configuration
│       └── definitions.py                     # Main Dagster definitions
├── pyproject.toml                             # Project dependencies
└── README.md                                  # This file
```

## Quick Start

### Prerequisites

- Python 3.9-3.13.3
- uv package manager
- Databricks workspace access
- Databricks job ID and credentials

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd dagster-databricks-components-demo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

### Configuration

4. **Set up environment variables:**
   ```bash
   export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
   export DATABRICKS_TOKEN="your-databricks-token"
   ```

### Running the Demo

5. **Start the Dagster development server:**
   ```bash
   dg dev
   ```

6. **Access the Dagster UI:**
   Open your browser to `http://localhost:3000` to explore the asset lineage, trigger materializations, and monitor your Databricks jobs.

## Component Configuration

The demo uses a YAML-based configuration in `src/dagster_databricks_components_demo/defs/databricks_job_hello_world/defs.yaml`:

```yaml
type: dagster_databricks_components_demo.components.databricks_job_component.DatabricksJobComponent

attributes:
  job_id: 1000180891217799  # Your Databricks job ID
  job_parameters:
    source_file_prefix: "s3://acme-analytics/raw"
    destination_file_prefix: "s3://acme-analytics/reports"
  
  workspace_config:
    host: "{{ env.DATABRICKS_HOST }}"
    token: "{{ env.DATABRICKS_TOKEN }}"
  
  asset_specs:
    - key: account_performance
      owners: ["alice@acme.com"]
      deps: [prepared_accounts, prepared_customers]
      kinds: [parquet]
```

## Key Benefits

- **Unified Orchestration**: Manage both Dagster and Databricks workloads from a single interface
- **Complete Lineage**: Track data flow from raw sources through Databricks transformations to final outputs
- **Operational Excellence**: Monitor job health, performance, and data quality in one place
- **Developer Experience**: Write infrastructure as code with type-safe, declarative components
- **Scalability**: Leverage Databricks' compute power while maintaining Dagster's orchestration capabilities

## Next Steps

- Customize the `job_id` and `job_parameters` in the YAML configuration for your Databricks jobs
- Add additional asset specifications to match your data pipeline
- Explore scheduling and sensor capabilities for automated pipeline execution
- Integrate with your existing CI/CD workflows

## Contributing

This demo showcases the core concepts of Dagster Components with Databricks. Feel free to extend it with additional features like:

- Multiple job configurations
- Custom metadata extraction
- Error handling and retry logic
- Integration with other data platforms

For more information about Dagster Components, visit the [official documentation](https://docs.dagster.io/concepts/components).
