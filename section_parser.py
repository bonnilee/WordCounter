import fitz  # PyMuPDF
import os

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

def extract_sections(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    doc = fitz.open(pdf_path)
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

    for sec in sections:
        sections[sec] = sections[sec].strip()

    return sections



