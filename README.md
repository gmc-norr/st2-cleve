# Cleve StackStorm Pack

This StackStorm pack provides actions for interacting with [Cleve](https://github.com/gmc-norr/cleve).

## Requirements

The pack is tightly coupled to the Cleve API, and currently requires Cleve >=0.8.0.

## Configuration

The three required configuration items are `base_url`, `illumina_directories`, and `api_key`.

```yaml
# Base URL where Cleve is served
base_url: https://cleve.com

# Directories that should be watched for new sequencing runs
illumina_directories:
    - /path/to/novaseq/runs
    - /path/to/miseq-i100/runs

# Cleve API key
api_key: xxx
```

## Actions

ref | description
----|-------------
add_analysis | Add a new analysis
add_run | Add a new sequencing run
add_run_workflow | Add a new sequencing run (with some extras)
get_analyses | Get sequencing analyses
get_analysis_file_prefix | Get prefix of files from an analysis
get_analysis_files | Get files from an analysis in cleve
get_platforms | Get information on the sequencing platforms in Cleve
get_run_qc | Get sample QC data
get_runs | Get sequencing runs
get_samplesheet | Get a samplesheet from a sequencing run
update_analysis | Update an analysis
update_run | Update a sequencing run

## Rules

ref | description
----|-------------
add_run | Rule for adding a new sequencing run
analysis_state_update | Forward an analysis stat update from a webhook to a new trigger
run_state_update | Forward a run state update from webhook to a new trigger

## Sensors

ref | description
----|-------------
IlluminaDirectorySensor | Detect potential new sequencing runs
