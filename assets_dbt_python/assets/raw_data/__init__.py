import numpy as np
import pandas as pd
from dagster import asset, MetadataValue
import os
import json

from assets_dbt_python.utils import random_data


@asset(
    compute_kind="ingest",
)
def meetings(context) -> pd.DataFrame:
    """A table containing all users data."""
    
    meetings = pd.DataFrame()
    project_dir = os.path.abspath(os.path.join(os.getcwd(), ''))
    data_path = os.path.join(project_dir, "data/meeting-transcripts")

    # Define the relative path to your data folder
    for filename in os.listdir(data_path):
        with open(os.path.join(data_path, filename), 'r') as f:
            json_data = json.load(f)
            meeting = pd.DataFrame(json_data).assign(filename=filename)
            # append to the main dataframe
            meetings = meetings._append(meeting)

    meetings.reset_index(drop=True, inplace=True)

    # the words column is a list of dictionaries, so we need to extract the 'text' key from each dictionary and join them together with a space
    meetings['text'] = meetings['words'].apply(lambda x: ' '.join([d['text'] for d in x]))

    # extract the lowest start_timestamp from the words column. It is a string, so we need to convert it to a float
    meetings['start_timestamp'] = meetings['words'].apply(lambda x: min([float(d['start_timestamp']) for d in x]))

    # extract the highest end_timestamp from the words column. It is a string, so we need to convert it to a float
    meetings['end_timestamp'] = meetings['words'].apply(lambda x: max([float(d['end_timestamp']) for d in x]))

    context.add_output_metadata(
        {
            "num_records": MetadataValue.int(meetings.shape[0]),
            "preview": MetadataValue.md(meetings.head().to_markdown()),
        }
    )
    return meetings
    