# Konfiguracja Parametrów Embeddingów

## Przegląd

Parametry związane z podziałem tekstu na chunki (fragmenty) są teraz konfigurowane przez zmienne środowiskowe, co umożliwia łatwą zmianę bez modyfikacji kodu.

## Zmienne Środowiskowe

### CHUNK_SIZE
- **Opis**: Rozmiar pojedynczego chunku tekstu w znakach
- **Wartość domyślna**: `2048`
- **Zakres**: Liczba całkowita > 0
- **Użycie**: Określa maksymalną długość fragmentu tekstu, który będzie przetwarzany jako pojedyncza jednostka

### CHUNK_OVERLAP
- **Opis**: Liczba znaków nakładki między sąsiednimi chunkami
- **Wartość domyślna**: `256`
- **Zakres**: Liczba całkowita >= 0 i < CHUNK_SIZE
- **Użycie**: Zapewnia kontekst między chunkami, poprawiając jakość wyszukiwania

## Konfiguracja

### 1. Plik .env

Dodaj następujące linie do pliku `.env`:

```env
# Text chunking configuration
CHUNK_SIZE=2048
CHUNK_OVERLAP=256
```

### 2. Przykładowa konfiguracja (config/env.example)

Plik `config/env.example` zawiera domyślne wartości:

```env
# Text chunking configuration
CHUNK_SIZE=2048
CHUNK_OVERLAP=256
```

## Zmodyfikowane Pliki

### 1. config/env.py
- Dodano import i deklarację zmiennych `CHUNK_SIZE` i `CHUNK_OVERLAP`
- Wartości są pobierane z zmiennych środowiskowych z fallbackiem na wartości domyślne

### 2. config/env.example
- Dodano sekcję z konfiguracją chunkowania tekstu

### 3. ingestion/text_splitter.py
- Zmieniono parametry funkcji `split_text()` na opcjonalne
- Domyślne wartości są pobierane z `config.env`
- Dodano import `CHUNK_SIZE` i `CHUNK_OVERLAP`

### 4. ingestion/file_loader.py
- Zmieniono parametry funkcji `load_file()` na opcjonalne
- Domyślne wartości są pobierane z `config.env`
- Dodano import `CHUNK_SIZE` i `CHUNK_OVERLAP`

## Użycie

### Domyślne wartości (z .env)

```python
from ingestion.file_loader import load_file

# Użyje CHUNK_SIZE=2048 i CHUNK_OVERLAP=256 z .env
chunks = load_file("document.txt")
```

### Niestandardowe wartości

```python
from ingestion.file_loader import load_file

# Nadpisanie wartości z .env
chunks = load_file("document.txt", chunk_size=1024, overlap=128)
```

### Bezpośrednie użycie split_text

```python
from ingestion.text_splitter import split_text

# Użyje wartości z .env
chunks = split_text(text)

# Lub z niestandardowymi wartościami
chunks = split_text(text, chunk_size=1024, overlap=128)
```

## Zalecenia

### Optymalne wartości

- **CHUNK_SIZE=2048**: Dobry balans między kontekstem a precyzją dla większości dokumentów
- **CHUNK_OVERLAP=256**: ~12.5% overlap zapewnia wystarczający kontekst między chunkami

### Dostosowanie wartości

**Zwiększ CHUNK_SIZE gdy:**
- Dokumenty zawierają długie, powiązane sekcje
- Potrzebujesz więcej kontekstu w pojedynczym chunku
- Masz dokumenty techniczne z długimi wyjaśnieniami

**Zmniejsz CHUNK_SIZE gdy:**
- Dokumenty zawierają krótkie, niezależne sekcje
- Potrzebujesz bardziej precyzyjnego wyszukiwania
- Masz ograniczenia pamięci lub wydajności

**Zwiększ CHUNK_OVERLAP gdy:**
- Informacje często rozciągają się na granice chunków
- Potrzebujesz lepszej ciągłości kontekstu
- Jakość wyszukiwania jest priorytetem nad rozmiarem indeksu

**Zmniejsz CHUNK_OVERLAP gdy:**
- Chcesz zmniejszyć rozmiar indeksu
- Dokumenty mają wyraźne granice sekcji
- Wydajność jest priorytetem

## Walidacja

System automatycznie waliduje, że:
- `CHUNK_OVERLAP < CHUNK_SIZE`
- Obie wartości są liczbami całkowitymi

Jeśli walidacja się nie powiedzie, zostanie zgłoszony błąd `ValueError`.

## Migracja z poprzedniej wersji

Jeśli używałeś wcześniej hardcoded wartości:

**Przed:**
```python
chunks = load_file("doc.txt", chunk_size=1024, overlap=200)
```

**Po migracji:**
1. Ustaw wartości w `.env`:
   ```env
   CHUNK_SIZE=1024
   CHUNK_OVERLAP=200
   ```

2. Uproszczony kod:
   ```python
   chunks = load_file("doc.txt")
   ```

## Troubleshooting

### Problem: ValueError: overlap musi być mniejszy niż chunk_size

**Rozwiązanie**: Upewnij się, że `CHUNK_OVERLAP < CHUNK_SIZE` w pliku `.env`

### Problem: Chunki są za duże/małe

**Rozwiązanie**: Dostosuj wartość `CHUNK_SIZE` w pliku `.env`

### Problem: Brak kontekstu między chunkami

**Rozwiązanie**: Zwiększ wartość `CHUNK_OVERLAP` w pliku `.env`