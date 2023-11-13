class Statement:
    def __init__(self, speaker, text, time_spoken):
        self.speaker = speaker
        self.text = text
        self.time_spoken = time_spoken
        self.politeness_score = None
        self.embedding = None
        self.influence_score = None
        self.off_topic_score = None
        self.curiosity_score = None

    def __repr__(self):
        return f"{self.speaker}: {self.time_spoken} : {self.text}"

    def get_words_per_minute(self):
        return len(self.text.split()) / (self.time_spoken / 60)

    def get_mentions(self, speaker_names):
        """
        TODO: Determine if the statement mentions the given speaker.
        :param speaker:
        :return:
        """
        speakers_mentioned = [speaker_name for speaker_name in speaker_names
                              if (speaker_name in self.text and speaker_name != self.speaker)]
        return speakers_mentioned

    def set_politeness_score(self, score):
        self.politeness_score = score

    def combine_statements(self, statement):
        """
        Appends the two statements into a single statement.
        :param statement:
        :return:
        """
        self.time_spoken += statement.time_spoken
        self.text += statement.text
        return self

    def set_embedding(self, embedding):
        self.embedding = embedding

    def set_influence_score(self, score):
        self.influence_score = score

    def set_off_topic_score(self, score):
        self.off_topic_score = score

    def set_curiosity_score(self, score):
        self.curiosity_score = score



class Speaker:
    def __init__(self, name):
        self.name = name
        self.statements = list()
        self.mentioned_count = 0
        self.early_commenter = False
        self.off_topic_classification_threshold = 0.5
        self.influence_classification_threshold = 0.5
        self.curiosity_classification_threshold = 0.5
        self.meeting_length = None

    def add_statement(self, statement):
        self.statements.append(statement)

    def set_early_commenter(self, is_early_commenter=True):
        self.early_commenter = is_early_commenter

    def add_mentioned(self):
        self.mentioned_count += 1

    def get_num_statements(self):
        return len(self.statements)

    def get_total_time_spoken(self):
        return sum([statement.time_spoken for statement in self.statements])

    def get_average_time_spoken(self):
        return self.get_total_time_spoken() / len(self.statements)

    def set_meeting_length(self, meeting_length):
        self.meeting_length = meeting_length

    def get_percent_time_spoken(self):
        if self.meeting_length is None:
            return None
        return self.get_total_time_spoken() / self.meeting_length

    def get_words_spoken(self):
        return sum([len(statement.text.split()) for statement in self.statements])

    def get_average_words_per_statement(self):
        return sum([statement.get_words_per_minute() for statement in self.statements]) / len(self.statements)

    def count_influence_statements(self):
        influence_scores = [statement.influence_score for statement in self.statements if statement.influence_score is not None]
        return sum([1 for score in influence_scores if score > self.influence_classification_threshold])

    def count_off_topic_statements(self):
        off_topic_scores = [statement.off_topic_score for statement in self.statements if statement.off_topic_score is not None]
        return sum([1 for score in off_topic_scores if score > self.off_topic_classification_threshold])

    def get_average_politeness_score(self):
        return sum([statement.politeness_score for statement in self.statements]) / len(self.statements)

    def get_average_influence_score(self):
        influence_scores = [statement.influence_score for statement in self.statements if statement.influence_score is not None]
        if len(influence_scores) == 0:
            return None
        return sum(influence_scores) / len(influence_scores)

    def get_average_off_topic_score(self):
        off_topic_scores = [statement.off_topic_score for statement in self.statements if statement.off_topic_score is not None]
        if len(off_topic_scores) == 0:
            return None
        return sum(off_topic_scores) / len(off_topic_scores)

    def get_average_curiosity_score(self):
        curiosity_scores = [statement.curiosity_score for statement in self.statements if statement.curiosity_score is not None]
        return sum(curiosity_scores) / len(curiosity_scores)

    def count_curiosity_statements(self):
        return sum([1 for statement in self.statements if statement.curiosity_score > self.curiosity_classification_threshold])

    def to_dict(self):
        return {
            "name": self.name,
            "mentioned_count": self.mentioned_count,
            "early_commenter": self.early_commenter,
            "percent_time_spoken": self.get_percent_time_spoken(),
            "average_wps": self.get_average_words_per_statement(),
            "politeness_score": self.get_average_politeness_score(),
            "influence_score": self.get_average_influence_score(),
            "off_topic_score": self.get_average_off_topic_score(),
            "curiosity_score": self.get_average_curiosity_score(),
            "influence_count": self.count_influence_statements(),
            "off_topic_count": self.count_off_topic_statements(),
            "curious_statement_count": self.count_curiosity_statements(),
            "words_spoken": self.get_words_spoken(),
            "average_time_spoken": self.get_average_time_spoken(),
            "total_time_spoken": self.get_total_time_spoken(),
            "num_statements": self.get_num_statements()
        }


