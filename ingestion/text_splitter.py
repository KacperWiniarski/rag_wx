from config.env import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text, chunk_size=None, overlap=None):
    """
    Dzieli tekst na nakładające się fragmenty.
    
    :param text: tekst wejściowy
    :param chunk_size: długość jednego chunku (domyślnie z env: CHUNK_SIZE)
    :param overlap: liczba znaków nakładki pomiędzy chunkami (domyślnie z env: CHUNK_OVERLAP)
    :return: lista fragmentów tekstu
    """
    # Use environment variables as defaults
    if chunk_size is None:
        chunk_size = CHUNK_SIZE
    if overlap is None:
        overlap = CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap musi być mniejszy niż chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # przesunięcie o chunk_size - overlap

    return chunks