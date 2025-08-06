import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import os

def plot_top_words(word_counts, output_dir='static/plots', filename='top_words.png', top_n=10):
    """
    Plots a bar chart of the top N words and saves it to a file.
    `word_counts` is a flat Counter or dict of {word: count}
    """
    if not word_counts:
        return None

    # Get top N words
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Count')
    plt.title('Top Words Across Document')
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches='tight')


    plt.close()

    return filepath

