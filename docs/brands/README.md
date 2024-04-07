# Brands Endpoints

## List all brands

`GET /brands/brands/`

Content-Type: application/json

Responses:

- 200 Okay -> Occurs upon successful list
  Response contains a json representation of the brands as follows:

```json
[
  {
    "id": "8f5cdeb6-c05c-41aa-9010-585a366f4ea5",
    "created_at": "2024-03-27T23:26:03.771923Z",
    "updated_at": "2024-03-27T23:26:03.771923Z",
    "name": "Lululemon",
    "logo": "https://logos-world.net/wp-content/uploads/2020/09/Lululemon-Emblem-700x394.png"
  },
  {
    "id": "048cf461-ae86-444d-b25f-d22cd41bca1e",
    "created_at": "2024-03-27T23:26:03.776004Z",
    "updated_at": "2024-03-27T23:26:03.776004Z",
    "name": "New Balance",
    "logo": "https://logos-world.net/wp-content/uploads/2020/09/New-Balance-Logo-1972-2006-700x394.png"
  }
]
```

## Get an individual brand

`GET /brands/brands/<brand id>/` where `<brand id>` is the UUID of the brand as shown above in the `id` value of the json

Content-Type: application/json

Responses:

- 200 Okay -> Occurs if a brand with that id exists in the database
  Response contains a json representation of the brand as follows:

```json
{
  "id": "8f5cdeb6-c05c-41aa-9010-585a366f4ea5",
  "created_at": "2024-03-27T23:26:03.771923Z",
  "updated_at": "2024-03-27T23:26:03.771923Z",
  "name": "Lululemon",
  "logo": "https://logos-world.net/wp-content/uploads/2020/09/Lululemon-Emblem-700x394.png"
}
```

- 404 Not Found -> Occurs if no brand with that id exists in the database
