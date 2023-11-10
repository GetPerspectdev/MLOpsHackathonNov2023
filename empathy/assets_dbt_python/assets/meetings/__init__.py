import numpy as np
import pandas as pd
from dagster import asset, MetadataValue
import os
import json

from assets_dbt_python.utils import random_data


@asset(
    compute_kind="Pandas",
)
def meetings(context) -> pd.DataFrame:
    """Prepare transcript data for processing."""
    
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
    
@asset(
    compute_kind="HuggingFace",
)
def open_ended_questions(context, meetings) -> pd.DataFrame:
    """Classifier for whether questions are open-ended."""
    
    from transformers import pipeline
    classifier = pipeline("sentiment-analysis", model="arl949/bert-base-cased-finetuned-open-ended-questions-english")
    
    texts = meetings['text'].tolist()
    
    questions = [text if '?' in text else '' for text in texts ]

    # Currently hitting some max length issues with the model, we can only take 512 words at a time
    classifications = classifier(questions, truncation=True, max_length=512, padding=True)

    context.add_output_metadata(
        {
            "num_records": MetadataValue.int(len(classifications)),
            "preview": MetadataValue.md(pd.DataFrame(classifications).head().to_markdown()),
        }
    )
    return pd.DataFrame(classifications)

@asset(
    compute_kind="VaderSentiment",
)
def affirmations(context, meetings) -> list:
    """Sentiment analysis of meeting contributions."""
    
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    
    texts = meetings['text'].tolist()
    
    scores = [analyzer.polarity_scores(text) for text in texts]

    context.add_output_metadata(
        {
            "num_records": MetadataValue.int(len(scores)),
            "preview": scores[:5],
        }
    )
    return scores

@asset(
    compute_kind="SentenceTransformers",
)
def reflective_listening(context, meetings) -> list:
    """Semantic similarity for listening and summary"""
    
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    texts = meetings['text'].tolist()
    
    # Calculate cosine similarity between the sentence and the one prior if they are in the same meeting
    sentences1 = [text for text in texts]
    sentences2 = [text for text in texts[1:]] + ['']

    #Compute embeddings
    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    #Compute cosine-similarities
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    
    # get scores along the diagonal then convert to list
    cosine_scores = np.diagonal(cosine_scores).tolist()

    context.add_output_metadata(
        {
            "num_records": len(cosine_scores),
            "preview": cosine_scores[:5],
        }
    )
    return cosine_scores

@asset(
    compute_kind="Pandas",
)
def motivation_interviewing_scores(context, meetings, open_ended_questions, affirmations, reflective_listening) -> pd.DataFrame:
    """Bring together the metrics for analytics."""
    
    # Open ended questions
    meetings['open_ended'] = open_ended_questions['score']

    # Take affirmations as a list of dicts and convert to a dataframe with the keys as columns
    affirmations = pd.DataFrame(affirmations)
    # add affirmations columns to meetings
    meetings['affirmations_neg'] = affirmations['neg']
    meetings['affirmations_neu'] = affirmations['neu']
    meetings['affirmations_pos'] = affirmations['pos']
    meetings['affirmations_compound'] = affirmations['compound']

    meetings['reflective_listening'] = reflective_listening

    meetings.to_csv('meetings.csv', index=False)
        
    context.add_output_metadata(
        {
            "preview": MetadataValue.md(meetings.head().to_markdown()),
        }
    )
    return meetings