import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
{"role": "system", "content": "You are a skilled evaluator of human speech and interaction. Evaluate if the following sentence is an open question, closed question, or not a question at all. Respond Open, Closed, or Not a Question."},
{"role": "user", "content": "I see that you are a skilled speech evaluator. How would you rate my speech?"}
#    {"role": "system", "content": "You are a skilled evaluator of human speech and interaction. Evaluate if the following sentence is an example of collaboration, leadership, creativity, or problem solving. Respond with a Yes or No for each, but do not explain."},
#    {"role": "user", "content": "Please help me."}
  ]
)

print(completion.choices[0].message)