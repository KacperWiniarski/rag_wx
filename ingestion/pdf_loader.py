import PyPDF2
from ingestion.ocr_utils import pdf_to_text_ocr

def load_pdf(pdf_path):
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        if text.strip():
            return text
        return pdf_to_text_ocr(pdf_path)
    except:
        return pdf_to_text_ocr(pdf_path)
