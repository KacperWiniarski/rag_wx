import os
from ingestion.text_splitter import split_text
from ingestion.pdf_loader import load_pdf
from config.env import CHUNK_SIZE, CHUNK_OVERLAP


def load_file(file, chunk_size=None, overlap=None):
    """
    Load and process a file (TXT or PDF) into text chunks.
    
    Args:
        file: Either a file path (str) or a file-like object (UploadedFile/BytesIO)
        chunk_size (int): Size of each text chunk in characters (domyślnie z env: CHUNK_SIZE)
        overlap (int): Number of overlapping characters between chunks (domyślnie z env: CHUNK_OVERLAP)
        
    Returns:
        list: List of text chunks
        
    Raises:
        Exception: If file type is unsupported or processing fails
        
    Supported formats:
        - TXT: Plain text files
        - PDF: Both text-based and scanned PDFs (with OCR)
    """
    # Use environment variables as defaults
    if chunk_size is None:
        chunk_size = CHUNK_SIZE
    if overlap is None:
        overlap = CHUNK_OVERLAP
    
    # Detect file extension
    if isinstance(file, str):
        # File path
        ext = os.path.splitext(file)[1].lower().replace(".", "")
        file_name = os.path.basename(file)
    else:
        # Uploaded file (UploadedFile / BytesIO)
        ext = file.name.split(".")[-1].lower()
        file_name = file.name
    
    # Load content based on file type
    try:
        if ext == "txt":
            content = _load_txt(file)
        elif ext == "pdf":
            content = load_pdf(file)
        else:
            raise Exception(f"Unsupported file type: .{ext}. Supported formats: TXT, PDF")
        
        # Validate content
        if not content or not content.strip():
            raise Exception(f"File '{file_name}' is empty or contains no extractable text")
        
        # Split into chunks
        chunks = split_text(content, chunk_size=chunk_size, overlap=overlap)
        
        if not chunks:
            raise Exception(f"Failed to create chunks from file '{file_name}'")
        
        return chunks
        
    except Exception as e:
        raise Exception(f"Error processing file '{file_name}': {str(e)}")

def _load_txt(file):
    """
    Load text from a TXT file.
    
    Args:
        file: Either a file path (str) or a file-like object
        
    Returns:
        str: File content
    """
    if isinstance(file, str):
        # File path
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        # File object
        try:
            # Try UTF-8 first
            return file.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            # Fallback to latin-1
            return file.getvalue().decode("latin-1")
