import json
import numpy as np

class ConversationAnalyzer:
    def __init__(self, json_file):
        # load convo to json
        self.convo = json.load(json_file)
        # get speakers
        self.speakers = set()
        for sent in self.convo:
            self.speakers.add(sent["speaker"])

    # def stitch_sentence(s):
    #     words = s["words"]
    #     total_time_elapsed = float(words[-1]["end_timestamp"]) - float(words[0]["start_timestamp"])
    #     time_between_words = 
    #     return  " ".join([f"{s['speaker']}: "] +\
    #                     [word["text"] for word in words] +\
    #                     [f"| TIME ELAPSED: {round(total_time_elapsed, 2)} sec"] + \
    #                     [f"| WORDS PER SECOND: {round(len(words) / total_time_elapsed, 2)}"] + \
    #                     [f"| WORDS PER SECOND: {round(len(words) / total_time_elapsed, 2)}"])

    # def stitch_convo(c):
    #     for sent in c:
    #         print(stitch_sentence(sent) + "\n")

    def total_time_elapsed(self):
        stop_time = float(self.convo[-1]["words"][-1]["end_timestamp"])
        start_time = float(self.convo[0]["words"][0]["start_timestamp"] )
        return stop_time - start_time

    def get_conversation_kpi(self):
        return {"Total Conversation Time": self.total_time_elapsed(),
                "Number of Speakers": len(self.speakers),
                "Average Sentence Length": np.average([len(s["words"]) for s in self.convo]),
                "Average Pause Between Speakers": self.get_avg_pause()}
        
    def get_avg_pause(self):
        pauses = []
        for i in range(1, len(self.convo)):
            start = float(self.convo[i]["words"][0]["start_timestamp"])
            stop = float(self.convo[i-1]["words"][-1]["end_timestamp"])
            pauses.append(start - stop)
        return sum(pauses) / len(pauses)
        

    def get_speaker_kpi(self, speaker):
        pass

    def get_speaker_dist(self):
        speaker_times = {s: 0 for s in self.speakers}
        for sent in self.convo:
            words = sent["words"]
            tot_time = float(words[-1]["end_timestamp"]) - float(words[0]["start_timestamp"])
            speaker_times[sent["speaker"]] += tot_time
        return speaker_times

            

