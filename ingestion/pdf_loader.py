import PyPDF2
import io
from ingestion.ocr_utils import pdf_to_text_ocr

def load_pdf(pdf_file):
    """
    Load text from a PDF file. Tries to extract text directly first,
    falls back to OCR if extraction fails or returns empty text.
    
    Args:
        pdf_file: Either a file path (str) or a file-like object (BytesIO/UploadedFile)
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        Exception: If both text extraction and OCR fail
    """
    try:
        # Handle file path vs file object
        if isinstance(pdf_file, str):
            # File path
            with open(pdf_file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = _extract_text_from_reader(reader)
        else:
            # File object (Streamlit UploadedFile or BytesIO)
            # Reset file pointer to beginning
            pdf_file.seek(0)
            reader = PyPDF2.PdfReader(pdf_file)
            text = _extract_text_from_reader(reader)
        
        # If text extraction successful, return it
        if text.strip():
            return text
        
        # Otherwise, try OCR
        return pdf_to_text_ocr(pdf_file)
        
    except Exception as e:
        # If text extraction fails, try OCR
        try:
            return pdf_to_text_ocr(pdf_file)
        except Exception as ocr_error:
            raise Exception(f"Failed to load PDF. Text extraction error: {e}, OCR error: {ocr_error}")

def _extract_text_from_reader(reader):
    """
    Extract text from all pages of a PDF reader object.
    
    Args:
        reader: PyPDF2.PdfReader object
        
    Returns:
        str: Concatenated text from all pages
    """
    text = ""
    for page_num, page in enumerate(reader.pages):
        try:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        except Exception as e:
            print(f"Warning: Failed to extract text from page {page_num + 1}: {e}")
            continue
    return text
