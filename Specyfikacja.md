![Squad logo](https://gitlab.com/squad.dev/squad/raw/master/static/squad_logo.png)


# Specyfikacja projektu

Projekt ma na celu stworzenie aplikacji mobilnej ułatwiającej użytkownikom znajdowanie kompanów do gry w piłkę nożną i inne dyscypliny sportowe.


Użytkownicy rejestrują się w aplikacji lub logują przez Facebooka, następnie zaznaczają na mapie miejsce, w którym najczęściej grają,
oraz odległość, jaką są skłonni przebyć, żeby zagrać mecz. Po zalogowaniu widzą mecze w okolicy, w której grają,
możliwe do filtrowaniapo zakresie czasowym, w którym będą się odbywać (dzisiaj, jutro, ten tydzień itd.).
Użytkownicy mogą także stworzyć nowy mecz w lokalizacji wybranej z listy boisk.
Twórca meczu dostaje powiadomienia o kolejnych graczach, którzy dołączyli do jego meczu.
Użytkownik ma dostęp do listy meczy, w których zadeklarował udział.
Dla każdego meczu utworzony jest osobny czat.
Jeżeli użytkownik zaznaczy, że szuka meczu, to dostaje powiadomienie o każdym nowo utworzonym meczu w jego okolicy.
Po rozegranym meczu gracze oceniają pozostałych graczy (pod kątem punktualności, kultury meczu itd., ale nie umiejętności).



## Definicje 

* **Mecz aktywny** to mecz utworzony w systemie, który jeszcze się nie odbył.

* Role w meczu:
    - **autor** - użytkownik, który utworzył mecz
    - **administrator** - użytkownik, który ma uprawnienia do zmiany ustawień meczu (MATCH.EDIT)
    - **uczestnik** - użytkownik, który bierze udział w meczu

## Wymagania funkcjonalne

* AUTH.
    1. Rejestracja
        1. Przez Facebooka
             1. Autoryzacja aplikacji
             2. Nazwa użytkownika ustawiana na automatycznie na nazwę z Facebooka
             3. Adres email ściągnięty z Facebooka
        1. Przez adres email
             1. Nazwa użytkownika do wprowadzenia
             2. Hasło
    2. Logowanie
        1. Przez Facebooka
        2. Przez adres email
* USER.
    - EDIT.
        1. Edycja profilu
            1. Zmiana promienia, w jakim system szuka meczu
            2. Zmiana punktu na mapie, w okolicy którego system szuka meczu
            3. Włączanie / wyłączenie powiadomień (checkboxy) jak w MATCH.NOTIF.1 oraz CHAT.NOTIF.1
            4. Dodawanie zdjęcia i opisu
            5. Wybór dyscyplin, dla których system będzie wyszukiwał mecze
            6. Edycja czasów i liczby wysłanych powiadomień typu MATCH.NOTIF.1.5 przed meczem
        2. Integracja konta
            1. Z Facebookiem
    - VIEW.
        1. Przeglądanie profili użytkowników - dostęp do ogólnych statystyk:
            1. Odsetek gier, na których użytkownik się nie pojawił
            2. Zestawione opinie innych użytkowników o graczu (jak w RANKING.1)
            3. Lista wspólnych meczy z użytkownikiem
        4. Lista użytkowników, z którymi wspólnie graliście
    - NOTIF.
        1. Powiadomienia
            1. Znajomy dołączył do aplikacji
* MATCH.
    - EDIT.
        1. Utworzenie nowego meczu
            1. Wybór dyscypliny
            2. Wybór ilości graczy: wartość minimalna, maksymalna
            3. Wybór daty i godziny
            4. Wybór wyjściowej lokalizacji (spośród miejsc zaznaczonych na mapie)
            5. Warunki zmiany daty/godziny: za zgodą przynajmniej n użytkowników, n - do wyboru
            6. Wybór czasu na zbranie się minimalnej liczby uczestników 
        2. Przekazanie praw administratora meczu innej osobie (obowiązkowe w przypadku, gdy autor meczu chce z niego zrezygnować)
            1. Osoba spośród uczestników danego meczu
        3. Zmiana ustawień meczu (tylko administrator meczu)
            1. Zmiana lokalizacji miejsca gry
            2. Zmiana terminu
        4. Usunięcie uczestnika meczu przez administratora
        5. Blokowanie użytkowników przez administratora meczu (nie mogą dołączyć i nie można do nich wysłać zaproszenia)
    - VIEW.
        1. Przeglądanie aktywnych meczów
            1. Przeglądanie aktywnych meczów na mapie
            2. Przeglądanie aktywnych meczów znajdujących się w obszarze promienia wyszukiwania od wybranej lokalizacji w postaci listy. 
                1. Możliwość sortowania po: dacie, odległości, znajomych
                2. Możliwość zmiany promienia wyszukiwania
        2. Przeglądanie listy aktywnych meczów, których jesteśmy uczestnikami
        3. Dołączenie do aktywnego meczu
        4. Anulowanie obecności w meczu
    - NOTIF.
        1. Powiadomienia
            1. Mecze w okolicy
            2. Zmiana składu meczów, których użytkownik jest uczestnikiem (dołączenia, opuszczenia meczu)
            3. Zmiana miejsca/terminu
            4. Zmiana administratora meczu
        5. Zbliża się termin meczu, w którym uczestniczymy
        6. Nie zebrał się skład meczu przed terminem określonym w MATCH.EDIT.6
        7. Zebrał się minimalny wymagany skład
    - AUTO.
        1. Mecz jest anulowany, jeśli przed terminem określonym w MATCH.EDIT.6 nie zbierze minimalna liczba uczestników określona w MATCH.EDIT.1.2
* INVITE.
    1. Wysłanie zaproszenia do meczu
        1. Wyszukiwanie użytkowników jak w SEARCH, możliwość zaznaczania checkboxów na liście
        2. Sugestie ostatnio zapraszanych użytkowników (z checkboxami)
        3. Każdy uczestnik meczu lub osoba, która otrzymała zaproszenie do tego meczu może wysłać zaproszenie
    2. Przeglądanie zaproszeń do aktywnych meczów
        1. Od kogo
        2. Na jaki mecz (link)
        3. Opcje: przyjmuję, odrzucam, chcę obserwować (otrzymywać powiadomienia o zmianie miejsca/terminu, dołączających uczestnikach)
* CHAT.
    - VIEW.
        1. Rozmowa z współgraczami odbytych i aktywnych meczów (tylko wiadomości tekstowe)
        2. Konwersacje 1-1 oraz grupowe
    - NOTIF.
        1. Powiadomienie o nowej wiadomości
* RANKING.
    1. Wystawienie oceny innym graczom po meczu
        1. punktualność (skala 1-5)
        2. *ogólna kultura osobista* (skala 1-5)
* SEARCH.
    1. Wyszukiwanie użytkowników:
        1. Po nazwie
        2. Po emailu
    2. Autocomplete z rozwijaną listą podpowiedzi


## Wymagania niefunkcjonalne

1. Niezawodność i stabilność
    1. Maksymalny czas niedostępności &lt;30% w godzinach 9-20
2. Wydajność i przepustowość
    1. Powiadomienia i komunikacja real-time z maksymalnym opóźnieniem &lt;30s
    2. Obsługa liczby użytkowników &lt;1000
    3. Bezawaryjna obsługa co najmniej 10 żądań/s. 
3. Dostępność
    1. Wsparcie dla czytników ekranów
    2. Dostępność na platformach mobilnych: iOS, Android
    3. Dostępność przez przeglądarkę internetową
4. Jakość
    1. Dostarczenie czytelnego kodu źródłowego i nowoczesnej formy wizualnej
    2. Zgodność stylu kodu z nowoczesnymi wytycznymi
        1. Frontend - ES6, AirBnB
        2. Backend - PEP8
5. Prywatność i bezpieczeństwo
    1. Zapewnienie bezpieczeństwa danych użytkowników i ich prywatności poprzez szyfrowanie i autoryzację
6. Utrzymanie
    1. Kontrola działania serwisu w czasie zakładanego czasu funkcjonowania
7. Rozszerzalność (poprzez zmiany w kodzie)
    1. Możliwość rozszerzania o nowe dyscypliny sportowe
8. Dokumentacja techniczna
    1. Dokumentacja w kodzie
9. Testy
    1. Dostarczenie testów jednostkowych
10. Licencjonowanie
    1. MIT




```
Version: #2
Last-modif: 2018/04/17 08:52
Author: Piotr Aleksander Styczyński


Commit-hash: 9936e843887bf7a05a949bbf2ca0a688ab705b01
```
