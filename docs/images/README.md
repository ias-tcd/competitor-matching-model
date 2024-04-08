# Images Endpoints

## Feed image(s) to model for predictions

`POST /images/predictions/`

Content-Type: multipart/form-data

Sample body with two images, with north face (takes in the brand id in the database) as a selected brand:

```form-data
{
 --form 'north face=@"/Users/dhruv/Pictures/Screenshots/Screenshot 2024-03-29 at 13.50.48.png"' \
--form 'adidas=@"/Users/dhruv/Pictures/Screenshots/Screenshot 2024-02-24 at 00.11.19.png"' \
--form 'brands="4048334f-e761-407e-8b68-3643bb3ee7a5"'
}
```

Responses:

- 200 Ok -> Occurs upon successful image prediction.
  Response containing a json representation of images and predictions:

```json
[
  {
    "image": {
      "id": "83b039de-a355-428a-8b26-133423e04b7c",
      "source": "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/53947785-3749-410f-879f-82ca9efb7846/15a6056f-82fa-4a97-8531-3253c7649a5f_Screenshot%202024-03-29%20at%2013.50.48.png",
      "user": "53947785-3749-410f-879f-82ca9efb7846"
    },
    "analysis": {
      "id": "f1c92dd0-072d-4416-9a19-264d8f2f913c",
      "image": "83b039de-a355-428a-8b26-133423e04b7c",
      "user": "53947785-3749-410f-879f-82ca9efb7846",
      "detections": {
        "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/53947785-3749-410f-879f-82ca9efb7846/15a6056f-82fa-4a97-8531-3253c7649a5f_Screenshot%202024-03-29%20at%2013.50.48.png": [
          {
            "bbox": {
              "x": 0.5084034,
              "y": 0.4393153,
              "width": 0.552521,
              "height": 0.2437759,
              "brand": "North Face"
            },
            "confidence": 0.8227977
          }
        ]
      }
    }
  },
  {
    "image": {
      "id": "f0796e50-4e9c-4a08-bfed-b2506cfa7fbb",
      "source": "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/53947785-3749-410f-879f-82ca9efb7846/dbbcb517-34ee-4499-b37e-c0a8557517aa_Screenshot%202024-02-24%20at%2000.11.19.png",
      "user": "53947785-3749-410f-879f-82ca9efb7846"
    },
    "analysis": {
      "id": "81102f37-373b-4150-a97c-811b68afa7d4",
      "image": "f0796e50-4e9c-4a08-bfed-b2506cfa7fbb",
      "user": "53947785-3749-410f-879f-82ca9efb7846",
      "detections": {}
    }
  }
]
```

- 403 Forbidden -> Occurs if:

  - Request was not authenticated
    - authentication token is invalid
    - authentication token is expired: needs to be refreshed
    - authentication token is missing
    - passwords do not match
    - authentication credentials fields are blank or invalid

- 400 Bad Request -> Occurs if:
  - No images were passed in the request
