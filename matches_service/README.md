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