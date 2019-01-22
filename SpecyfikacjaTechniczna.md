![Squad logo](https://gitlab.com/squad.dev/squad/raw/master/static/squad_logo.png)

Projekt ma na celu stworzenie aplikacji mobilnej ułatwiającej użytkownikom znajdowanie kompanów do gry w piłkę nożną i inne dyscypliny sportowe.

# Specyfikacja techniczna projektu

* **Architektura systemu**
  * *FRONTEND*
  * *GATE*
  * *AUTH*
  * *MATCH*
  * *USER*
* **API**
  * *GATE*
  * *AUTH*
  * *MATCH*
  * *USER*

## Architektura systemu

![Components diagram](https://gitlab.com/squad.dev/squad/raw/master/static/architektura.png)

System ma typową *architekturę mikroserwisową*.

Definicje:
  * sieć mikroserwisowa - wewnętrzna sieć połączeń pomiędzy mikroserwisami a bramą, do której uzytkownik ma jedynie dostęp pośredni poprzez bramę

Każdy mikroserwis posiada osobną bazę danych dotyczącą funkcjonalości jaką ten serwis oferuje.

### FRONTEND *(Aplikacja użytkownika)*

Aplikacja ma możliwość kierowania zapytań wyłącznie do bramy. Z punktu widzenia aplikacji nie istnieje żaden inny serwis poza bramą.

### GATE *(Brama)*

Wszystkie zapytania o dane z aplikacji użytkownika kierowane są do serwera-bramy, który rozpatruje zapytania i asynchronicznie odpytuje pozostałe serwisy o dane.<br>
Po uzupełnieniu danych potrzebnych do odpowiedzi wysyła komunikat zwrotny do aplikacji użytkownika.

Brama odpowiada również za kontrolę i optymalizację ruchu.

 * W przypadku zbyt dużej liczby zapytań może zwrócić odpowiedni błąd HTTP
 * Brama zapewnia podstawową obsługę cache w przypadkach, w których jest to możliwe, aby w przypadku podobnych zapytań nie generować zbyt dużego ruchu wewnątrz sieci mikroserwisowej

API bramy jest sformułowane za pomocą języka GraphQL (zob. *sekcja API.GATE*)

### AUTH *(Autoryzacja)*

Serwis odpowiadający za obsługę żądań bramy odnośnie autoryzacji zgodnych ze specyfikacją (*zob. specyfikacja sek. AUTH*)

* Serwis posiada niezależną bazę danych SQLite o danych dostępu użytkowników
* Serwis komunikuje się z zewnętrznym API serwisu Facebook w celu udostępnienia możliwości logowani/rejestracji przez Facebook

### MATCH *(Zarządzanie meczami)*

Serwis odpowiadający za obsługę żądań bramy związanych z interakcją użytkowników z meczami (*zob. specyfikacja sek. MATCH*)

* Serwis posiada niezależną bazę danych PostGIS zawierającą dane geolokalizacyjne odnośnie wszystkich meczy przechowywanych w serwisie

### USER *(Zarzadzanie użytkownikami)*

Serwis odpowiadający za obsługę żądań bramy związanych z zarządzaniem danymi użytkowników w serwisie (*zob. specyfikacja sek. USER*)

* Serwis posiada niezależną bazę danych MongoDB przechowującą dane o użytkownikach (dane o profilach i wszystkie inne wymagane do realizacji zadań zgodnych ze specyfikacją)

![Detailed components diagram](https://gitlab.com/squad.dev/squad/raw/master/static/architektura_detale.png)


## API

### GATE
[Repozytorium](https://gitlab.com/squad.dev/gate_service/blob/master/API%201.1.md)

### AUTH
[Repozytorium](https://gitlab.com/squad.dev/auth/blob/master/README.md)

### MATCH
[Repozytorium](https://gitlab.com/squad.dev/matches_service/blob/master/README.md)

### USER
*Jeszcze nie zaimplementowane*

