from src.utils.generic_utils import read_json, load_json_paths, combine_conversations
def main():
    word_paths = load_json_paths()
    word_converasations = read_json(word_paths)
    conversations = combine_conversations(word_converasations)


if __name__ == "__main__":
    main()