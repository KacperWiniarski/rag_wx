import os
from ingestion.pdf_loader import load_pdf

def load_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return load_pdf(path)
    elif ext == ".txt":
        return open(path, "r", encoding="utf-8").read()
    else:
        raise Exception(f"Unsupported file type: {ext}")
