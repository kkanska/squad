## Na potrzeby projektu na przedmiot "JNP3 : Projektowanie wysokowydajnych serwisów webowych", projekt został wzbogacony o możliwość generowania meczy z wyborem:
 - współrzędnych boiska
 - id autora wprowadzającego informacje do systemu
 - godziny rozpoczęcia i zakończenia rozgrywek
 - długości pojedyńczego meczu
 - daty rozpoczęcia i zakończenia rozgrywek
 - listy id graczy oddzielonych spacjami lub przecinkami
 - dyscypliny
 
#### Aplikacja korzysta z kolejki RabbitMQ oraz Celery workerów do dodawania pojedyńczych meczy do bazy danych.
Dzięki temu użytkownik aplikacji nie musi czekać, aż zadanie zostanie wykonane. Na stronie jest on informowany że 
workerzy wkrótce dodadzą nowe mecze do bazy danych.

#### Aplikacja używa zpartycjonowanej tabeli trzymającej informacje o meczech.
##### Do partycjonowania został wykorzystane narzędzie *Architect*
Tabela **Match** podzielona została na 6 części, każda z nich trzymająca mecze zaczynające się w godzinach z 
przedziału <4 * num - 4, 4 * num) gdzie num to numer części.

## POST /matches/
```
    {
            "location": "SRID=4326;POINT (21.04090086919246 53.81391628442898)",
            "author_id": 15,
            "date": "2018-05-11",
            "discipline": 1,
            "players": [
                1,
                2,
                4
            ]
    }
```
## GET /matches/?lat={latitide}&lng={longitude}&radius={radius_in_meters}&author={user_id}&date={string_yyyy-mm-dd}[&player={player_id}]
```
    [
        {
            "id": 1,
            "location": "SRID=4326;POINT (20.04090086919246 52.81391628442898)",
            "author_id": 10,
            "date": "2018-06-11",
            "discipline": 0,
            "players": [
                3
            ]
        },
        {
            "id": 2,
            "location": "SRID=4326;POINT (21.04090086919246 53.81391628442898)",
            "author_id": 15,
            "date": "2018-05-11",
            "discipline": 1,
            "players": [
                1,
                2,
                4
            ]
        }
    ]
```
## PATCH /matches/
```
    {
    "id":2,
    "new_player":10
    }
```
or
```
    {
    "id":2,
    "remove_player":10
    }
```
or
```
    {
    "id":2,
    "location":"SRID=4326;POINT (21.04090086919246 53.81391628442898)"
    }
```
or
```
    {
    "id":2,
    "date":"2018-05-11"
    }
```

## GET /matches/<match_id>

## PUT /matches/<match_id>

## DELETE /matches/<match_id>