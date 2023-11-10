import os

from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from .assets import meetings

meetings_assets = load_assets_from_package_module(
    meetings,
    group_name="meetings",
    # all of these assets live in the duckdb database, under the schema meetings
    key_prefix=["meetings"],
)

# define jobs as selections over the larger graph
run_all_job = define_asset_job("run_all_job", selection="*")

defs = Definitions(
    assets=[*meetings_assets],
    schedules=[
        ScheduleDefinition(job=run_all_job, cron_schedule="@daily"),
    ],
)
