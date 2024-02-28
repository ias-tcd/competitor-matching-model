# Accounts Endpoints

## Register a new user

`POST /accounts/register/`

Content-Type: application/json
Sample body:

```json
{
  "first_name": "",
  "last_name": "",
  "email": "",
  "password": "",
  "confirm_password": ""
}
```

Responses:

- 201 Created -> Occurs upon successful register.
  Response contains a json representation of the created user:

```json
{
  "first_name": "",
  "last_name": "",
  "email": ""
}
```

- 400 Bad Request -> Occurs if:
  - passwords do not match
  - any of the fields are blank
  - email is invalid
  - email is already used
  - password is too common

## Login an existing user

`POST /accounts/login/`

Content-Type: application/json
Sample body:

```json
{
  "email": "",
  "password": ""
}
```

Responses:

- 200 Okay -> Occurs upon successful login.
  Response containing the access and refresh tokens for future authentication:

```json
{
  "refresh": "",
  "access": ""
}
```

- 400 Bad Request -> Occurs if:
  - password does not match
  - any of the fields are blank
  - email is invalid
  - email does not correspond to an existing user in the database

# Refresh an existing access token

`POST /accounts/login/refresh/`

Content-Type: application/json
Sample body:

```json
{
  "refresh": ""
}
```

Responses:

- 200 Okay -> Occurs upon successful token refresh.
  Response containing the access and refresh tokens for future authentication:

```json
{
  "refresh": "",
  "access": ""
}
```

- 400 Bad Request -> Occurs if:
  - refresh token does not correspond to a currently **active** refresh token for a user
  - any of the fields are blank
