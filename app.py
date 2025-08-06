from flask import Flask, render_template, request, flash
from flask import url_for
from werkzeug.utils import secure_filename
import os
from collections import Counter
import fitz  # PyMuPDF
import re
from nltk.corpus import stopwords
import nltk
from visualizer import plot_top_words  # your plotting function



app = Flask(__name__)
app.secret_key = 'supersecret'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Download stopwords once
nltk.download('stopwords')
STOP_WORDS = set(w.lower() for w in stopwords.words('english'))

def is_bold(span):
    if span.get("flags", 0) & 2:
        return True
    if "bold" in span.get("font", "").lower():
        return True
    return False

def is_likely_heading(text, size, span):
    if not text:
        return False

    bold = is_bold(span)

    if size < 12:
        return False

    if text.isupper():
        return True

    if text.istitle() and 1 <= len(text.split()) <= 10:
        if bold or size >= 13:
            return True

    if bold and len(text.split()) <= 10:
        return True

    return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)
            flash('File uploaded successfully!')

            min_count_str = request.form.get('min_count', '2')
            try:
                min_count = int(min_count_str)
            except ValueError:
                min_count = 2
                flash("Invalid minimum count input. Using default = 2.")

            extra_stopwords_raw = request.form.get('extra_stopwords', '').strip()
            extra_stopwords = {w.lower() for w in extra_stopwords_raw.split(",")} if extra_stopwords_raw else set()

            section_data, plot_path = extract_section_data_and_plot(filepath, min_count, extra_stopwords)

            # Get relative URL for plot image to serve
            plot_url = url_for('static', filename='plots/top_words.png')


            return render_template('upload.html', section_data=section_data,
                                   min_count=min_count,
                                   extra_stopwords=extra_stopwords_raw,
                                   plot_url=plot_url)

        else:
            flash('Please upload a valid PDF file.')

    return render_template('upload.html', section_data=None, min_count=2, extra_stopwords='')


def extract_section_data_and_plot(filepath, min_count=2, extra_stopwords=None):
    # Ensure extra stopwords are lowercase and a set
    extra_stopwords = set(w.strip().lower() for w in (extra_stopwords or []))

    # Combine with default stopwords (all lowercase)
    all_stopwords = STOP_WORDS.union(extra_stopwords)

    doc = fitz.open(filepath)
    sections = {}
    current_section = "Introduction"
    sections[current_section] = ""

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    size = span["size"]

                    if is_likely_heading(text, size, span):
                        current_section = text
                        if current_section not in sections:
                            sections[current_section] = ""
                    else:
                        sections[current_section] += text + " "

    section_data = {}
    combined_word_counts = Counter()

    for sec, content in sections.items():
        words = re.findall(r'\b[a-zA-Z]+\b', content.lower())
        word_count = len(words)
        preview = content[:100] + ("..." if len(content) > 100 else "")

        filtered_words = [w for w in words if w not in all_stopwords]
        counts = Counter(filtered_words)

        # Add to combined counts for the plot
        combined_word_counts.update(counts)

        top_words = [(word, cnt) for word, cnt in counts.most_common(10) if cnt >= min_count]

        section_data[sec] = {
            "word_count": word_count,
            "preview": preview,
            "top_words": top_words
        }

    # Create plots directory if needed
    plots_dir = os.path.join('static', 'plots')
    os.makedirs(plots_dir, exist_ok=True)

    plot_path = plot_top_words(combined_word_counts, output_dir=plots_dir, filename="top_words.png")

    return section_data, plot_path




if __name__ == '__main__':
    app.run(debug=True)




