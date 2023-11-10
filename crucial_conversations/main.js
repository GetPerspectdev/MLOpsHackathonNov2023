// The following is part of a nodejs flow in Pipedream

import axios from "axios"
import _ from 'lodash';

export default defineComponent({
  async run({ steps, $ }) {
    // Variables
    let conversation = [];
    let text = steps.trigger.event.body;

    // Merge the transcript into a human redable dialog
    _.forEach(text, function(sentance, index){
      // Mark who the speaker is
      let new_sentance = sentance.speaker + ": ";
      
      // Concatenate the words
      _.forEach(sentance.words, function(word){
        new_sentance += word.text + " ";
      });
      
      // Remove trailing white space
      new_sentance = new_sentance.trim();
      
      // Add concatenated sentance to conversation
      conversation.push(new_sentance);
    });

    // Construct the ChatGPT prompt
    let prompt = `Play the role of the author of Crucial Conversations. The following transcript is from a meeting. From the perspective of the of the author determine the following details. 1, if the conversation is crucial. If the conversation is not crucial then return that the conversation is not crucial and don't process the rest of the questions about the conversation. 2, the goal / focus of the crucial conversation. 3, a score between 0 and 100 on how each of the speakers performed. 4, a brief explanation of the reasoning for each of the score. 5, what each involved speaker could have done to improve how they handled the crucial conversation. The data should be returned in a valid JSON object so that it can be processed. The example structure is as follows. 
    results = {
      "is_conversation_crucial": true,
      "conversation_goal": "The goal of the conversation",
      "participant_review": [
        {
          "speaker": "A",
          "conversation_score": 80,
          "conversation_score_reason": "Reason for the score",
          "conversation_improvement": "What the speaker could have done to improve"
        }
      ],
    }

    The conversation: 
    `

    // Add the conversation to the prompt
    _.forEach(conversation, function(sentance){
      prompt += sentance + '\n';
    });
    
    // Return the results
    return prompt
    
  },
})