from typing import List

from src.utils.schema import Speaker
import matplotlib.pyplot as plt


def display_person(speaker: Speaker):
    """
    Display the given speaker.
    :param speaker:
    :return:
    """
    labels = ['Mentioned Count', 'Number of Comments', 'Influence Count', 'Off Topic Count']
    values = [speaker.mentioned_count, speaker.get_num_statements(), speaker.count_influence_statements(), speaker.count_off_topic_statements()]
    fig = plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.show()

    labels = ['Average Politeness Score', 'Average Curiosity Score', 'Average Influence Score', 'Average Off Topic Score']
    values = [speaker.get_average_politeness_score(), speaker.get_average_curiosity_score(),
              speaker.get_average_influence_score(), speaker.get_average_off_topic_score()]
    fig = plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    print("\n")


def save_values(speakers: List[Speaker], save_path) :
    import pandas as pd
    df = pd.DataFrame.from_records([speaker.to_dict() for speaker in speakers])
    df.to_csv(save_path, index=False)
    return True