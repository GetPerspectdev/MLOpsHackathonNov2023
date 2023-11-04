import os

from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from .assets import raw_data

raw_data_assets = load_assets_from_package_module(
    raw_data,
    group_name="raw_data",
    # all of these assets live in the duckdb database, under the schema raw_data
    key_prefix=["raw_data"],
)

# define jobs as selections over the larger graph
everything_job = define_asset_job("everything_everywhere_job", selection="*")

defs = Definitions(
    assets=[*raw_data_assets],
    schedules=[
        ScheduleDefinition(job=everything_job, cron_schedule="@daily"),
    ],
)
