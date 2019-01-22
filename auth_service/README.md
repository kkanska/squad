# Auth Microservice

Service responsible for authorization of users

## Prerequsites
- Flask
- Requests
- Python3

## Running

Set up `export FLASK_APP`  
Run `flask run`  
Server listens on port **5001**

**Important!** Before first deployment run `flask init-db`


## API

### Login 

```
POST /auth/login
{
    'email': value,
    'password': value
}
```

**Response**:
```
{
    'id': id_of_user_or_-1,
    'email': value,
    'msg': message
}
```

### Register

```
POST /auth/register
{
    'email': value,
    'passoword': value
}
```

**Response**:
```
{
    'id': id_of_user_or_-1,
    'email': value,
    'msg': message
}
```

### For testing

```
/auth
```

Testing of authorization

