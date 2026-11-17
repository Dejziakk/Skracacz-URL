# Skracacz URL

Projekt realizowany w ramach przedmiotu **Metody Wirtualizacji**.

## Opis projektu

Skracacz URL to prosta aplikacja internetowa do tworzenia krótszych adresów stron internetowych.

Użytkownik może:
- dodać nowy link i wybrać własny krótki kod,
- wygenerować losowy kod, jeśli nie poda własnego,
- zobaczyć listę zapisanych linków,
- otworzyć skrócony link i przejść na właściwą stronę,
- sprawdzić liczbę odwiedzin każdego linku,
- usunąć wybrany link.

Aplikacja korzysta z Dockera i bazy danych PostgreSQL.

## Architektura projektu

Projekt składa się z trzech kontenerów Docker:

- **Frontend (Nginx)** – wyświetla stronę internetową napisaną w HTML i JavaScript.
- **Backend (Python FastAPI)** – obsługuje dodawanie, pobieranie i usuwanie linków oraz przekierowania.
- **Baza danych (PostgreSQL)** – przechowuje linki i informacje o odwiedzinach.

Kontenery są uruchamiane za pomocą Docker Compose i komunikują się ze sobą w sieci Dockera.

Frontend wysyła żądania do backendu, a backend odczytuje i zapisuje dane w PostgreSQL.

## Wykorzystane technologie

- Docker i Docker Compose
- Nginx
- HTML i JavaScript
- Python i FastAPI
- PostgreSQL

## Uruchomienie projektu

Do uruchomienia projektu potrzebny jest **Docker Desktop**.

1. Pobierz repozytorium z GitHuba.

2. W głównym folderze projektu utwórz plik `.env`:

   ```env
   POSTGRES_USER=skracacz
   POSTGRES_PASSWORD=skracacz_test
   POSTGRES_DB=skracacz_db
   ```

   Hasło jest przykładowe i można je zmienić.

3. Otwórz terminal w głównym folderze projektu i wpisz:

   ```bash
   docker compose up -d --build
   ```

4. Poczekaj, aż kontenery się uruchomią, a następnie otwórz:

   **http://localhost:8082**

Dodatkowe adresy:

- `http://localhost:8082/api/docs` – dokumentacja API (Swagger).
- `http://localhost:8082/api/status` – sprawdzenie działania backendu.
- `http://localhost:8082/api/health` – sprawdzenie stanu backendu.
- `http://localhost:8082/api/db-status` – sprawdzenie połączenia z bazą danych.

Aby zatrzymać i usunąć kontenery, wpisz:

```bash
docker compose down
```

Dane zapisane w bazie pozostaną zachowane dzięki wolumenowi Dockera.

## Widoki aplikacji

Frontend ma dwa główne widoki.

### Skróć link

Użytkownik wpisuje adres strony internetowej i opcjonalnie własny kod.

Po zatwierdzeniu formularza aplikacja zapisuje link w bazie danych i wyświetla skrócony adres.

Przykład:

- Oryginalny adres: `https://www.google.com`
- Kod: `google`
- Skrócony adres: `http://localhost:8082/api/r/google`

### Moje linki

W tym widoku użytkownik może zobaczyć wszystkie zapisane linki.

Przy każdym linku wyświetlany jest:
- skrócony adres,
- oryginalny adres,
- liczba odwiedzin,
- przycisk do usunięcia linku.

Kliknięcie skróconego adresu przekierowuje użytkownika na właściwą stronę i zwiększa licznik odwiedzin.

## Baza danych

W bazie PostgreSQL znajdują się dwie tabele:

**Tabela `links`**

Przechowuje informacje o skróconych linkach:
- `id` – identyfikator linku,
- `code` – krótki kod,
- `url` – oryginalny adres,
- `created_at` – data utworzenia.

**Tabela `visits`**

Przechowuje informacje o odwiedzinach:
- `id` – identyfikator odwiedzin,
- `link_id` – identyfikator odwiedzonego linku,
- `visited_at` – data odwiedzin.

Tabele są połączone relacją **jeden do wielu (1:N)**. Jeden link może mieć wiele odwiedzin.

Po usunięciu linku usuwane są również jego odwiedziny dzięki `ON DELETE CASCADE`.

Struktura bazy jest zapisana w pliku `database/init.sql`. Przy pierwszym uruchomieniu nowej bazy tworzone są tabele i dodawane przykładowe linki `google` i `youtube`.

Dane są przechowywane w wolumenie `postgres_data`, dzięki czemu nie znikają po restarcie lub ponownym utworzeniu kontenerów.

## API backendu

Backend udostępnia następujące endpointy:

| Metoda | Adres | Działanie |
|---|---|---|
| GET | `/api/link` | Pobranie wszystkich linków i liczby odwiedzin |
| GET | `/api/link/{link_id}` | Pobranie linku na podstawie kodu |
| POST | `/api/link` | Dodanie nowego linku |
| DELETE | `/api/link/{link_id}` | Usunięcie linku |
| GET | `/api/r/{code}` | Przekierowanie i zapisanie odwiedzin |
| GET | `/api/health` | Sprawdzenie stanu backendu |
| GET | `/api/status` | Sprawdzenie działania backendu |
| GET | `/api/db-status` | Sprawdzenie połączenia z bazą |

W adresach `/api/link/{link_id}` parametr `link_id` oznacza krótki kod linku, np. `google`.

### Przykład dodania linku

Żądanie `POST /api/link`:

```json
{
  "link": "https://www.google.com",
  "code": "google"
}
```

Pole `code` jest opcjonalne. Jeśli użytkownik go nie poda, aplikacja wygeneruje losowy kod.

Przykładowa odpowiedź:

```json
{
  "code": "google",
  "link": "https://www.google.com"
}
```

### Przykład pobrania listy linków

Żądanie `GET /api/link`.

Przykładowa odpowiedź:

```json
[
  {
    "code": "google",
    "link": "https://www.google.com",
    "visits": 5
  },
  {
    "code": "wiki",
    "link": "https://www.wikipedia.org",
    "visits": 1
  }
]
```

### Obsługa błędów

Backend sprawdza poprawność danych i zwraca odpowiednie komunikaty:

- **400 Bad Request** – podany kod linku już istnieje.
- **404 Not Found** – nie znaleziono linku o podanym kodzie.
- **422 Unprocessable Entity** – podane dane są niepoprawne, np. adres URL ma zły format.

API można przetestować w Swaggerze pod adresem:

`http://localhost:8082/api/docs`

## Przeprowadzone testy

Podczas pracy nad projektem sprawdziliśmy:

- dodawanie nowych linków,
- wyświetlanie listy linków,
- przekierowywanie na oryginalne strony,
- zliczanie odwiedzin,
- usuwanie linków,
- odrzucanie niepoprawnych adresów URL,
- blokowanie dodawania linków z powtarzającym się kodem,
- obsługę nieistniejących linków,
- zachowanie danych po restarcie kontenerów,
- zachowanie danych po wykonaniu `docker compose down` i `docker compose up -d`.

## Wykorzystanie AI

Podczas realizacji projektu korzystaliśmy z narzędzi AI jako pomocy przy pisaniu kodu, tworzeniu dokumentacji, rozwiązywaniu problemów i nauce Dockera.

Proponowane rozwiązania sprawdzaliśmy i testowaliśmy podczas pracy nad aplikacją.