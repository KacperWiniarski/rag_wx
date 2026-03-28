# 📘 Instalacja i Uruchomienie RAG System - Przewodnik Krok Po Kroku

## 📋 Spis treści
1. [Wymagania systemowe](#wymagania-systemowe)
2. [Instalacja Python i narzędzi](#instalacja-python-i-narzędzi)
3. [Pobranie projektu](#pobranie-projektu)
4. [Konfiguracja środowiska wirtualnego](#konfiguracja-środowiska-wirtualnego)
5. [Instalacja zależności](#instalacja-zależności)
6. [Instalacja Tesseract OCR](#instalacja-tesseract-ocr)
7. [Konfiguracja kluczy API](#konfiguracja-kluczy-api)
8. [Konfiguracja Elasticsearch](#konfiguracja-elasticsearch)
9. [Pierwsze uruchomienie](#pierwsze-uruchomienie)
10. [Testowanie aplikacji](#testowanie-aplikacji)
11. [Rozwiązywanie problemów](#rozwiązywanie-problemów)

---

## 1. Wymagania systemowe

### Minimalne wymagania:
- **System operacyjny:** Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+
- **RAM:** 8 GB (zalecane 16 GB)
- **Procesor:** Dual-core 2.0 GHz+
- **Miejsce na dysku:** 5 GB wolnego miejsca
- **Połączenie internetowe:** Wymagane (do API Watsonx.ai i Elasticsearch)

### Wymagane oprogramowanie:
- Python 3.10 lub nowszy
- Git
- Tesseract OCR (dla przetwarzania PDF)
- Edytor tekstu (np. VS Code, Notepad++)

---

## 2. Instalacja Python i narzędzi

### Windows:

#### Krok 2.1: Instalacja Python
1. Pobierz Python z oficjalnej strony: https://www.python.org/downloads/
2. Uruchom instalator
3. **WAŻNE:** Zaznacz opcję "Add Python to PATH"
4. Kliknij "Install Now"
5. Poczekaj na zakończenie instalacji

#### Krok 2.2: Weryfikacja instalacji Python
Otwórz PowerShell lub Command Prompt i wykonaj:
```powershell
python --version
```
Powinieneś zobaczyć: `Python 3.10.x` lub nowszy

```powershell
pip --version
```
Powinieneś zobaczyć wersję pip

#### Krok 2.3: Instalacja Git
1. Pobierz Git z: https://git-scm.com/download/win
2. Uruchom instalator z domyślnymi ustawieniami
3. Weryfikacja:
```powershell
git --version
```

### Linux (Ubuntu/Debian):

```bash
# Aktualizacja systemu
sudo apt update && sudo apt upgrade -y

# Instalacja Python 3.10+
sudo apt install python3 python3-pip python3-venv -y

# Instalacja Git
sudo apt install git -y

# Weryfikacja
python3 --version
pip3 --version
git --version
```

### macOS:

```bash
# Instalacja Homebrew (jeśli nie masz)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalacja Python
brew install python@3.10

# Instalacja Git
brew install git

# Weryfikacja
python3 --version
pip3 --version
git --version
```

---

## 3. Pobranie projektu

### Krok 3.1: Wybierz lokalizację
Otwórz terminal/PowerShell i przejdź do katalogu, gdzie chcesz mieć projekt:

**Windows:**
```powershell
cd C:\Users\TwojaNazwa\Documents
```

**Linux/Mac:**
```bash
cd ~/Documents
```

### Krok 3.2: Sklonuj repozytorium
```bash
git clone <URL_TWOJEGO_REPOZYTORIUM>
cd RAG_ws_es
```

Lub jeśli masz już projekt lokalnie, po prostu przejdź do jego katalogu:
```bash
cd c:/Users/kacper/OneDrive\ -\ TDSYNNEX/Desktop/Dlab/RAG_ws_es
```

### Krok 3.3: Sprawdź strukturę projektu
```bash
# Windows
dir

# Linux/Mac
ls -la
```

Powinieneś zobaczyć:
- `app.py`
- `requirements.txt`
- `README.md`
- Katalogi: `config/`, `ingestion/`, `retrieval/`, `frontend/`

---

## 4. Konfiguracja środowiska wirtualnego

### Dlaczego środowisko wirtualne?
Środowisko wirtualne izoluje zależności projektu od systemowego Pythona, zapobiegając konfliktom.

### Krok 4.1: Utwórz środowisko wirtualne

**Windows:**
```powershell
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

### Krok 4.2: Aktywuj środowisko wirtualne

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Krok 4.3: Weryfikacja aktywacji
Po aktywacji powinieneś zobaczyć `(venv)` na początku linii w terminalu:
```
(venv) C:\Users\kacper\...\RAG_ws_es>
```

### ⚠️ WAŻNE:
Zawsze aktywuj środowisko wirtualne przed pracą z projektem!

---

## 5. Instalacja zależności

### Krok 5.1: Aktualizacja pip
```bash
python -m pip install --upgrade pip
```

### Krok 5.2: Instalacja wszystkich pakietów
```bash
pip install -r requirements.txt
```

To zainstaluje:
- ✅ Streamlit (interfejs webowy)
- ✅ Elasticsearch (baza wektorowa)
- ✅ IBM Watsonx.ai (LLM i embeddingi)
- ✅ PyTesseract (OCR)
- ✅ PDF2Image (przetwarzanie PDF)
- ✅ Sentence-transformers (embeddingi)
- ✅ I inne zależności...

**Czas instalacji:** 5-10 minut (zależy od połączenia internetowego)

### Krok 5.3: Weryfikacja instalacji
```bash
pip list
```

Sprawdź czy zainstalowane są kluczowe pakiety:
- `streamlit`
- `elasticsearch`
- `ibm-watsonx-ai`
- `pytesseract`
- `pdf2image`

---

## 6. Instalacja Tesseract OCR

Tesseract jest wymagany do przetwarzania skanowanych PDF-ów.

### Windows:

#### Krok 6.1: Pobierz instalator
1. Przejdź do: https://github.com/UB-Mannheim/tesseract/wiki
2. Pobierz najnowszą wersję (np. `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

#### Krok 6.2: Zainstaluj Tesseract
1. Uruchom instalator
2. **WAŻNE:** Zapamiętaj ścieżkę instalacji (domyślnie: `C:\Program Files\Tesseract-OCR`)
3. Zaznacz opcję instalacji języków (wybierz przynajmniej angielski i polski)
4. Dokończ instalację

#### Krok 6.3: Dodaj Tesseract do PATH
1. Otwórz "Ustawienia systemu" → "System" → "Informacje o systemie"
2. Kliknij "Zaawansowane ustawienia systemu"
3. Kliknij "Zmienne środowiskowe"
4. W sekcji "Zmienne systemowe" znajdź `Path` i kliknij "Edytuj"
5. Kliknij "Nowy" i dodaj: `C:\Program Files\Tesseract-OCR`
6. Kliknij "OK" we wszystkich oknach
7. **Uruchom ponownie terminal/PowerShell**

#### Krok 6.4: Weryfikacja
```powershell
tesseract --version
```

Powinieneś zobaczyć wersję Tesseract.

### Linux (Ubuntu/Debian):

```bash
# Instalacja Tesseract z językami
sudo apt install tesseract-ocr tesseract-ocr-pol tesseract-ocr-eng -y

# Instalacja poppler-utils (dla pdf2image)
sudo apt install poppler-utils -y

# Weryfikacja
tesseract --version
```

### macOS:

```bash
# Instalacja Tesseract
brew install tesseract tesseract-lang

# Instalacja poppler (dla pdf2image)
brew install poppler

# Weryfikacja
tesseract --version
```

---

## 7. Konfiguracja kluczy API

### Krok 7.1: Uzyskaj klucze API

#### Watsonx.ai:
1. Zaloguj się do IBM Cloud: https://cloud.ibm.com/
2. Przejdź do **Manage → Access (IAM) → API keys**
3. Kliknij **Create an IBM Cloud API key**
4. Nadaj nazwę (np. "RAG-System-Key")
5. Kliknij **Create**
6. **WAŻNE:** Skopiuj klucz i zapisz w bezpiecznym miejscu (nie będziesz mógł go ponownie zobaczyć!)

#### Watsonx Project ID:
1. Przejdź do watsonx.ai: https://dataplatform.cloud.ibm.com/
2. Otwórz swój projekt
3. Kliknij **Manage** → **General**
4. Skopiuj **Project ID**

#### Elasticsearch:
1. Zaloguj się do Elastic Cloud: https://cloud.elastic.co/
2. Otwórz swój deployment
3. Przejdź do **Security → API keys**
4. Kliknij **Create API key**
5. Nadaj nazwę (np. "RAG-System")
6. Wybierz odpowiednie uprawnienia (read/write)
7. Kliknij **Create API key**
8. Skopiuj klucz i zapisz bezpiecznie

#### Elasticsearch URL:
1. W Elastic Cloud Console
2. Skopiuj **Elasticsearch endpoint** (np. `https://xxx.es.eu-central-1.aws.elastic.cloud:443`)

### Krok 7.2: Utwórz plik .env

**Windows:**
```powershell
copy config\env.example .env
```

**Linux/Mac:**
```bash
cp config/env.example .env
```

### Krok 7.3: Edytuj plik .env

Otwórz plik `.env` w edytorze tekstu i wypełnij swoimi danymi:

```bash
# Watsonx.ai
WATSONX_API_KEY=TWOJ_KLUCZ_API_WATSONX
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
WATSONX_PROJECT_ID=TWOJ_PROJECT_ID
LLM_MODEL_ID=meta-llama/llama-4-maverick-17b-128e-instruct-fp8
EMBED_MODEL_ID=intfloat/multilingual-e5-large

# Elasticsearch serverless
ES_URL=TWOJ_ELASTICSEARCH_URL
ES_API_KEY=TWOJ_KLUCZ_API_ELASTICSEARCH
ES_INDEX=rag-documents
```

**Przykład wypełnionego pliku:**
```bash
# Watsonx.ai
WATSONX_API_KEY=abc123XYZ789_example_key_do_not_share
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
WATSONX_PROJECT_ID=82b92519-b5fa-4b80-a8a0-0247f1e2bedf
LLM_MODEL_ID=meta-llama/llama-4-maverick-17b-128e-instruct-fp8
EMBED_MODEL_ID=intfloat/multilingual-e5-large

# Elasticsearch serverless
ES_URL=https://my-project.es.eu-central-1.aws.elastic.cloud:443
ES_API_KEY=ZnlJenlwb0I2WjJRYmstdnlzVkc6eFZsMjFod2dFVUxXYnpEWGs1RVNhZw==
ES_INDEX=rag-documents
```

### Krok 7.4: Weryfikacja pliku .env

**Windows:**
```powershell
Get-Content .env
```

**Linux/Mac:**
```bash
cat .env
```

Upewnij się, że:
- ✅ Wszystkie zmienne są wypełnione
- ✅ Brak spacji wokół znaku `=`
- ✅ Brak cudzysłowów wokół wartości
- ✅ Plik znajduje się w głównym katalogu projektu (nie w `config/`)

### ⚠️ BEZPIECZEŃSTWO:
- **NIGDY** nie commituj pliku `.env` do Git!
- **NIGDY** nie udostępniaj kluczy API publicznie!
- Plik `.env` jest już w `.gitignore`

---

## 8. Konfiguracja Elasticsearch

### Krok 8.1: Sprawdź wymiary embeddingów

Domyślny model `intfloat/multilingual-e5-large` używa **1024 wymiarów**.

Otwórz plik `config/es_config.py` i sprawdź:
```python
"embedding": {
    "type": "dense_vector",
    "dims": 1024,  # ← To musi być 1024 dla multilingual-e5-large
    "index": True,
    "similarity": "cosine"
}
```

### Krok 8.2: Testowe połączenie z Elasticsearch

Utwórz plik testowy `test_es_connection.py`:
```python
from config.es_config import get_es

try:
    es = get_es()
    info = es.info()
    print("✅ Połączenie z Elasticsearch udane!")
    print(f"Wersja: {info['version']['number']}")
except Exception as e:
    print(f"❌ Błąd połączenia: {e}")
```

Uruchom test:
```bash
python test_es_connection.py
```

### Krok 8.3: Utwórz indeks (opcjonalnie)

Indeks zostanie utworzony automatycznie przy pierwszym uploadzię, ale możesz go utworzyć ręcznie:

```python
from config.es_config import get_es, get_index_mapping

es = get_es()
index_name = "rag-documents"

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=get_index_mapping())
    print(f"✅ Indeks {index_name} utworzony!")
else:
    print(f"ℹ️ Indeks {index_name} już istnieje")
```

---

## 9. Pierwsze uruchomienie

### Krok 9.1: Upewnij się, że środowisko wirtualne jest aktywne
Powinieneś widzieć `(venv)` w terminalu.

### Krok 9.2: Uruchom aplikację
```bash
streamlit run app.py
```

### Krok 9.3: Otwórz aplikację w przeglądarce

Streamlit automatycznie otworzy przeglądarkę. Jeśli nie, przejdź do:
```
http://localhost:8501
```

### Krok 9.4: Sprawdź interfejs

Powinieneś zobaczyć:
- 🎯 Sidebar z menu: "Upload" i "Chat"
- 📄 Główny obszar aplikacji

---

## 10. Testowanie aplikacji

### Test 1: Upload dokumentu (TXT)

#### Krok 10.1: Przygotuj testowy plik
Utwórz plik `test_document.txt` z treścią:
```
Sztuczna inteligencja (AI) to dziedzina informatyki zajmująca się tworzeniem 
systemów zdolnych do wykonywania zadań wymagających ludzkiej inteligencji.

Machine Learning jest poddziedziną AI, która pozwala systemom uczyć się 
z danych bez jawnego programowania.

Deep Learning wykorzystuje sieci neuronowe do rozpoznawania wzorców w danych.
```

#### Krok 10.2: Upload pliku
1. W aplikacji wybierz **Upload** z menu
2. Kliknij **Browse files**
3. Wybierz `test_document.txt`
4. Kliknij **Upload and Process**

#### Krok 10.3: Sprawdź wyniki
Powinieneś zobaczyć:
- ✅ "Processing file..."
- ✅ "Splitting into chunks..."
- ✅ "Generating embeddings..."
- ✅ "Indexing to Elasticsearch..."
- ✅ "Success! Document indexed."

### Test 2: Chat RAG

#### Krok 10.4: Przejdź do Chat
1. Wybierz **Chat** z menu
2. W polu tekstowym wpisz: "Co to jest machine learning?"
3. Kliknij **Send** lub naciśnij Enter

#### Krok 10.5: Sprawdź odpowiedź
Powinieneś zobaczyć:
- 🔍 Znalezione konteksty z dokumentu
- 💬 Odpowiedź wygenerowaną przez LLM
- 📚 Źródła (chunks z dokumentu)

### Test 3: Upload PDF (opcjonalnie)

Jeśli masz zainstalowany Tesseract:
1. Przygotuj prosty PDF
2. Upload przez interfejs
3. Sprawdź czy OCR działa (dla skanów)

---

## 11. Rozwiązywanie problemów

### Problem 1: "ModuleNotFoundError: No module named 'streamlit'"

**Przyczyna:** Środowisko wirtualne nie jest aktywne lub pakiety nie są zainstalowane.

**Rozwiązanie:**
```bash
# Aktywuj venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Zainstaluj ponownie
pip install -r requirements.txt
```

### Problem 2: "Missing required environment variables"

**Przyczyna:** Plik `.env` nie istnieje lub jest pusty.

**Rozwiązanie:**
```bash
# Sprawdź czy plik istnieje
ls .env  # Linux/Mac
dir .env # Windows

# Jeśli nie istnieje, utwórz go
cp config/env.example .env

# Wypełnij swoimi kluczami API
```

### Problem 3: "Elasticsearch connection failed"

**Przyczyna:** Błędny URL lub klucz API Elasticsearch.

**Rozwiązanie:**
1. Sprawdź `ES_URL` w `.env` - musi zawierać `https://` i port `:443`
2. Sprawdź `ES_API_KEY` - skopiuj ponownie z Elastic Cloud
3. Sprawdź połączenie internetowe
4. Sprawdź czy deployment Elasticsearch jest aktywny

### Problem 4: "Watsonx authentication failed"

**Przyczyna:** Błędny klucz API lub Project ID.

**Rozwiązanie:**
1. Zweryfikuj `WATSONX_API_KEY` w IBM Cloud Console
2. Sprawdź `WATSONX_PROJECT_ID` w watsonx.ai
3. Upewnij się, że klucz ma odpowiednie uprawnienia

### Problem 5: "Dimension mismatch" w Elasticsearch

**Przyczyna:** Wymiary embeddingów nie zgadzają się z konfiguracją indeksu.

**Rozwiązanie:**
```python
# Usuń stary indeks
from config.es_config import get_es
es = get_es()
es.indices.delete(index="rag-documents")

# Uruchom aplikację ponownie - indeks zostanie utworzony z poprawnymi wymiarami
```

### Problem 6: "Tesseract not found"

**Przyczyna:** Tesseract nie jest zainstalowany lub nie jest w PATH.

**Rozwiązanie Windows:**
1. Zainstaluj Tesseract (patrz sekcja 6)
2. Dodaj do PATH: `C:\Program Files\Tesseract-OCR`
3. Uruchom ponownie terminal
4. Sprawdź: `tesseract --version`

**Rozwiązanie Linux:**
```bash
sudo apt install tesseract-ocr tesseract-ocr-pol -y
```

### Problem 7: "Port 8501 already in use"

**Przyczyna:** Inna instancja Streamlit już działa.

**Rozwiązanie:**
```bash
# Znajdź i zakończ proces
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8501 | xargs kill -9

# Lub użyj innego portu
streamlit run app.py --server.port 8502
```

### Problem 8: Wolne generowanie embeddingów

**Przyczyna:** Duże pliki lub wolne połączenie z Watsonx.ai.

**Rozwiązanie:**
- Podziel duże dokumenty na mniejsze pliki
- Sprawdź połączenie internetowe
- Rozważ użycie lokalnego modelu embeddingów (wymaga modyfikacji kodu)

### Problem 9: "PDF processing failed"

**Przyczyna:** Uszkodzony PDF lub brak Tesseract.

**Rozwiązanie:**
1. Sprawdź czy PDF nie jest uszkodzony (otwórz w Adobe Reader)
2. Dla skanów upewnij się, że Tesseract jest zainstalowany
3. Spróbuj najpierw z prostym plikiem TXT
4. Sprawdź logi w terminalu dla szczegółów błędu

### Problem 10: Aplikacja się zawiesza

**Rozwiązanie:**
1. Naciśnij `Ctrl+C` w terminalu aby zatrzymać
2. Sprawdź logi w terminalu
3. Sprawdź połączenie z Elasticsearch i Watsonx
4. Uruchom ponownie: `streamlit run app.py`

---

## 📚 Dodatkowe zasoby

### Dokumentacja:
- **Streamlit:** https://docs.streamlit.io/
- **Elasticsearch:** https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
- **IBM Watsonx.ai:** https://www.ibm.com/docs/en/watsonx-as-a-service
- **Tesseract OCR:** https://github.com/tesseract-ocr/tesseract

### Pliki w projekcie:
- `README.md` - Ogólny opis projektu
- `CHECKLIST_PRZED_URUCHOMIENIEM.md` - Checklist bezpieczeństwa
- `IMPROVEMENTS.md` - Planowane ulepszenia
- `PDF_SUPPORT.md` - Szczegóły obsługi PDF
- `SECURITY.md` - Wytyczne bezpieczeństwa

---

## ✅ Checklist końcowy

Przed rozpoczęciem pracy upewnij się, że:

- [ ] Python 3.10+ zainstalowany i w PATH
- [ ] Git zainstalowany
- [ ] Projekt pobrany/sklonowany
- [ ] Środowisko wirtualne utworzone i aktywne
- [ ] Wszystkie pakiety zainstalowane (`pip install -r requirements.txt`)
- [ ] Tesseract OCR zainstalowany (dla PDF)
- [ ] Plik `.env` utworzony i wypełniony
- [ ] Klucze API Watsonx.ai działają
- [ ] Klucze API Elasticsearch działają
- [ ] Połączenie z Elasticsearch działa
- [ ] Aplikacja uruchamia się bez błędów
- [ ] Test upload dokumentu przeszedł pomyślnie
- [ ] Test chat RAG działa poprawnie

---

## 🎉 Gratulacje!

Jeśli wszystkie kroki zostały wykonane pomyślnie, Twój system RAG jest gotowy do użycia!

### Następne kroki:
1. 📄 Zaindeksuj swoje dokumenty przez interfejs Upload
2. 💬 Zadawaj pytania w interfejsie Chat
3. 🔧 Dostosuj konfigurację w plikach `config/`
4. 📈 Monitoruj wydajność i optymalizuj

### Potrzebujesz pomocy?
- Sprawdź sekcję [Rozwiązywanie problemów](#11-rozwiązywanie-problemów)
- Przeczytaj `IMPROVEMENTS.md` dla dodatkowych wskazówek
- Sprawdź logi w terminalu dla szczegółowych informacji o błędach

---

**Wersja dokumentu:** 1.0  
**Data ostatniej aktualizacji:** 2026-03-05  
**Autor:** RAG System Team