# 🐳 Docker Setup - RAG System

## Szybki start z Docker

Ten przewodnik pokazuje jak uruchomić aplikację RAG System w kontenerze Docker w kilku prostych krokach.

---

## 📋 Spis treści

1. [Wymagania](#wymagania)
2. [Instalacja Docker](#instalacja-docker)
3. [Konfiguracja](#konfiguracja)
4. [Budowanie obrazu](#budowanie-obrazu)
5. [Uruchomienie z docker-compose](#uruchomienie-z-docker-compose)
6. [Uruchomienie z docker run](#uruchomienie-z-docker-run)
7. [Zarządzanie kontenerem](#zarządzanie-kontenerem)
8. [Rozwiązywanie problemów](#rozwiązywanie-problemów)
9. [Zaawansowane opcje](#zaawansowane-opcje)

---

## 1. Wymagania

### Minimalne wymagania systemowe:
- **RAM:** 4 GB (zalecane 8 GB)
- **Procesor:** Dual-core 2.0 GHz+
- **Miejsce na dysku:** 3 GB wolnego miejsca
- **System operacyjny:** 
  - Windows 10/11 (64-bit) z WSL2
  - Linux (kernel 3.10+)
  - macOS 10.15+

### Wymagane oprogramowanie:
- Docker Engine 20.10+ lub Docker Desktop
- Docker Compose 2.0+ (zwykle wbudowany w Docker Desktop)

---

## 2. Instalacja Docker

### Windows:

#### Krok 2.1: Pobierz Docker Desktop
1. Przejdź do: https://www.docker.com/products/docker-desktop/
2. Pobierz Docker Desktop dla Windows
3. Uruchom instalator

#### Krok 2.2: Włącz WSL2
Docker Desktop wymaga WSL2:
```powershell
# Uruchom PowerShell jako Administrator
wsl --install
```

#### Krok 2.3: Uruchom Docker Desktop
1. Uruchom Docker Desktop z menu Start
2. Poczekaj aż Docker się uruchomi (ikona wieloryba w zasobniku systemowym)
3. Weryfikacja:
```powershell
docker --version
docker-compose --version
```

### Linux (Ubuntu/Debian):

```bash
# Usuń stare wersje
sudo apt-get remove docker docker-engine docker.io containerd runc

# Zainstaluj zależności
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Dodaj oficjalny klucz GPG Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Dodaj repozytorium Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Zainstaluj Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Dodaj użytkownika do grupy docker (aby nie używać sudo)
sudo usermod -aG docker $USER
newgrp docker

# Weryfikacja
docker --version
docker compose version
```

### macOS:

1. Pobierz Docker Desktop dla Mac: https://www.docker.com/products/docker-desktop/
2. Otwórz plik `.dmg` i przeciągnij Docker do Applications
3. Uruchom Docker z Applications
4. Weryfikacja:
```bash
docker --version
docker compose version
```

---

## 3. Konfiguracja

### Krok 3.1: Przejdź do katalogu projektu
```bash
cd c:/Users/kacper/OneDrive\ -\ TDSYNNEX/Desktop/Dlab/RAG_ws_es
```

### Krok 3.2: Utwórz plik .env
```bash
# Windows
copy config\env.example .env

# Linux/Mac
cp config/env.example .env
```

### Krok 3.3: Wypełnij plik .env
Edytuj plik `.env` i dodaj swoje klucze API:

```bash
# Watsonx.ai
WATSONX_API_KEY=twoj_klucz_api_watsonx
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
WATSONX_PROJECT_ID=twoj_project_id
LLM_MODEL_ID=meta-llama/llama-4-maverick-17b-128e-instruct-fp8
EMBED_MODEL_ID=intfloat/multilingual-e5-large

# Elasticsearch serverless
ES_URL=twoj_elasticsearch_url
ES_API_KEY=twoj_elasticsearch_api_key
ES_INDEX=rag-documents
```

### Krok 3.4: Utwórz katalogi dla danych
```bash
# Windows
mkdir data
mkdir docs

# Linux/Mac
mkdir -p data docs
```

---

## 4. Budowanie obrazu

### Opcja A: Budowanie z docker-compose (zalecane)
```bash
docker-compose build
```

### Opcja B: Budowanie bezpośrednio
```bash
docker build -t rag-system:latest .
```

**Czas budowania:** 5-10 minut (przy pierwszym budowaniu)

### Sprawdzenie zbudowanego obrazu
```bash
docker images | grep rag-system
```

Powinieneś zobaczyć:
```
rag-system    latest    abc123def456    2 minutes ago    1.2GB
```

---

## 5. Uruchomienie z docker-compose

### Krok 5.1: Uruchom kontener
```bash
docker-compose up -d
```

Flagi:
- `-d` - uruchom w tle (detached mode)

### Krok 5.2: Sprawdź status
```bash
docker-compose ps
```

Powinieneś zobaczyć:
```
NAME         IMAGE              STATUS         PORTS
rag-system   rag-system:latest  Up 30 seconds  0.0.0.0:8501->8501/tcp
```

### Krok 5.3: Sprawdź logi
```bash
# Wszystkie logi
docker-compose logs

# Logi w czasie rzeczywistym
docker-compose logs -f

# Ostatnie 50 linii
docker-compose logs --tail=50
```

### Krok 5.4: Otwórz aplikację
Przejdź do przeglądarki:
```
http://localhost:8501
```

---

## 6. Uruchomienie z docker run

Jeśli wolisz nie używać docker-compose:

```bash
docker run -d \
  --name rag-system \
  -p 8501:8501 \
  -e WATSONX_API_KEY="twoj_klucz" \
  -e WATSONX_URL="https://eu-de.ml.cloud.ibm.com" \
  -e WATSONX_PROJECT_ID="twoj_project_id" \
  -e LLM_MODEL_ID="meta-llama/llama-4-maverick-17b-128e-instruct-fp8" \
  -e EMBED_MODEL_ID="intfloat/multilingual-e5-large" \
  -e ES_URL="twoj_elasticsearch_url" \
  -e ES_API_KEY="twoj_elasticsearch_api_key" \
  -e ES_INDEX="rag-documents" \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/docs:/app/docs \
  --restart unless-stopped \
  rag-system:latest
```

**Windows PowerShell:**
```powershell
docker run -d `
  --name rag-system `
  -p 8501:8501 `
  -e WATSONX_API_KEY="twoj_klucz" `
  -e WATSONX_URL="https://eu-de.ml.cloud.ibm.com" `
  -e WATSONX_PROJECT_ID="twoj_project_id" `
  -e LLM_MODEL_ID="meta-llama/llama-4-maverick-17b-128e-instruct-fp8" `
  -e EMBED_MODEL_ID="intfloat/multilingual-e5-large" `
  -e ES_URL="twoj_elasticsearch_url" `
  -e ES_API_KEY="twoj_elasticsearch_api_key" `
  -e ES_INDEX="rag-documents" `
  -v ${PWD}/data:/app/data `
  -v ${PWD}/docs:/app/docs `
  --restart unless-stopped `
  rag-system:latest
```

---

## 7. Zarządzanie kontenerem

### Zatrzymanie kontenera
```bash
# Z docker-compose
docker-compose stop

# Bezpośrednio
docker stop rag-system
```

### Uruchomienie ponownie
```bash
# Z docker-compose
docker-compose start

# Bezpośrednio
docker start rag-system
```

### Restart kontenera
```bash
# Z docker-compose
docker-compose restart

# Bezpośrednio
docker restart rag-system
```

### Zatrzymanie i usunięcie
```bash
# Z docker-compose (usuwa kontenery, sieci, ale zachowuje volumes)
docker-compose down

# Usuń również volumes (UWAGA: usunie dane!)
docker-compose down -v

# Bezpośrednio
docker stop rag-system
docker rm rag-system
```

### Sprawdzenie logów
```bash
# Z docker-compose
docker-compose logs -f

# Bezpośrednio
docker logs -f rag-system
```

### Wejście do kontenera (debugging)
```bash
# Z docker-compose
docker-compose exec rag-system /bin/bash

# Bezpośrednio
docker exec -it rag-system /bin/bash
```

### Sprawdzenie zużycia zasobów
```bash
docker stats rag-system
```

---

## 8. Rozwiązywanie problemów

### Problem 1: "Cannot connect to Docker daemon"

**Przyczyna:** Docker nie jest uruchomiony.

**Rozwiązanie:**
- **Windows/Mac:** Uruchom Docker Desktop
- **Linux:** 
  ```bash
  sudo systemctl start docker
  sudo systemctl enable docker
  ```

### Problem 2: "Port 8501 already in use"

**Przyczyna:** Inny proces używa portu 8501.

**Rozwiązanie:**
```bash
# Znajdź proces używający portu
# Windows
netstat -ano | findstr :8501

# Linux/Mac
lsof -i :8501

# Zmień port w docker-compose.yml
ports:
  - "8502:8501"  # Użyj portu 8502 zamiast 8501
```

### Problem 3: "Build failed" lub "No space left on device"

**Przyczyna:** Brak miejsca na dysku lub stare obrazy Docker.

**Rozwiązanie:**
```bash
# Usuń nieużywane obrazy, kontenery i volumes
docker system prune -a

# Sprawdź miejsce
docker system df
```

### Problem 4: Kontener się restartuje w kółko

**Przyczyna:** Błąd w konfiguracji lub brakujące zmienne środowiskowe.

**Rozwiązanie:**
```bash
# Sprawdź logi
docker-compose logs --tail=100

# Sprawdź czy plik .env istnieje i jest poprawny
cat .env

# Sprawdź status kontenera
docker-compose ps
```

### Problem 5: "Permission denied" na Linux

**Przyczyna:** Użytkownik nie jest w grupie docker.

**Rozwiązanie:**
```bash
sudo usermod -aG docker $USER
newgrp docker

# Lub uruchom z sudo
sudo docker-compose up -d
```

### Problem 6: Wolne działanie aplikacji

**Przyczyna:** Za mało przydzielonych zasobów.

**Rozwiązanie:**
```bash
# Zwiększ limity w docker-compose.yml
services:
  rag-system:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          memory: 2G
```

### Problem 7: "Tesseract not found" w kontenerze

**Przyczyna:** Tesseract nie został zainstalowany w obrazie.

**Rozwiązanie:**
```bash
# Przebuduj obraz
docker-compose build --no-cache

# Sprawdź czy Tesseract jest w kontenerze
docker-compose exec rag-system tesseract --version
```

### Problem 8: Zmiany w kodzie nie są widoczne

**Przyczyna:** Kod jest skopiowany do obrazu podczas budowania.

**Rozwiązanie:**
```bash
# Przebuduj obraz
docker-compose build

# Uruchom ponownie
docker-compose up -d

# Lub użyj volume dla development (dodaj do docker-compose.yml):
volumes:
  - .:/app  # UWAGA: Tylko dla development!
```

---

## 9. Zaawansowane opcje

### Development mode z hot-reload

Utwórz `docker-compose.dev.yml`:
```yaml
version: '3.8'

services:
  rag-system:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: rag-system-dev
    ports:
      - "8501:8501"
    environment:
      - WATSONX_API_KEY=${WATSONX_API_KEY}
      - WATSONX_URL=${WATSONX_URL}
      - WATSONX_PROJECT_ID=${WATSONX_PROJECT_ID}
      - LLM_MODEL_ID=${LLM_MODEL_ID}
      - EMBED_MODEL_ID=${EMBED_MODEL_ID}
      - ES_URL=${ES_URL}
      - ES_API_KEY=${ES_API_KEY}
      - ES_INDEX=${ES_INDEX}
    volumes:
      - .:/app  # Mount całego kodu dla hot-reload
      - /app/venv  # Exclude venv
    command: streamlit run app.py --server.runOnSave=true
    restart: unless-stopped
```

Uruchom:
```bash
docker-compose -f docker-compose.dev.yml up
```

### Budowanie dla różnych platform

```bash
# Dla ARM64 (Apple Silicon)
docker buildx build --platform linux/arm64 -t rag-system:arm64 .

# Dla AMD64 (Intel/AMD)
docker buildx build --platform linux/amd64 -t rag-system:amd64 .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t rag-system:latest .
```

### Optymalizacja rozmiaru obrazu

Obraz jest już zoptymalizowany przez:
- ✅ Multi-stage build
- ✅ Slim base image (python:3.11-slim)
- ✅ Czyszczenie cache apt
- ✅ .dockerignore

Aktualny rozmiar: ~1.2 GB

### Monitoring i logi

```bash
# Eksport logów do pliku
docker-compose logs > logs.txt

# Monitoring w czasie rzeczywistym
docker stats rag-system

# Health check
docker inspect --format='{{.State.Health.Status}}' rag-system
```

### Backup danych

```bash
# Backup volumes
docker run --rm \
  -v rag_ws_es_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz /data

# Restore
docker run --rm \
  -v rag_ws_es_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/data-backup.tar.gz -C /
```

### Uruchomienie w tle z automatycznym restartem

```bash
docker-compose up -d --restart=always
```

### Skalowanie (jeśli potrzebne)

```bash
# Uruchom 3 instancje (wymaga load balancera)
docker-compose up -d --scale rag-system=3
```

---

## 📊 Porównanie: Docker vs Tradycyjna instalacja

| Aspekt | Docker | Tradycyjna instalacja |
|--------|--------|----------------------|
| **Czas setup** | 10-15 min | 30-60 min |
| **Zależności** | Automatyczne | Ręczna instalacja |
| **Izolacja** | ✅ Pełna | ❌ Brak |
| **Przenośność** | ✅ Wysoka | ⚠️ Średnia |
| **Aktualizacje** | `docker-compose pull` | Ręczne |
| **Rollback** | Łatwy | Trudny |
| **Zużycie RAM** | +200-300 MB | Bazowe |
| **Tesseract OCR** | ✅ Wbudowany | Ręczna instalacja |

---

## ✅ Checklist Docker

Przed uruchomieniem upewnij się, że:

- [ ] Docker Desktop/Engine zainstalowany i uruchomiony
- [ ] Plik `.env` utworzony i wypełniony
- [ ] Katalogi `data/` i `docs/` utworzone
- [ ] Port 8501 jest wolny
- [ ] Masz co najmniej 4 GB wolnej pamięci RAM
- [ ] Masz co najmniej 3 GB wolnego miejsca na dysku

---

## 🎯 Szybkie komendy

```bash
# Buduj i uruchom
docker-compose up -d --build

# Sprawdź status
docker-compose ps

# Zobacz logi
docker-compose logs -f

# Restart
docker-compose restart

# Zatrzymaj
docker-compose stop

# Usuń wszystko
docker-compose down -v

# Wejdź do kontenera
docker-compose exec rag-system /bin/bash

# Sprawdź zużycie zasobów
docker stats rag-system
```

---

## 🆘 Potrzebujesz pomocy?

1. Sprawdź logi: `docker-compose logs`
2. Sprawdź status: `docker-compose ps`
3. Sprawdź health check: `docker inspect rag-system`
4. Zobacz sekcję [Rozwiązywanie problemów](#8-rozwiązywanie-problemów)

---

## 📚 Dodatkowe zasoby

- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose:** https://docs.docker.com/compose/
- **Best Practices:** https://docs.docker.com/develop/dev-best-practices/

---

**Wersja dokumentu:** 1.0  
**Data ostatniej aktualizacji:** 2026-03-05  
**Kompatybilność:** Docker 20.10+, Docker Compose 2.0+