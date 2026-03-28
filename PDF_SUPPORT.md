# 📄 Obsługa plików PDF

## ✅ Zaimplementowane funkcje

System RAG obsługuje teraz pełną obsługę plików PDF z następującymi funkcjami:

### 1. **Automatyczna detekcja typu PDF**
- **PDF z tekstem:** Bezpośrednia ekstrakcja tekstu za pomocą PyPDF2
- **PDF skanowany:** Automatyczne przełączenie na OCR (Tesseract)
- **PDF hybrydowy:** Próba ekstrakcji tekstu, fallback do OCR jeśli potrzebne

### 2. **Obsługa różnych źródeł plików**
- ✅ Ścieżka do pliku (str)
- ✅ Streamlit UploadedFile
- ✅ BytesIO objects

### 3. **OCR dla skanowanych PDF**
- Konwersja PDF → obrazy (300 DPI)
- OCR z Tesseract
- Obsługa wielu języków (angielski + polski)
- Oznaczanie numerów stron w tekście

### 4. **Ulepszona obsługa błędów**
- Szczegółowe komunikaty błędów
- Graceful fallback (tekst → OCR)
- Walidacja pustych plików
- Informacje o postępie w UI

## 📦 Wymagania

### Podstawowe (już w requirements.txt)
```
PyPDF2
pdf2image
pytesseract
Pillow
```

### Systemowe - Tesseract OCR

#### Windows
1. Pobierz instalator: https://github.com/UB-Mannheim/tesseract/wiki
2. Zainstaluj (domyślnie: `C:\Program Files\Tesseract-OCR`)
3. Dodaj do PATH:
   ```powershell
   $env:Path += ";C:\Program Files\Tesseract-OCR"
   ```
4. Sprawdź instalację:
   ```powershell
   tesseract --version
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-pol
tesseract --version
```

#### macOS
```bash
brew install tesseract tesseract-lang
tesseract --version
```

## 🚀 Użycie

### W aplikacji Streamlit

1. Uruchom aplikację:
   ```bash
   streamlit run app.py
   ```

2. Przejdź do zakładki **Upload**

3. Wybierz pliki:
   - Obsługiwane: `.txt`, `.pdf`
   - Możesz wybrać wiele plików naraz

4. System automatycznie:
   - Wykryje typ pliku
   - Wyekstrahuje tekst (lub użyje OCR)
   - Podzieli na chunki
   - Wygeneruje embeddingi
   - Zaindeksuje w Elasticsearch

### Programowo

```python
from ingestion.file_loader import load_file

# Załaduj PDF
chunks = load_file("document.pdf")

# Lub z custom parametrami
chunks = load_file(
    "document.pdf",
    chunk_size=2048,  # większe chunki
    overlap=400       # większe nakładanie
)

# Wynik: lista stringów (chunków tekstu)
print(f"Created {len(chunks)} chunks")
```

### Bezpośrednio z PDF loader

```python
from ingestion.pdf_loader import load_pdf

# Załaduj cały tekst z PDF
text = load_pdf("document.pdf")

# Lub z file object
with open("document.pdf", "rb") as f:
    text = load_pdf(f)
```

### Tylko OCR

```python
from ingestion.ocr_utils import pdf_to_text_ocr

# Wymuś OCR (dla skanów)
text = pdf_to_text_ocr("scanned_document.pdf")
```

## 📊 Przykłady użycia

### Przykład 1: Pojedynczy PDF
```python
from ingestion.file_loader import load_file
from config.watsonx_config import get_embedding_model
from ingestion.ingest_to_es import ingest_document

# 1. Załaduj i podziel na chunki
chunks = load_file("raport.pdf")
print(f"Chunks: {len(chunks)}")

# 2. Wygeneruj embeddingi
embed_model = get_embedding_model()
embeddings = embed_model(chunks)

# 3. Zaindeksuj w Elasticsearch
chunks_with_metadata = [
    {"file": "raport.pdf", "text": chunk}
    for chunk in chunks
]
response = ingest_document(chunks_with_metadata, embeddings)
print("Indexed:", response)
```

### Przykład 2: Batch processing
```python
import os
from pathlib import Path

pdf_dir = Path("documents/")
all_chunks = []

for pdf_file in pdf_dir.glob("*.pdf"):
    try:
        chunks = load_file(str(pdf_file))
        chunks_with_metadata = [
            {"file": pdf_file.name, "text": chunk}
            for chunk in chunks
        ]
        all_chunks.extend(chunks_with_metadata)
        print(f"✅ {pdf_file.name}: {len(chunks)} chunks")
    except Exception as e:
        print(f"❌ {pdf_file.name}: {e}")

print(f"\nTotal: {len(all_chunks)} chunks from {len(list(pdf_dir.glob('*.pdf')))} files")
```

