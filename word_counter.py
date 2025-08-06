import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Download once
nltk.download('stopwords')

# Base stop words
DEFAULT_STOP_WORDS = set(w.lower() for w in stopwords.words('english'))
DEFAULT_STOP_WORDS.update(['st', 'mr', 'mrs', 'inc', 'dr'])

def count_words(text, min_count=3, additional_stopwords=None):
    stop_words = DEFAULT_STOP_WORDS.copy()
    if additional_stopwords:
        stop_words.update(w.strip().lower() for w in additional_stopwords)

    # Confirm 'st' is in stop words
    print("✅ 'st' in stop_words?", 'st' in stop_words)

    # Extract words using regex
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    # Print raw extracted words containing 'st'
    for w in words:
        if 'st' in w:
            print(f"🔍 Word with 'st': {repr(w)}")

    # Show words NOT in stop_words (for debugging)
    for w in words:
        norm = w.strip().lower()
        if norm == 'st' and norm not in stop_words:
            print(f"❌ 'st' not being filtered properly: {repr(norm)}")

    # Filter stop words
    filtered_words = [w.strip().lower() for w in words if w.strip().lower() not in stop_words]

    print("🧹 Filtered words sample:", filtered_words[:20])

    word_counts = Counter(filtered_words)
    filtered_counts = {word: count for word, count in word_counts.items() if count >= min_count}

    return filtered_counts


test_text = "St. Paul is a city. Mr. Smith lives on 1st St. near Dr. Jones."
print(count_words(test_text))
