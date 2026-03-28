# 🔐 Bezpieczeństwo

## Ochrona kluczy API

### ⚠️ NIGDY nie commituj wrażliwych danych

Plik `.env` zawiera wrażliwe klucze API i **NIGDY** nie powinien być dodany do repozytorium Git.

**Chronione pliki (już w `.gitignore`):**
- `.env`
- `.env.local`
- `*.env`
- Pliki z danymi w `data/`

### 📋 Konfiguracja środowiska

1. Skopiuj `config/env.example` do `.env`:
```bash
cp config/env.example .env
```

2. Wypełnij swoje klucze API w `.env`

3. Sprawdź, czy `.env` jest w `.gitignore`:
```bash
git check-ignore .env
# Powinno zwrócić: .env
```

## 🚨 Co zrobić, jeśli klucze zostały ujawnione?

Jeśli przypadkowo dodałeś klucze API do repozytorium:

### 1. Natychmiastowa rotacja kluczy

**Watsonx.ai:**
- Przejdź do IBM Cloud Console
- Wygeneruj nowy API key
- Usuń stary klucz

**Elasticsearch:**
- Przejdź do Elastic Cloud Console
- Wygeneruj nowy API key
- Usuń stary klucz

### 2. Usuń klucze z historii Git

```bash
# Usuń plik z indeksu (zachowaj lokalnie)
git rm --cached .env

# Commit zmian
git add .gitignore
git commit -m "chore: remove .env from repository"

# Opcjonalnie: wyczyść historię Git (UWAGA: zmienia historię!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

### 3. Zaktualizuj `.env` z nowymi kluczami

```bash
# Edytuj .env z nowymi kluczami
nano .env
```

## 🛡️ Best Practices

### Dla developerów

1. **Używaj różnych kluczy dla różnych środowisk:**
   - Development: `.env.development`
   - Staging: `.env.staging`
   - Production: `.env.production`

2. **Regularnie rotuj klucze API** (co 90 dni)

3. **Używaj secret managera w produkcji:**
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault
   - IBM Cloud Secrets Manager

4. **Nigdy nie loguj kluczy API:**
```python
# ❌ ŹLE
print(f"API Key: {WATSONX_API_KEY}")

# ✅ DOBRZE
print("API Key: ***hidden***")
```

5. **Sprawdzaj przed commitem:**
```bash
# Przed każdym commitem
git diff --cached | grep -i "api_key\|password\|secret"
```

### Dla zespołów

1. **Code review:** Zawsze sprawdzaj, czy PR nie zawiera kluczy
2. **Pre-commit hooks:** Użyj narzędzi jak `detect-secrets`
3. **GitHub Secret Scanning:** Włącz w ustawieniach repozytorium
4. **Dokumentacja:** Utrzymuj aktualną listę wymaganych zmiennych środowiskowych

## 🔍 Narzędzia do wykrywania sekretów

### detect-secrets
```bash
pip install detect-secrets
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

### git-secrets
```bash
# Instalacja
brew install git-secrets  # Mac
apt-get install git-secrets  # Linux

# Konfiguracja
git secrets --install
git secrets --register-aws
```

### TruffleHog
```bash
pip install truffleHog
trufflehog --regex --entropy=False .
```

## 📞 Zgłaszanie problemów bezpieczeństwa

Jeśli znajdziesz problem bezpieczeństwa w tym projekcie:

1. **NIE** twórz publicznego issue
2. Wyślij email do maintainera projektu
3. Opisz problem szczegółowo
4. Poczekaj na odpowiedź przed publicznym ujawnieniem

## 📚 Dodatkowe zasoby

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [IBM Cloud Security](https://www.ibm.com/cloud/security)
- [Elastic Security](https://www.elastic.co/security)