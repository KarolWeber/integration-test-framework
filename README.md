# ⚠️Repozytorium tylko do wglądu

---

# Integration Test Framework 

Framework do pisania i uruchamiania testów automatycznych dla platformy
kasynowej.

---

## Spis treści

- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Struktura projektu](#struktura-projektu)
- [Jak pisać nowe testy](#jak-pisać-nowe-testy)
- [Przykładowy test](#przykładowy-test)
- [Serwisy](#serwisy)
- [Uruchamianie testów](#uruchamianie-testów)
- [Logowanie i raportowanie](#logowanie-i-raportowanie)
- [Jakość kodu](#jakość-kodu)

---

## Instalacja

Framework działa na Python 3.13.7.
Instalacja wymaganych bibliotek

```bash
pip install -r requirements.txt
```

---

## Konfiguracja

Należy skonfigurować zmienne środowiskowe w pliku .env

- PLAYER_API='url'
- ADMIN_API='url'
- PROVIDER_ONE='url'
- PROVIDER_ONE_ORIGIN='url'
- PROVIDER_TWO='url'
- PLAYER_EMAIL='@example.com'
- ADMIN_TEST_USERNAME='username@example.com'
- ADMIN_TEST_PASSWORD='password'

---

## Struktura projektu

- api -> Klienci i serwisy API
    - clients -> Klienci do komunikacji API
    - services -> Serwisy logiki biznesowej
    - request_api.py -> Wysyłka żądań HTTP
- entities -> Encje i modele danych zwracanych przez API
- infrastructure -> Pliki konfiguracyjne
- tests -> Folder z testami
- urls -> Adresy URL API
- utils -> Funkcje pomocnicze
    - assertions -> Funkcje budujące asercje i raporty
    - cleanup -> Funkcje czyszczące środowisko
    - converters -> Konwertery danych
    - enums -> Enumy
    - files -> Funkcje zarządające plikami
    - generators -> Generatory danych
    - logging -> Logowanie testów
    - mappers -> Mappery
    - payloads -> Payloady
    - reports -> Konwersja raportu allure do jednolitego pliku HTML
    - resources -> Pliki używane w testach
    - waiters -> Funkcje oczekujące na określone warunki

---

## Jak pisać nowe testy

Każdy test w frameworku powinien mieć spójny układ i wykorzystywać wspólne komponenty.

Powinien mieć określony tytuł `@allure.title()` oraz wpływ `@allure.severity()` </br>
Allure umożliwia wykorzystanie następującuch poziomów:

- BLOCKER
- CRITICAL
- NORMAL
- MINOR
- TRIVIAL

W celu prawidłowego raportowania należy w teście przekazać obiekt request, używany przez pytest. </br>
Na początku testu należy zainicjalizować klasę asercji `CheckAssertions`, która odpowiada za:

- dodawanie i przechowywanie asercji,
- sprawdzanie wyników testu,
- generowanie czytelnych raportów w Allure (sekcja stdout),
- automatyczne tworzenie nazw testów na podstawie ich ścieżki.

Metoda `assertion()` klasy `CheckAssertions` umożliwia dodanie wielu asercji do jednego testu,
natomiast metoda `check_assertions()` uruchamia ich weryfikację i zwraca wynik końcowy testu.

---

## Przykładowy test

```
@allure.title('Provider one player authentication') # Tytuł testu
@allure.severity(allure.severity_level.NORMAL) # Wpływ testu
def test_provider_one_player_authentication(self, request): 
    ca = CheckAssertions(request=request) -# Inicjalizacja klasy asercji
    
    player = PlayerService() # Inicjalizacja kontekstu gracza
    player.user.login() # Logowanie gracza

    admin = AdminService() # Inicjalizacja kontekstu administratowa
    admin.user.login() # Logowanie administratora
    game = admin.technical.game.create_custom_game() # Stworzenie gry technicznej przez administratora

    player_run_game = player.game.run_provider_one_game(game=custom_game) # Uruchomienie sesji gry 

    ca.assertion( # Dodanie asercji
                 name="Provider one authenticate status", # Nazwa asercji
                 expected="SUCCESS", # Spodziewany wynik testu
                 current=player_run_game.authenticate_status, # Uzyskany rezultat
                 operator='eq' # Operator asercji
                )
    ca.check_assertions() # Uruchomienie sprawdzenia asercji i wygenerowanie raportu
```

---

## Serwisy

Framework udostępnia zestaw serwisów umożliwiających komunikację z API i
wykonywanie operacji testowych. </br>
Każdy serwis odpowiada za określony obszar funkcjonalny platformy.

- AdminService -> umożliwia zarządzanie platformą kasynową (np. użytkownikami,
  grami, bonusami).

- PlayerService -> umożliwia operacje po stronie gracza, takie jak logowanie,
  uruchamianie gier czy rozgrywki.

<u>Obecnie obsługują jedynie podstawowy zakres operacji niezbędnych do testów
integracji z dostawcami.</u>

- ProviderOneService – obsługuje integrację z API dostawcy Provider One, m.in. autoryzację,
  obstawianie zakładów i wypłaty wygranych.
- ProviderTwoService – obsługuje integrację z API dostawcy Provider Two, m.in. autoryzację,
  obstawianie zakładów i wypłaty wygranych.

---

## Uruchamianie testów

***

Uruchamianie wszystkich testów:

```bash
pytest
```

***

Uruchamianie testów z wybranymi tagami(np. integration_test_provider_one):

```bash
pytest -m integration_test_provider_one
```

Lista dostępnych tagów znajduje się w pliku pytest.ini

***

Uruchamianie testów wraz z generowaniem raportu allure:

```bash
pytest --alluredir=allure-result
```

***

Uruchomienie raportu lokalnie:

```bash
allure serve allure-results
```

***

Generowanie raportu po zakończeniu sesji testowej:

```bash
allure generate
```

Aby wygenerować raport w scalonym pliku HTML po wygenerowaniu raportu należy
uruchomić skrypt `utils/reports/report_generator.py`

---

## Logowanie i raportowanie

- Framework wykorzystuje Allure do raportowania wyników testów.
- Klasę StepLogger stosujemy do logowania kroków testu i odpowiedzi API.
- Klasę CheckAssertions wykonywanuje wiele asercji nie zakańczając testu póki
  nie zostaną sprawdzone wszystkie, w przypadku kiedy jedna z asercji w jednym
  teście z pełnym opisem, wartościami oczekiwanymi i uzyskanymi.

---

## Jakość kodu

Projekt wykorzystuje `flake8` do statycznej analizy kodu i utrzymania zgodności ze standardem PEP8.

Uruchomienie analizy kodu:

```bash
flake8 .
```

---