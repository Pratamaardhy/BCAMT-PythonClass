def most_frequent_word(text):
    """Return a dictionary with the most common word and its count.
    Example: most_frequent_word('Hallo aku dan ...') -> {'word': 'lucu', 'count': 2}
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    cleaned_text = text.strip()
    if cleaned_text == "":
        raise ValueError("text cannot be empty")

    words = []
    for token in cleaned_text.lower().replace('-', ' ').split():
        cleaned_word = ""
        for ch in token:
            if ch.isalpha() or ch.isdigit():
                cleaned_word += ch
        if cleaned_word:
            words.append(cleaned_word)

    if not words:
        raise ValueError("No valid words found in the text")

    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    most_word = ""
    most_count = 0
    for word, count in frequency.items():
        if count > most_count:
            most_word = word
            most_count = count

    return {
        'word': most_word,
        'count': most_count,
    }

def run_tests():
    sentence = "Hallo aku dan teman-temanku mempunyai kucing annabul lucu-lucu."
    assert most_frequent_word(sentence) == {'word': 'lucu', 'count': 2}

    try:
        most_frequent_word("")
        raise AssertionError("most_frequent_word should reject empty input")
    except ValueError:
        pass

if __name__ == "__main__":
    run_tests()
    print("Challenge 6 tests passed successfully.")
