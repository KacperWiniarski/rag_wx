
# 🧠 RAG System — Watsonx.ai + Elasticsearch Serverless + Streamlit + OCR

Kompletny system Retrieval-Augmented Generation zbudowany w Pythonie.

Projekt zawiera:

- 🔍 **Watsonx.ai** — LLM + embeddingi  
- 🧮 **Elasticsearch Serverless 8.14** — wektorowa baza danych (dense_vector + kNN)  
- 📄 **OCR dla PDF** — Tesseract + pdf2image  
- ☁️ Streamlit:  
  - **Moduł upload** do indeksacji dokumentów  
  - **Czat RAG**  
- 🏗 Modularna, klarowna struktura repozytorium  
- 🔐 Pełna separacja zmiennych API poprzez `.env`  

---

# 📁 Struktura projektu

```
rag-system/
│── requirements.txt
│── README.md
│── .env.example
│── .gitignore
│
├── config/
│   ├── env.py
│   ├── settings.py
│   ├── watsonx_config.py
│   └── es_config.py
│
├── data/
├── docs/
│
├── ingestion/
│   ├── __init__.py
│   ├── ocr_utils.py
│   ├── pdf_loader.py
│   ├── file_loader.py
│   ├── text_splitter.py
│   ├── embedding_generator.py
│   └── ingest_to_es.py
│
├── retrieval/
│   ├── __init__.py
│   ├── retriever.py
│   └── rag_pipeline.py
│
├── frontend/
│   ├── __init__.py
│   ├── rag_upload_app.py
│   └── rag_chat_app.py
│
└── app.py
```

# 🚀 Funkcje systemu

### 🔹 1. Indeksacja dokumentów
- **PDF** (tekst lub skan) — automatyczna detekcja + **OCR Tesseract** dla skanów
- **TXT** — pliki tekstowe
- Automatyczny podział na chunki z nakładaniem
- Embeddingi z **watsonx.ai** (intfloat/multilingual-e5-large, 1024 wymiary)
- Zapis do Elasticsearch Serverless z mappingiem dense_vector

### 🔹 2. Wyszukiwanie
- kNN via Elasticsearch 8.14
- cosine similarity
- wektor query generowany przez watsonx.ai

### 🔹 3. Generowanie odpowiedzi
- RAG prompt → LLM watsonx.ai (Granite 20B lub dowolny inny)

### 🔹 4. Interfejs użytkownika
- Streamlit upload (do indeksacji)
- Streamlit chat → RAG pipeline

---

# 🔧 Wymagania

- Python **3.10+**
- Zainstalowany **Tesseract**:
  - Linux: `sudo apt install tesseract-ocr`
  - Mac: `brew install tesseract`
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki

---

# 📜 Instalacja

```
git clone <repo_url>
cd rag-system

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

---

# 🔐 Konfiguracja zmiennych środowiskowych

1. Skopiuj `config/env.example` do `.env` w głównym katalogu projektu:
```bash
# Linux/Mac
cp config/env.example .env

# Windows
copy config\env.example .env
```

2. Uzupełnij swoje klucze API do Watsonx.ai i Elasticsearch Serverless w pliku `.env`:
```bash
# Watsonx.ai
WATSONX_API_KEY=twoj_api_key
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
WATSONX_PROJECT_ID=twoj_project_id
LLM_MODEL_ID=meta-llama/llama-4-maverick-17b-128e-instruct-fp8
EMBED_MODEL_ID=intfloat/multilingual-e5-large

