from src.utils.generic_utils import read_json, load_json_paths, combine_conversations, edit_save_path
from src.utils.process_utils import anaylze_statement_level_conversation

from src.utils.viz import save_values
def main():
    # folder = './meeting-transcripts'
    # word_paths = load_json_paths(folder)
    word_paths = ['./meeting-transcripts/long_product_conversation.json']
    word_level_conversations = read_json(word_paths)
    statement_level_conversations = [combine_conversations(word_conversation) for word_conversation in word_level_conversations]
    conversation_info = [anaylze_statement_level_conversation(conversation) for conversation in statement_level_conversations]
    save_paths = [edit_save_path(path) for path in word_paths]
    for i in range(len(conversation_info)):
        save_values(conversation_info[i].values(), save_paths[i])


if __name__ == "__main__":
    main()
