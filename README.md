# Cleve StackStorm Pack

This StackStorm pack provides actions for interacting with [Cleve](https://github.com/gmc-norr/cleve).

## Requirements

The pack is tightly coupled to the Cleve API, and currently requires Cleve >=1.0.0

## Notes

When this automation looks for new runs to be added to Cleve, it only looks for the files required as defined in the config.
By default this is `RunInfo.xml` and `RunParameters.xml`.
If not all required files are found, the directory will be ignored, and a warning will be logged.

If the workflow `add_run_workflow` gets an error response from Cleve, it will mark the sequencing run that was attempted to be added as excluded.
By default it writes the file `.cleve-exclude` in the run directory.
This will tell the sensor to not attempt to add this run again.
If this was caused by an error that is fixable, you can simply delete the `.cleve-exclude` file, and the sensor will pick this up on the next poll.

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