# Elasticsearch serverless
ES_URL=twoj_elasticsearch_url
ES_API_KEY=twoj_elasticsearch_api_key
ES_INDEX=rag-documents
```

## ⚠️ WAŻNE - Bezpieczeństwo

- **NIGDY nie commituj pliku `.env` do repozytorium!**
- Plik `.env` jest już dodany do `.gitignore`
- Jeśli przypadkowo dodałeś klucze API do repo, **natychmiast je zrotuj**
- Nie udostępniaj kluczy API w issues, pull requestach ani komunikacji publicznej
- Używaj różnych kluczy dla środowisk dev/staging/production

---

# 🧩 Uruchomienie aplikacji

```
streamlit run app.py
```

Aplikacja ma dwa moduły (wybór z sidebar):

- **Upload** → wysyłanie dokumentów i indeksacja
- **Chat** → RAG chatbot

---

# 🗂 Indeksowanie dokumentów

1. Przejdź w Streamlit do **Upload**
2. Prześlij PDF lub TXT
3. System:
   - wykona OCR (jeśli PDF bez tekstu)
   - podzieli treść na chunki
   - wygeneruje embeddingi
   - wyśle dane do Elasticsearch

---

# 💬 Czat RAG

1. Przejdź do **Chat**
2. Zadaj pytanie
3. Silnik RAG:
   - embeduje pytanie (watsonx)
   - wyszukuje wektorowo w Elasticsearch
   - buduje kontekst
   - generuje odpowiedź LLM watsonx.ai

---

# 🧠 Elasticsearch Mapping

```json
{
  "mappings": {
    "properties": {
      "content": { "type": "text" },
      "embedding": {
        "type": "dense_vector",
        "dims": 1024,
        "index": true,
        "similarity": "cosine"
      },
      "source": { "type": "keyword" },
      "chunk_id": { "type": "keyword" }
    }
  }
}
```

**Uwaga:** Wymiar `dims` musi odpowiadać modelowi embeddingów:
- `intfloat/multilingual-e5-large`: **1024** (domyślny)
- `ibm/slate-125m-english-rtrvr`: **768**
- `sentence-transformers/all-MiniLM-L6-v2`: **384**

Jeśli zmienisz model embeddingów w `.env`, zaktualizuj również `dims` w `config/es_config.py`.

---

# 🔌 Połączenie z Watsonx.ai (embedding + LLM)

### Embedding example:
```python
from ibm_watsonx_ai import WatsonxEmbeddings
emb = WatsonxEmbeddings(model_id="ibm/slate-125m-english-rtrvr", credentials={"apikey": WATSONX_APIKEY, "url": WATSONX_URL})
vector = emb.embed(["hello world"])
```

### LLM example:
```python
from ibm_watsonx_ai import WatsonxLLM
llm = WatsonxLLM(model_id="ibm/granite-20b-multilingual", credentials={"apikey": WATSONX_APIKEY, "url": WATSONX_URL})
answer = llm.generate("Hello, who are you?")
```

---

# 🖼 OCR Pipeline

Obsługiwane:

- PDF → tekst
- PDF → OCR (jeśli PDF jest skanem)
- UTF-8
- obrazy rasterowe z PDF

---

# 🐳 Docker - Szybkie uruchomienie

System można uruchomić w kontenerze Docker bez instalacji zależności na lokalnym systemie.

## Wymagania Docker
- Docker Engine 20.10+ lub Docker Desktop
- Docker Compose 2.0+
- 4 GB RAM (zalecane 8 GB)
- 3 GB wolnego miejsca na dysku

## Szybki start

### 1. Utwórz plik .env
```bash
# Linux/Mac
cp config/env.example .env

# Windows
copy config\env.example .env
```

### 2. Wypełnij klucze API w .env
```bash
WATSONX_API_KEY=twoj_klucz_api
WATSONX_PROJECT_ID=twoj_project_id
ES_URL=twoj_elasticsearch_url
ES_API_KEY=twoj_elasticsearch_api_key
```

### 3. Uruchom z docker-compose
```bash
# Zbuduj i uruchom
docker-compose up -d

# Sprawdź logi
docker-compose logs -f

# Otwórz w przeglądarce
http://localhost:8501
```

### 4. Zarządzanie
```bash
# Zatrzymaj
docker-compose stop

# Uruchom ponownie
docker-compose start

# Usuń kontener
docker-compose down
```

## Zalety Docker
✅ Brak instalacji Python, Tesseract i innych zależności
✅ Tesseract OCR wbudowany w obraz
✅ Izolowane środowisko
✅ Łatwe aktualizacje i rollback
✅ Działa identycznie na Windows, Linux i macOS
✅ Gotowy do uruchomienia w 10-15 minut

## Szczegółowa dokumentacja
Pełna dokumentacja Docker z troubleshooting: **[DOCKER_SETUP.md](DOCKER_SETUP.md)**

---

# 📚 Dokumentacja

- **[INSTALACJA_KROK_PO_KROKU.md](INSTALACJA_KROK_PO_KROKU.md)** - Szczegółowa instalacja tradycyjna (Python + venv)
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Instalacja i uruchomienie z Docker
- **[CHECKLIST_PRZED_URUCHOMIENIEM.md](CHECKLIST_PRZED_URUCHOMIENIEM.md)** - Checklist bezpieczeństwa
- **[PDF_SUPPORT.md](PDF_SUPPORT.md)** - Szczegóły obsługi PDF i OCR
- **[SECURITY.md](SECURITY.md)** - Wytyczne bezpieczeństwa
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Planowane ulepszenia

---

# 🎉 Miłej pracy z RAG!
