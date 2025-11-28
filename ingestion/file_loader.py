import os

def load_file(file):
    # jeśli to ścieżka
    if isinstance(file, str):
        ext = os.path.splitext(file)[1].lower()
        if ext == ".txt":
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            raise Exception(f"Unsupported file type: {ext}")
    # jeśli to Streamlit uploaded file (BytesIO)
    else:
        ext = getattr(file, "name", "").split(".")[-1].lower()
        if ext == "txt":
            content = file.getvalue().decode("utf-8")
        else:
            raise Exception(f"Unsupported file type: {ext}")

    # prosty split na linie / chunky po np. 500 znaków
    chunk_size = 500
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    return chunks
