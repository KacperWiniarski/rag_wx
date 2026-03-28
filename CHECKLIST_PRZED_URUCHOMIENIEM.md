# ✅ Checklist przed uruchomieniem aplikacji

## 🚨 KRYTYCZNE - Musisz to zrobić TERAZ

### 1. Zrotuj klucze API (NATYCHMIAST!)
Twoje klucze API były w repozytorium i są teraz publiczne. **MUSISZ je zrotować:**

#### Watsonx.ai:
1. Zaloguj się do [IBM Cloud Console](https://cloud.ibm.com/)
2. Przejdź do **Manage → Access (IAM) → API keys**
3. Znajdź klucz: `KljiTxEECuWoZfuzqj--9jPrpyIaGnOSxtr7iNoTXhRM`
4. **Usuń ten klucz**
5. Utwórz nowy klucz API
6. Zapisz nowy klucz w bezpiecznym miejscu

#### Elasticsearch:
1. Zaloguj się do [Elastic Cloud Console](https://cloud.elastic.co/)
2. Przejdź do swojego deployment
3. **Security → API keys**
4. Usuń klucz: `ZnlJenlwb0I2WjJRYmstdnlzVkc6eFZsMjFod2dFVUxXYnpEWGs1RVNhZw==`
5. Utwórz nowy API key
6. Zapisz nowy klucz

### 2. Utwórz plik `.env`

```bash
# W głównym katalogu projektu
cp config/env.example .env
```

### 3. Wypełnij `.env` NOWYMI kluczami

Edytuj plik `.env` i wstaw **NOWE** klucze API:

```bash
# Watsonx.ai
WATSONX_API_KEY=TWOJ_NOWY_KLUCZ_WATSONX
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
WATSONX_PROJECT_ID=82b92519-b5fa-4b80-a8a0-0247f1e2bedf
LLM_MODEL_ID=meta-llama/llama-4-maverick-17b-128e-instruct-fp8
EMBED_MODEL_ID=intfloat/multilingual-e5-large

# Elasticsearch serverless
ES_URL=https://my-elasticsearch-project-d02264.es.eu-central-1.aws.elastic.cloud:443
ES_API_KEY=TWOJ_NOWY_KLUCZ_ELASTICSEARCH
ES_INDEX=rag-documents
```

### 4. Sprawdź czy `.env` NIE jest w Git

```bash
git status
# .env NIE powinien się pojawić na liście
```

## 📦 Instalacja zależności

```bash
# Aktywuj środowisko wirtualne
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Zainstaluj zależności
pip install -r requirements.txt
```

## 🔍 Weryfikacja przed uruchomieniem

### Sprawdź czy masz wszystkie wymagane zmienne:

```bash
# Windows PowerShell
Get-Content .env

# Linux/Mac
cat .env
```

Upewnij się, że masz:
- ✅ `WATSONX_API_KEY` (nowy klucz!)
- ✅ `WATSONX_PROJECT_ID`
- ✅ `ES_URL`
- ✅ `ES_API_KEY` (nowy klucz!)
- ✅ `ES_INDEX`
- ✅ `LLM_MODEL_ID`
- ✅ `EMBED_MODEL_ID`

## ⚠️ WAŻNE - Wymiary embeddingów

**Sprawdź zgodność modelu z Elasticsearch:**

Jeśli używasz `intfloat/multilingual-e5-large` (domyślnie):
- ✅ Wymiary: **1024** (już poprawione w `config/es_config.py`)

Jeśli chcesz użyć innego modelu:
1. Zmień `EMBED_MODEL_ID` w `.env`
2. Zaktualizuj `dims` w `config/es_config.py`:
   - `ibm/slate-125m-english-rtrvr`: **768**
   - `sentence-transformers/all-MiniLM-L6-v2`: **384**

## 🚀 Uruchomienie aplikacji

```bash
streamlit run app.py
```

## 🧪 Test podstawowy

### 1. Test Upload (indeksacja):
1. Otwórz aplikację w przeglądarce
2. Wybierz **Upload** z menu
3. Prześlij plik `.txt`
4. Sprawdź czy:
   - ✅ Chunki zostały utworzone
   - ✅ Embeddingi zostały wygenerowane
   - ✅ Dane zostały wysłane do Elasticsearch

### 2. Test Chat (RAG):
1. Przejdź do **Chat**
2. Zadaj pytanie związane z przesłanym dokumentem
3. Sprawdź czy:
   - ✅ System znajduje kontekst
   - ✅ LLM generuje odpowiedź

## 🐛 Możliwe problemy

### Problem: "Missing required environment variables"
**Rozwiązanie:** Sprawdź czy plik `.env` istnieje i zawiera wszystkie wymagane zmienne

### Problem: "Elasticsearch connection failed"
**Rozwiązanie:** 
- Sprawdź czy `ES_URL` jest poprawny
- Sprawdź czy nowy `ES_API_KEY` działa
- Sprawdź połączenie internetowe

### Problem: "Watsonx authentication failed"
**Rozwiązanie:**
- Sprawdź czy nowy `WATSONX_API_KEY` jest poprawny
- Sprawdź czy `WATSONX_PROJECT_ID` jest poprawny

### Problem: "Dimension mismatch" w Elasticsearch
**Rozwiązanie:**
- Usuń stary indeks: 
  ```python
  from config.es_config import get_es
  es = get_es()
  es.indices.delete(index="rag-documents")
  ```
- Utwórz nowy z poprawnymi wymiarami (1024)

### Problem: "Tesseract not found" (dla PDF z OCR)
**Rozwiązanie:**
- Zainstaluj Tesseract OCR:
  - **Windows:** [Pobierz instalator](https://github.com/UB-Mannheim/tesseract/wiki)
  - **Linux:** `sudo apt install tesseract-ocr tesseract-ocr-pol`
  - **Mac:** `brew install tesseract tesseract-lang`
- Dodaj Tesseract do PATH (Windows)

### Problem: "PDF processing failed"
**Rozwiązanie:**
- Sprawdź czy plik PDF nie jest uszkodzony
- Dla skanów PDF upewnij się, że Tesseract jest zainstalowany
- Spróbuj najpierw z prostym plikiem TXT

## 📝 Podsumowanie

**Przed uruchomieniem MUSISZ:**
1. ✅ Zrotować klucze API (Watsonx + Elasticsearch)
2. ✅ Utworzyć plik `.env` z NOWYMI kluczami
3. ✅ Zainstalować zależności (`pip install -r requirements.txt`)
4. ✅ Sprawdzić zgodność wymiarów embeddingów

**Dopiero wtedy możesz:**
- 🚀 Uruchomić aplikację (`streamlit run app.py`)
- 📄 Wrzucać pliki do embeddingów
- 💬 Chatować z RAG-iem

## 🆘 Potrzebujesz pomocy?

Jeśli coś nie działa:
1. Sprawdź logi w terminalu
2. Sprawdź czy wszystkie zmienne środowiskowe są ustawione
3. Sprawdź połączenie z Elasticsearch i Watsonx
4. Zobacz `IMPROVEMENTS.md` dla dodatkowych informacji

---

**Status:** ⚠️ Aplikacja NIE jest gotowa do uruchomienia bez wykonania powyższych kroków!