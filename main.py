from section_parser import extract_sections
from word_counter import count_words, DEFAULT_STOP_WORDS
from visualizer import plot_top_words
from exporter import export_word_counts_to_csv
import os

def process_pdf(file_path, min_count=3, extra_stopwords=None, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output folder exists

    sections = extract_sections(file_path)

    # Print the first 100 characters of each section as a preview
    for section, content in sections.items():
        print(f"\nSection: {section}")
        print(content[:100])

    combined_stopwords = DEFAULT_STOP_WORDS.copy()
    if extra_stopwords:
        combined_stopwords.update(extra_stopwords)

    word_counts = {}
    for section, content in sections.items():
        counts = count_words(content, min_count=min_count, additional_stopwords=combined_stopwords)
        word_counts[section] = counts

    # Save CSV and plot inside the output folder
    csv_path = export_word_counts_to_csv(word_counts, output_file=os.path.join(output_dir, "word_counts.csv"))
    plot_path = plot_top_words(word_counts, output_dir=output_dir)

    return csv_path, plot_path


def main():
    pdf_file = r"C:\Users\lynch\Downloads\test document pdf (1).pdf"

    try:
        min_count = int(input("Enter minimum word count to include (default 3): ") or 3)
    except ValueError:
        print("Invalid input, using default minimum count = 3")
        min_count = 3

    extra = input("Enter extra stop words to exclude, separated by commas (or leave blank): ").strip()
    extra_stopwords = {w.strip().lower() for w in extra.split(",")} if extra else set()

    csv_path, plot_path = process_pdf(pdf_file, min_count, extra_stopwords)
    print(f"\nExported CSV to: {csv_path}")        
    print(f"Plot saved to: {plot_path}")
       
    print(f"Plot saved to: {plot_path}")

if __name__ == "__main__":
    main()

