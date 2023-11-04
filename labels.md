# This markdown file is used to explain the reasoning behind the labels used in the dataset.

### name
The name of the person who spoke the statement.

### mentioned_count
The number of times this person was mentioned other people's statements. (Limit one per statement)

### early_commenter
Was this person involved in the conversation early on? (Did they speak in the first 10 statements? This is a tuneable parameter)

### percent_time_spoken
What percentage of the total time spoken was this person speaking? (Time person spent speaking / Total talking time of meeting)

### average_wps
How fast does this person talk? (Average words per second)

### politeness_score
A zero shot encoding model was used to determine the politeness of a statement. (Score from 0 to 1, 1 being the most polite)

### influence_score
What was the average influence score of this person's statements? (Score from 0 to 1, 1 being the most influential)
This was calculated by embedding statements and then comparing similarity to previous statements and future statements.
A Context Window fo 3 statements before and after was used.
Cosine similarity was used to compare embeddings.
Score is ((1-previous_similarity) + (future_similarity)) / 2

### off_topic_score
What was the average off topicedness of this person's statements? (Score from 0 to 1, 1 being the most off topic)
This was calculated by embedding statements and then comparing similarity to previous statements and future statements.
A Context Window fo 3 statements before and after was used.
Cosine similarity was used to compare embeddings.
Score is ((1-previous_similarity) + (1-future_similarity)) / 2

### curiosity_score
How curious was the average statement of this person? (Score from 0 to 1, 1 being the most curious)
This was calculated by using a zero shot encoding model to determine the curiosity of a statement.

### influence_count
How many statements did the person make that were above a certain influence threshold? (Tuneable parameter)

### off_topic_count
How many statements did the person make that were above a certain off topic threshold? (Tuneable parameter)

### curious_statement_count
How many statements did the person make that were above a certain curiosity threshold? (Tuneable parameter)

### words_spoken
How many words did the person speak?

### average_time_spoken
What was the average time of the person's statements?

### total_time_spoken
What was the total time of the person's statements?

### num_statements
How many statements did the person make?
