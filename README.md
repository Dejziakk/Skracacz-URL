# Skracacz URL

Projekt realizowany w ramach przedmiotu **Metody Wirtualizacji**.

## Opis projektu

Celem projektu jest stworzenie aplikacji internetowej do skracania adresów URL oraz zliczania kliknięć w utworzone linki.

Obecnie przygotowano środowisko aplikacji z wykorzystaniem trzech kontenerów Docker. Funkcjonalność skracania linków i zliczania kliknięć będzie rozwijana w kolejnych etapach.

## Architektura

Projekt składa się z trzech kontenerów Docker:

- **Frontend (Nginx)** – wyświetla stronę internetową przygotowaną w HTML i JavaScript.
- **Backend (Python FastAPI)** – obsługuje żądania HTTP, zwraca dane w formacie JSON i komunikuje się z bazą danych.
- **Baza danych (PostgreSQL)** – będzie przechowywać informacje o skróconych linkach i kliknięciach.

Kontenery komunikują się ze sobą za pomocą sieci Docker Compose.

## Wykorzystane technologie

- Docker i Docker Compose
- Nginx
- HTML i JavaScript
- Python i FastAPI
- PostgreSQL

## Uruchomienie projektu

Do uruchomienia projektu potrzebny jest Docker Desktop.

1. Pobierz repozytorium z GitHuba.

2. W głównym folderze projektu utwórz plik `.env` z następującą zawartością:

   ```env
   POSTGRES_USER=skracacz
   POSTGRES_PASSWORD=moje_haslo
   POSTGRES_DB=skracacz_db
   ```

   Hasło `moje_haslo` jest przykładowe. Można ustawić własne hasło.

3. Otwórz terminal w głównym folderze projektu i wpisz:

   ```bash
   docker compose up --build -d
   ```

4. Po uruchomieniu kontenerów sprawdź działanie aplikacji w przeglądarce:

   - `http://localhost:8082` – strona główna.
   - `http://localhost:8082/api/status` – sprawdzenie backendu.
   - `http://localhost:8082/api/db-status` – sprawdzenie połączenia z bazą danych.

Aby zatrzymać kontenery, wpisz:

```bash
docker compose down
```

## Aktualny stan projektu

- Utworzono frontend oparty na Nginx.
- Utworzono backend w Pythonie z wykorzystaniem FastAPI.
- Uruchomiono bazę danych PostgreSQL.
- Skonfigurowano trzy kontenery za pomocą Docker Compose.
- Uruchomiono komunikację HTTP i JSON między frontendem a backendem.
- Przetestowano połączenie backendu z bazą danych PostgreSQL.

## Wykorzystanie AI

Podczas realizacji projektu korzystamy z narzędzi AI jako wsparcia przy planowaniu projektu, tworzeniu dokumentacji, wyjaśnianiu zagadnień technicznych oraz przygotowywaniu i analizowaniu fragmentów kodu.

Wygenerowane propozycje są sprawdzane i testowane podczas pracy nad projektem.