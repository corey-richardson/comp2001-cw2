# comp2001-cw2

[![wakatime](https://wakatime.com/badge/user/55c30436-1509-4eb9-9f18-fa9b7c6060c4/project/5f7a8f4f-1835-4c5e-9247-f8f017771ee8.svg)](https://wakatime.com/@coreyrichardson/projects/ouktfmbpqg?start=2024-12-28&end=2025-01-07)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MicrosoftSQLServer](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Running the API via Docker

### Building the Container

<!-- RUN FROM FROM /cw2 -->
```bash 
docker build -t trails-api .
docker login
docker tag trails-api coreyrichardson1/trails-api
docker push coreyrichardson1/trails-api
```

### Pulling and Running the Container

```bash
docker pull coreyrichardson1/trails-api
docker run -p 8000:8000 coreyrichardson1/trails-api
```
```
 * Serving Flask app 'config'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.17.0.2:8000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 662-058-616
```

The Flask application should be found running [here](http://127.0.0.1:8000).

## API Authentication

All users have access to `READ`/`GET` endpoints, and to the **Authentication** `POST` endpoint `/login`.

To gain access to `CREATE`/`POST`, `UPDATE`/`PUT` and `DELETE`/`DELETE` endpoints, use the `Authentication` endpoint to generate a JWT token and then include this as the `Authorization` header in the format `Bearer <TOKEN>`. This token will expire after an hour.

The following table lists the valid accounts provided in the coursework specification. These accounts have, or any other found in the provided authenticator API, will be given the `ADMIN` role. 

Email                | Password
---                  | ---
grace@plymouth.ac.uk | ISAD123!
tim@plymouth.ac.uk   | COMP2001!
ada@plymouth.ac.uk   | insecurePassword

Send the following `POST` request body to `/login`:

```json
{
    "email" : "grace@plymouth.ac.uk",
    "password" : "ISAD123!"
}
```

This will return a JWT token in the following format:

```json
{
    "token": "<header>.<payload>.<signature>"
}
```

Copy the value of `token` and include it as the value for a header named `Authorization` in your requests, with a `Bearer ` prefix.

```
Authorization:Bearer <token>
```

Without this header present in your request, the routes will be protected and will return you `401 Missing Token`. Other possible responses are `401 Token Expired` and `401 Invalid Token`. Tokens expire 1 hour after generation.

Refer to [Authentication.py](cw2\Project\Authentication.py) for route protection implementation.