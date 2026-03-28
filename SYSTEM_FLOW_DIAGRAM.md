# 🔄 Schemat Przepływu Danych - System RAG

## 📊 Architektura Systemu

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM RAG - ARCHITEKTURA                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐                                    ┌──────────────────┐
│                  │                                    │                  │
│  ADMINISTRATOR   │                                    │  UŻYTKOWNIK      │
│  (Zasilanie      │                                    │  (Pytania)       │
│   bazy danych)   │                                    │                  │
│                  │                                    │                  │
└────────┬─────────┘                                    └────────┬─────────┘
         │                                                       │
         │ 1. Upload dokumentów                                 │ 1. Zadaje pytanie
         │    (PDF/TXT)                                         │
         ▼                                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                        STREAMLIT FRONTEND (app.py)                          │
│                                                                              │
│  ┌──────────────────────────┐         ┌──────────────────────────┐        │
│  │  📤 Upload Module        │         │  💬 Chat Module          │        │
│  │  (rag_upload_app.py)     │         │  (rag_chat_app.py)       │        │
│  └────────────┬─────────────┘         └────────────┬─────────────┘        │
│               │                                     │                       │
└───────────────┼─────────────────────────────────────┼───────────────────────┘
                │                                     │
                │                                     │
                ▼                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WARSTWA PRZETWARZANIA                                │
└─────────────────────────────────────────────────────────────────────────────┘
                │                                     │
    ┌───────────┴──────────┐              ┌─────────┴──────────┐
    │                      │              │                     │
    ▼                      ▼              ▼                     ▼
┌─────────┐         ┌──────────┐    ┌──────────┐        ┌──────────┐
│ File    │         │ PDF      │    │ RAG      │        │ Retriever│
│ Loader  │────────▶│ Loader   │    │ Pipeline │◀───────│          │
│         │         │ + OCR    │    │          │        │          │
└────┬────┘         └────┬─────┘    └────┬─────┘        └────┬─────┘
     │                   │               │                   │
     │ 2. Ładowanie      │ 3. OCR        │ 8. Generowanie    │ 6. Wyszukiwanie
     │    pliku          │    (Tesseract)│    odpowiedzi     │    wektorowe
     │                   │               │                   │
     ▼                   ▼               ▼                   │
┌─────────────────────────────┐   ┌──────────────┐         │
│  Text Splitter              │   │  LLM Model   │         │
│  (chunking + overlap)       │   │  (Watsonx.ai)│         │
└──────────┬──────────────────┘   └──────────────┘         │
           │                                                 │
           │ 4. Podział na chunki                           │
           ▼                                                 │
┌─────────────────────────────┐                             │
│  Embedding Generator        │                             │
│  (Watsonx.ai Embeddings)    │◀────────────────────────────┘
└──────────┬──────────────────┘     5. Embedding pytania
           │
           │ 5. Generowanie embeddingów
           │    (wektory 1024-wymiarowe)
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                    ELASTICSEARCH SERVERLESS 8.14                            │
│                         (Baza Wektorowa)                                    │
│                                                                              │
│  Index: rag-documents                                                       │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │  Document Structure:                                        │            │
│  │  {                                                          │            │
│  │    "content": "tekst chunka",                              │            │
│  │    "embedding": [1024-wymiarowy wektor],                   │            │
│  │    "source": "nazwa_pliku.pdf",                            │            │
│  │    "chunk_id": "unique_id"                                 │            │
│  │  }                                                          │            │
│  │                                                             │            │
│  │  Mapping:                                                   │            │
│  │  - dense_vector (dims: 1024)                               │            │
│  │  - similarity: cosine                                       │            │
│  │  - kNN search enabled                                       │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │
                                    │ 7. Zwraca top-k
                                    │    najbardziej podobnych
                                    │    chunków
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         WATSONX.AI (IBM Cloud)                              │
│                                                                              │
│  ┌──────────────────────────┐         ┌──────────────────────────┐        │
│  │  Embedding Model         │         │  LLM Model               │        │
│  │  intfloat/multilingual-  │         │  meta-llama/llama-4-     │        │
│  │  e5-large                │         │  maverick-17b-128e       │        │
│  │  (1024 dimensions)       │         │  -instruct-fp8           │        │
│  └──────────────────────────┘         └──────────────────────────┘        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Przepływ 1: ADMINISTRATOR - Zasilanie Bazy Wektorowej

