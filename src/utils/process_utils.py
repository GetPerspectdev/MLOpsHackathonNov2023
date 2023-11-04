def words_to_statements(words):
    statements = []
    for i in range(0, len(words), 3):
        statements.append(words[i:i+3])
    return statements