import csv
import os

def export_word_counts_to_csv(word_counts, output_file="results/word_counts.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Section", "Word", "Count"])
        for section, counts in word_counts.items():
            for word, count in counts.items():
                writer.writerow([section, word, count])
    return output_file  # return the filename/path