## 🔧 Konfiguracja

### Parametry chunkowania

W `ingestion/file_loader.py`:
```python
chunks = load_file(
    file,
    chunk_size=1024,  # Rozmiar chunka w znakach
    overlap=200       # Nakładanie między chunkami
)
```

**Rekomendacje:**
- **Krótkie dokumenty:** `chunk_size=512, overlap=100`
- **Standardowe:** `chunk_size=1024, overlap=200` (domyślne)
- **Długie dokumenty:** `chunk_size=2048, overlap=400`

### Języki OCR

W `ingestion/ocr_utils.py`:
```python
# Zmień linię 44:
page_text = pytesseract.image_to_string(page, lang='eng+pol')

# Dostępne języki:
# - 'eng' - angielski
# - 'pol' - polski
# - 'deu' - niemiecki
# - 'fra' - francuski
# - 'spa' - hiszpański
# Pełna lista: tesseract --list-langs
```

### Jakość OCR

W `ingestion/ocr_utils.py`:
```python
# Zmień DPI (linia 35 i 39):
pages = convert_from_path(pdf_file, dpi=300)  # Wyższa jakość = wolniej

# Opcje:
# - dpi=150: Szybko, niska jakość
# - dpi=300: Standardowo (domyślne)
# - dpi=600: Wysoka jakość, wolno
```

## 🐛 Rozwiązywanie problemów

### Problem: "Tesseract not found"
**Przyczyna:** Tesseract nie jest zainstalowany lub nie jest w PATH

**Rozwiązanie:**
1. Zainstaluj Tesseract (patrz sekcja Wymagania)
2. Dodaj do PATH
3. Zrestartuj terminal/IDE

### Problem: "PDF processing failed"
**Możliwe przyczyny:**
- Uszkodzony plik PDF
- Brak uprawnień do odczytu
- PDF chroniony hasłem

**Rozwiązanie:**
1. Sprawdź czy plik otwiera się w PDF reader
2. Usuń ochronę hasłem
3. Spróbuj z innym plikiem

### Problem: OCR zwraca śmieci
**Przyczyna:** Niska jakość skanu lub niewłaściwy język

**Rozwiązanie:**
1. Zwiększ DPI: `dpi=600`
2. Dodaj właściwy język: `lang='pol'`
3. Popraw jakość skanu przed przetwarzaniem

### Problem: Wolne przetwarzanie
**Przyczyna:** OCR jest wolny dla dużych plików

**Rozwiązanie:**
1. Zmniejsz DPI: `dpi=150`
2. Przetwarzaj mniejsze pliki
3. Użyj PDF z tekstem zamiast skanów

## 📈 Wydajność

### Benchmarki (przykładowe)

| Typ PDF | Strony | Czas | Metoda |
|---------|--------|------|--------|
| Tekst | 10 | ~2s | PyPDF2 |
| Tekst | 100 | ~15s | PyPDF2 |
| Skan (300 DPI) | 10 | ~45s | OCR |
| Skan (300 DPI) | 100 | ~7min | OCR |

**Wskazówki optymalizacji:**
- Preferuj PDF z tekstem nad skanami
- Dla skanów: użyj niższego DPI jeśli jakość pozwala
- Przetwarzaj duże pliki w tle (batch processing)

## 🎯 Najlepsze praktyki

1. **Testuj z małymi plikami najpierw**
   ```python
   # Test z 1-2 stronowym PDF
   chunks = load_file("test.pdf")
   ```

2. **Waliduj wyniki**
   ```python
   chunks = load_file("document.pdf")
   print(f"Chunks: {len(chunks)}")
   print(f"First chunk preview: {chunks[0][:200]}...")
   ```

3. **Obsługuj błędy**
   ```python
   try:
       chunks = load_file("document.pdf")
   except Exception as e:
       print(f"Error: {e}")
       # Fallback lub retry
   ```

4. **Monitoruj jakość OCR**
   ```python
   text = pdf_to_text_ocr("scan.pdf")
   if len(text) < 100:
       print("Warning: Very short text extracted, check OCR quality")
   ```

## 📚 Dodatkowe zasoby

- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [pytesseract](https://github.com/madmaze/pytesseract)

## 🆘 Wsparcie

Jeśli masz problemy z obsługą PDF:
1. Sprawdź logi w terminalu
2. Przetestuj z prostym plikiem TXT najpierw
3. Sprawdź czy Tesseract jest zainstalowany: `tesseract --version`
4. Zobacz `CHECKLIST_PRZED_URUCHOMIENIEM.md` dla szczegółów

---

**Status:** ✅ Pełna obsługa PDF zaimplementowana i przetestowana