### Krok po kroku:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 1: UPLOAD DOKUMENTU                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Administrator ──┐
                │
                ├─▶ [1] Otwiera Streamlit UI (http://localhost:8501)
                │
                ├─▶ [2] Wybiera "Upload" z menu bocznego
                │
                └─▶ [3] Przesyła plik(i): PDF lub TXT
                        │
                        ▼
                ┌───────────────────────────────────┐
                │  frontend/rag_upload_app.py       │
                │  - Odbiera plik(i)                │
                │  - Waliduje format (PDF/TXT)      │
                │  - Wyświetla informacje o pliku   │
                └───────────┬───────────────────────┘
                            │
                            ▼

┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 2: PRZETWARZANIE PLIKU                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

                ┌───────────────────────────────────┐
                │  ingestion/file_loader.py         │
                │  - Wykrywa typ pliku              │
                │  - Deleguje do odpowiedniego      │
                │    loadera                        │
                └───────────┬───────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
    ┌──────────────────┐    ┌──────────────────────┐
    │  TXT File        │    │  PDF File            │
    │  - Czyta UTF-8   │    │  ingestion/          │
    │  - Fallback:     │    │  pdf_loader.py       │
    │    latin-1       │    │                      │
    └────────┬─────────┘    └──────────┬───────────┘
             │                         │
             │                         ├─▶ Próba ekstrakcji tekstu
             │                         │   (PyPDF2)
             │                         │
             │                         ├─▶ Jeśli brak tekstu:
             │                         │   OCR (Tesseract)
             │                         │   - pdf2image
             │                         │   - pytesseract
             │                         │
             └─────────┬───────────────┘
                       │
                       ▼
                ┌───────────────────────────────────┐
                │  ingestion/text_splitter.py       │
                │  - chunk_size: 1024 znaków        │
                │  - overlap: 200 znaków            │
                │  - Tworzy listę chunków           │
                └───────────┬───────────────────────┘
                            │
                            ▼
                    [Lista chunków tekstu]
                    Chunk 1: "Lorem ipsum..."
                    Chunk 2: "...ipsum dolor..."
                    Chunk 3: "...dolor sit..."

┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 3: GENEROWANIE EMBEDDINGÓW                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                ┌───────────────────────────────────┐
                │  config/watsonx_config.py         │
                │  get_embedding_model()            │
                │  - Inicjalizuje Watsonx.ai        │
                │  - Model: intfloat/multilingual-  │
                │           e5-large                │
                └───────────┬───────────────────────┘
                            │
                            ▼
                ┌───────────────────────────────────┐
                │  Dla każdego chunka:              │
                │  1. Wysyła do Watsonx.ai          │
                │  2. Otrzymuje wektor [1024 dim]   │
                │  3. Dodaje do listy embeddingów   │
                └───────────┬───────────────────────┘
                            │
                            ▼
                    [Lista embeddingów]
                    Embedding 1: [0.123, -0.456, ...]
                    Embedding 2: [0.789, 0.234, ...]
                    Embedding 3: [-0.567, 0.890, ...]

┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 4: INDEKSACJA W ELASTICSEARCH                                          │
└─────────────────────────────────────────────────────────────────────────────┘

                ┌───────────────────────────────────┐
                │  ingestion/ingest_to_es.py        │
                │  - Przygotowuje dokumenty         │
                │  - Bulk insert do ES              │
                └───────────┬───────────────────────┘
                            │
                            ▼
                ┌───────────────────────────────────┐
                │  Elasticsearch Serverless         │
                │  Index: rag-documents             │
                │                                   │
                │  Dla każdego chunka tworzy:       │
                │  {                                │
                │    "_id": "unique_id",            │
                │    "content": "tekst chunka",     │
                │    "embedding": [wektor 1024],    │
                │    "source": "plik.pdf",          │
                │    "chunk_id": "chunk_0"          │
                │  }                                │
                └───────────┬───────────────────────┘
                            │
                            ▼
                    ✅ Dokumenty zaindeksowane
                    ✅ Gotowe do wyszukiwania
```

---

## 💬 Przepływ 2: UŻYTKOWNIK - Zadawanie Pytań (RAG)

### Krok po kroku:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 1: ZADANIE PYTANIA                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

Użytkownik ──┐
             │
             ├─▶ [1] Otwiera Streamlit UI
             │
             ├─▶ [2] Wybiera "Chat" z menu
             │
             └─▶ [3] Wpisuje pytanie:
                     "Jakie są główne funkcje systemu?"
                     │
                     ▼
             ┌───────────────────────────────────┐
             │  frontend/rag_chat_app.py         │
             │  - Odbiera pytanie użytkownika    │
             │  - Wywołuje rag_answer(question)  │
             └───────────┬───────────────────────┘
                         │
                         ▼

┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 2: WYSZUKIWANIE KONTEKSTU (RETRIEVAL)                                  │
└─────────────────────────────────────────────────────────────────────────────┘

             ┌───────────────────────────────────┐
             │  retrieval/rag_pipeline.py        │
             │  rag_answer(question)             │
             │  - Wywołuje search(question)      │
             └───────────┬───────────────────────┘
                         │
                         ▼
             ┌───────────────────────────────────┐
             │  retrieval/retriever.py           │
             │  search(query, k=3)               │
             └───────────┬───────────────────────┘
                         │
                         ├─▶ [1] Generuje embedding pytania
                         │       (Watsonx.ai)
                         │       query_vec = [1024 dim]
                         │
                         ├─▶ [2] Wysyła kNN query do ES:
                         │       {
                         │         "knn": {
                         │           "field": "embedding",
                         │           "query_vector": query_vec,
                         │           "k": 3,
                         │           "num_candidates": 50
                         │         }
                         │       }
                         │
                         ▼
             ┌───────────────────────────────────┐
             │  Elasticsearch                    │
             │  - Wyszukuje wektorowo (kNN)      │
             │  - Cosine similarity              │
             │  - Zwraca top-3 najbardziej       │
             │    podobne chunki                 │
             └───────────┬───────────────────────┘
                         │
                         ▼
                 [Kontekst - 3 chunki]
                 Chunk 1: "System RAG oferuje..."
                 Chunk 2: "Główne funkcje to..."
                 Chunk 3: "Dodatkowo system..."

┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 3: GENEROWANIE ODPOWIEDZI (GENERATION)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

             ┌───────────────────────────────────┐
             │  retrieval/rag_pipeline.py        │
             │  - Łączy chunki w kontekst        │
             │  - Buduje prompt:                 │
             │    "You are a RAG assistant.      │
             │     Context: [chunki]             │
             │     Question: [pytanie]           │
             │     Answer based on context."     │
             └───────────┬───────────────────────┘
                         │
                         ▼
             ┌───────────────────────────────────┐
             │  config/watsonx_config.py         │
             │  get_llm_model()                  │
             │  - Model: meta-llama/llama-4-     │
             │           maverick-17b-128e       │
             └───────────┬───────────────────────┘
                         │
                         ▼
             ┌───────────────────────────────────┐
             │  Watsonx.ai LLM                   │
             │  - Przetwarza prompt              │
             │  - Generuje odpowiedź na          │
             │    podstawie kontekstu            │
             └───────────┬───────────────────────┘
                         │
                         ▼
                 [Wygenerowana odpowiedź]
                 "System RAG oferuje następujące
                  główne funkcje: indeksację
                  dokumentów PDF/TXT, wyszukiwanie
                  wektorowe oraz generowanie
                  odpowiedzi..."

┌─────────────────────────────────────────────────────────────────────────────┐
│ FAZA 4: WYŚWIETLENIE ODPOWIEDZI                                             │
└─────────────────────────────────────────────────────────────────────────────┘

             ┌───────────────────────────────────┐
             │  frontend/rag_chat_app.py         │
             │  - Otrzymuje odpowiedź            │
             │  - Wyświetla w UI Streamlit       │
             └───────────┬───────────────────────┘
                         │
                         ▼
                 Użytkownik widzi odpowiedź
                 w interfejsie czatu
```

---

## 🔧 Komponenty Systemu

### 1. **Frontend (Streamlit)**
- **app.py** - Główny punkt wejścia, router między modułami
- **rag_upload_app.py** - Interfejs do uploadowania dokumentów
- **rag_chat_app.py** - Interfejs czatu RAG

### 2. **Ingestion (Przetwarzanie dokumentów)**
- **file_loader.py** - Ładowanie plików TXT/PDF
- **pdf_loader.py** - Ekstrakcja tekstu z PDF + OCR
- **ocr_utils.py** - Narzędzia OCR (Tesseract)
- **text_splitter.py** - Podział tekstu na chunki
- **embedding_generator.py** - Generowanie embeddingów
- **ingest_to_es.py** - Indeksacja w Elasticsearch

### 3. **Retrieval (Wyszukiwanie i generowanie)**
- **retriever.py** - Wyszukiwanie wektorowe w ES
- **rag_pipeline.py** - Orkiestracja RAG (retrieval + generation)

### 4. **Config (Konfiguracja)**
- **env.py** - Ładowanie zmiennych środowiskowych
- **watsonx_config.py** - Konfiguracja Watsonx.ai (LLM + embeddings)
- **es_config.py** - Konfiguracja Elasticsearch

### 5. **Zewnętrzne Serwisy**
- **Watsonx.ai** - LLM i embeddingi (IBM Cloud)
- **Elasticsearch Serverless 8.14** - Baza wektorowa
- **Tesseract OCR** - Rozpoznawanie tekstu ze skanów

---

## 📊 Przepływ Danych - Podsumowanie

```
ADMINISTRATOR                          UŻYTKOWNIK
     │                                      │
     │ Upload PDF/TXT                       │ Zadaje pytanie
     ▼                                      ▼
┌─────────────────────────────────────────────────────┐
│              STREAMLIT FRONTEND                     │
│  Upload Module          │         Chat Module       │
└────────┬────────────────┴──────────────┬────────────┘
         │                                │
         │ Przetwarzanie                  │ RAG Pipeline
         ▼                                ▼
┌─────────────────────┐         ┌─────────────────────┐
│  File Processing    │         │  Query Processing   │
│  - Load             │         │  - Embed query      │
│  - OCR (if needed)  │         │  - Search ES        │
│  - Split to chunks  │         │  - Build context    │
│  - Generate vectors │         │  - Generate answer  │
└─────────┬───────────┘         └──────────┬──────────┘
          │                                 │
          │ Bulk insert                     │ kNN search
          ▼                                 ▼
┌─────────────────────────────────────────────────────┐
│         ELASTICSEARCH SERVERLESS 8.14               │
│  Index: rag-documents                               │
│  - dense_vector (1024 dims)                         │
│  - cosine similarity                                │
│  - kNN search                                       │
└─────────────────────────────────────────────────────┘
          ▲                                 │
          │                                 │
          │ Embeddings                      │ Top-k chunks
          │                                 ▼
┌─────────────────────────────────────────────────────┐
│              WATSONX.AI (IBM Cloud)                 │
│  - Embedding Model (intfloat/multilingual-e5-large) │
│  - LLM Model (meta-llama/llama-4-maverick-17b)     │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Bezpieczeństwo

- Wszystkie klucze API przechowywane w `.env`
- `.env` w `.gitignore` (nigdy nie commitowany)
- Separacja credentials dla dev/staging/production
- HTTPS dla połączeń z Watsonx.ai i Elasticsearch

---

## 🚀 Technologie

| Komponent | Technologia |
|-----------|-------------|
| Frontend | Streamlit |
| LLM | Watsonx.ai (Llama 4 Maverick 17B) |
| Embeddings | Watsonx.ai (multilingual-e5-large) |
| Vector DB | Elasticsearch Serverless 8.14 |
| OCR | Tesseract + pdf2image |
| Language | Python 3.10+ |
| Deployment | Docker + docker-compose |

---

## 📈 Metryki Wydajności

- **Wymiar embeddingów**: 1024
- **Chunk size**: 1024 znaków
- **Chunk overlap**: 200 znaków
- **kNN k**: 3 (top-3 najbardziej podobne chunki)
- **kNN candidates**: 50
- **Similarity**: cosine

---

*Schemat wygenerowany dla projektu RAG System - Watsonx.ai + Elasticsearch*