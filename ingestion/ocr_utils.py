import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
import io

def pdf_to_text_ocr(pdf_file):
    """
    Extract text from a PDF using OCR (Optical Character Recognition).
    Useful for scanned PDFs or PDFs without embedded text.
    
    Args:
        pdf_file: Either a file path (str) or a file-like object (BytesIO/UploadedFile)
        
    Returns:
        str: Extracted text from all pages
        
    Raises:
        Exception: If OCR processing fails
        
    Note:
        Requires Tesseract OCR to be installed on the system.
        - Windows: https://github.com/UB-Mannheim/tesseract/wiki
        - Linux: sudo apt install tesseract-ocr
        - Mac: brew install tesseract
    """
    try:
        # Handle file path vs file object
        if isinstance(pdf_file, str):
            # File path - use convert_from_path
            pages = convert_from_path(pdf_file, dpi=300)
        else:
            # File object - read bytes and use convert_from_bytes
            pdf_file.seek(0)
            pdf_bytes = pdf_file.read()
            pages = convert_from_bytes(pdf_bytes, dpi=300)
        
        # Extract text from each page
        text = ""
        for page_num, page in enumerate(pages, start=1):
            try:
                page_text = pytesseract.image_to_string(page, lang='eng+pol')  # English + Polish
                text += f"\n--- Page {page_num} ---\n{page_text}\n"
            except Exception as e:
                print(f"Warning: OCR failed for page {page_num}: {e}")
                continue
        
        return text.strip()
        
    except Exception as e:
        raise Exception(f"OCR processing failed: {e}. Make sure Tesseract is installed.")
