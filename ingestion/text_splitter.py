def split_text(text, chunk_size=1024, overlap=500):
    """
    Dzieli tekst na nakładające się fragmenty.
    
    :param text: tekst wejściowy
    :param chunk_size: długość jednego chunku
    :param overlap: liczba znaków nakładki pomiędzy chunkami
    :return: lista fragmentów tekstu
    """

    if overlap >= chunk_size:
        raise ValueError("overlap musi być mniejszy niż chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # przesunięcie o chunk_size - overlap

    return chunks