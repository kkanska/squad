# Users Microservice

Microservice responsible for handling user data, eg. preferances, settings, usernames etc.


### Prerequisites

Installed docker and docker-compose.


## Installing and deployment

Run 
```
docker-compose up
```
in main folder.
That's all!


## Built With

* [Flask](http://flask.pocoo.org/) - Web microframework
* [Redis](https://redis.io/) - The fastest database engine on this planet
* [redis-py](https://github.com/andymccurdy/redis-py) - Redis Python Client

## License

This project is licensed under the MIT License.

## REST API

### Get user
```
GET /api/users/<int:user_id>
```
**Response:**
JSON containing all user data

### Create user
```
POST /api/users
{
  “key1”: “value1”,
  “key2”:”value2”,
}
```
**Response:**
```
{
  “id”: <int:user_id>,
  “key1”: “value1”,
  “key2”:”value2”,
}
```

### Update user
```
PATCH /api/users/<int:user_id>
{
  “key1_to_change”: “new_value”,
  “new_key”: ”value”,
}
```
**Repsonse:**
JSON containg all user data


### RANK user
```
PATCH /api/rank/<int:user_id>
{
  “rating" : "value",
  "match_id": "value",
}
```
**Repsonse:**
Status Code 202
