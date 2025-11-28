
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
- PDF (tekst lub skan) — **OCR Tesseract**
- TXT
- automatyczny podział na chunki
- embeddingi z **watsonx.ai**
- zapis do Elasticsearch Serverless z mappingiem dense_vector

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

1. Skopiuj `config\env.example` do `.env`
```
cp .env.example .env
```
2. Uzupełnij swoje klucze API do Watsonx.ai i Elasticsearch Serverless

⚠ **Nie dodawaj prawdziwego `.env` do repo!**

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
        "dims": 384,
        "index": true,
        "similarity": "cosine"
      },
      "source": { "type": "keyword" },
      "chunk_id": { "type": "keyword" }
    }
  }
}
```

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

# 🐳 Docker (opcjonalnie)

Można przygotować:

- Dockerfile
- docker-compose dla:
  - Streamlit
  - Elasticsearch Serverless Proxy
  - Tesseract

---

# 🎉 Miłej pracy z RAG!
