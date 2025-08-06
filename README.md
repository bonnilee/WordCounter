# 🧠 PDF Word Search Flask App

This web application allows users to upload a PDF document and search for specific word occurrences by section. It extracts headers based on font styles and generates a chart showing the count of each search term per section.

## 📦 Features

- Upload and parse PDF documents
- Automatically detect and separate sections using font headers
- Clean text using NLTK stopwords
- Search for a specific word
- View word frequency per section in a chart

## 🛠 Technologies Used

- Python
- Flask
- pdfminer.six
- NLTK
- Matplotlib
- Pandas
- HTML/CSS (Jinja templates)

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pdf-word-search-app.git
   cd pdf-word-search-app
