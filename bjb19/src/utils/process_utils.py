from typing import List

import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from src.utils.schema import Statement, Speaker
import numpy as np

class ModelHub:
    def __init__(self):
        self.zero_encode_model_name = "facebook/bart-large-mnli"
        self.zero_encode_pipeline = None
        self.embed_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
        self.embed_model = None
        self.curosity_model_name = 'shahrukhx01/bert-mini-finetune-question-detection'
        self.curiosity_model = None

    def politeness_score(self, text):
        """
        :param text:
        :return:
        """
        if self.zero_encode_pipeline is None:
            self.zero_encode_pipeline = pipeline(model=self.zero_encode_model_name)
        candidate_labels = ["polite"]
        output = self.zero_encode_pipeline(text, candidate_labels=candidate_labels)
        return output['scores'][0]


    def embed_text(self, text):
        if self.embed_model is None:
            self.embed_model = SentenceTransformer(self.embed_model_name)
        embedding = self.embed_model.encode(text)
        return embedding


    def similiarty_score(self, embedding, compare_embeddings):
        """
        :param text:
        :param texts:
        :return:
        """
        compare_embeddings = np.array(compare_embeddings)
        similarities = util.pytorch_cos_sim(embedding, compare_embeddings)
        return float(torch.mean(similarities))

    def get_influence_score(self, embedding, previous_embeddings, next_embeddings):
        """
        :param text:
        :return:
        """
        previous_similarity = self.similiarty_score(embedding, previous_embeddings)
        upcoming_similarity = self.similiarty_score(embedding, next_embeddings)
        influence_score = ((1 - previous_similarity) + upcoming_similarity) / 2
        return influence_score

    def get_off_topic_score(self, embedding, previous_embeddings, next_embeddings):
        """
        :param text:
        :return:
        """
        previous_similarity = self.similiarty_score(embedding, previous_embeddings)
        upcoming_similarity = self.similiarty_score(embedding, next_embeddings)
        off_topic_score = (1-previous_similarity + 1-upcoming_similarity) / 2
        return off_topic_score

    def curiosity_score(self, text):
        """
        :param text:
        :return:
        """
        if self.zero_encode_pipeline is None:
            self.zero_encode_pipeline = pipeline(model=self.zero_encode_model_name)
        candidate_labels = ["curiosity expressed"]
        output = self.zero_encode_pipeline(text, candidate_labels=candidate_labels)
        return output['scores'][0]


def anaylze_statement_level_conversation(conversation: List[Statement]):
    """
    Analyze the given conversation at the statement level.
    :param conversation:
    :return:
    """
    hub = ModelHub()
    speaker_names = set([statement.speaker for statement in conversation])
    speakers = dict()
    for speaker_name in speaker_names:
        speakers[speaker_name] = Speaker(speaker_name)

    for statement in conversation:
        speakers[statement.speaker].add_statement(statement)

    for statement in conversation:
        mentioned = statement.get_mentions(speaker_names)
        for speaker in mentioned:
            speakers[speaker].add_mentioned()

    total_conversation_time = sum([statement.time_spoken for statement in conversation])
    for speaker_name in speaker_names:
        speakers[speaker_name].set_meeting_length(total_conversation_time)

    early_statement_index = 10
    for early_statement in conversation[:early_statement_index]:
        speakers[early_statement.speaker].set_early_commenter()

    for statement in conversation:
        statement.set_politeness_score(hub.politeness_score(statement.text))

    for statement in conversation:
        statement.set_embedding(hub.embed_text(statement.text))

    influence_context_window = 3
    for i in range(influence_context_window, len(conversation) - influence_context_window):
        previous_embeddings = [ statement.embedding for statement in conversation[i-influence_context_window:i] ]
        future_embeddings = [ statement.embedding for statement in conversation[i+1:i+influence_context_window+1] ]
        current_embedding = conversation[i].embedding
        influence_score = hub.get_influence_score(current_embedding, previous_embeddings, future_embeddings)
        statement.set_influence_score(influence_score)

    off_topic_context_window = 3
    for i in range(off_topic_context_window, len(conversation) - off_topic_context_window):
        previous_embeddings = [ statement.embedding for statement in conversation[i-off_topic_context_window:i] ]
        future_embeddings = [ statement.embedding for statement in conversation[i+1:i+off_topic_context_window+1] ]
        current_embedding = conversation[i].embedding
        off_topic_score = hub.get_off_topic_score(current_embedding, previous_embeddings, future_embeddings)
        statement.set_off_topic_score(off_topic_score)

    for statement in conversation:
        statement.set_curiosity_score(hub.curiosity_score(statement.text))
    return speakers
