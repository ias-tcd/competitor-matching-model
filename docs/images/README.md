# Images Endpoints

## Feeed image(s) to model for predictions

`POST /images/predictions/`

Content-Type: multipart/form-data

Sample body with two images:

```form-data
{
 --form 'north face=@"/path/to/image/"' \
 --form 'adidas=@"/path/to/image/"'
}
```

Responses:

- 200 Ok -> Occurs upon successful image prediction.
  Response containing a json representation of images and predictions:

```json
[
  {
    "image": {
      "id": "e40b7456-4d8d-45d5-8271-5dad094c03ed",
      "source": "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/53947785-3749-410f-879f-82ca9efb7846/3bf19f0f-0865-45ac-a7db-817dc33fa452_Screenshot%202024-03-29%20at%2013.50.48.png",
      "user": "53947785-3749-410f-879f-82ca9efb7846"
    },
    "analysis": {
      "id": "3e054aae-4fea-45e3-88a2-06eb0a88c9a3",
      "image": "e40b7456-4d8d-45d5-8271-5dad094c03ed",
      "user": "53947785-3749-410f-879f-82ca9efb7846",
      "detections": {
        "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/53947785-3749-410f-879f-82ca9efb7846/3bf19f0f-0865-45ac-a7db-817dc33fa452_Screenshot%202024-03-29%20at%2013.50.48.png": [
          {
            "bbox": {
              "x": 0.7169118,
              "y": 0.8469917,
              "width": 0.4443277,
              "height": 0.0549793,
              "brand": "North Face"
            },
            "confidence": 0.1828757
          },
          {
            "bbox": {
              "x": 0.1538866,
              "y": 0.8469917,
              "width": 0.2363445,
              "height": 0.0466805,
              "brand": "North Face"
            },
            "confidence": 0.2011037
          },
          {
            "bbox": {
              "x": 0.9852941,
              "y": 0.9849585,
              "width": 0.0294118,
              "height": 0.0280083,
              "brand": "North Face"
            },
            "confidence": 0.2324943
          },
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
      "id": "e8164439-37a6-4242-a98f-9591ddf10709",
      "source": "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/53947785-3749-410f-879f-82ca9efb7846/447c647d-6ea3-4872-8fbd-779fbfbc49d7_Screenshot%202024-02-24%20at%2000.11.19.png",
      "user": "53947785-3749-410f-879f-82ca9efb7846"
    },
    "analysis": {
      "id": "c4ebe26f-74e3-4495-961f-4bb240accc85",
      "image": "e8164439-37a6-4242-a98f-9591ddf10709",
      "user": "53947785-3749-410f-879f-82ca9efb7846",
      "detections": {
        "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/53947785-3749-410f-879f-82ca9efb7846/447c647d-6ea3-4872-8fbd-779fbfbc49d7_Screenshot%202024-02-24%20at%2000.11.19.png": [
          {
            "bbox": {
              "x": 0.0536779,
              "y": 0.1476982,
              "width": 0.0656064,
              "height": 0.0294118,
              "brand": "North Face"
            },
            "confidence": 0.0987038
          },
          {
            "bbox": {
              "x": 0.9828529,
              "y": 0.266624,
              "width": 0.0183897,
              "height": 0.0664962,
              "brand": "North Face"
            },
            "confidence": 0.1191955
          },
          {
            "bbox": {
              "x": 0.2629225,
              "y": 0.1473785,
              "width": 0.0487078,
              "height": 0.0262148,
              "brand": "North Face"
            },
            "confidence": 0.1240576
          },
          {
            "bbox": {
              "x": 0.2447813,
              "y": 0.9574808,
              "width": 0.0879722,
              "height": 0.0773657,
              "brand": "New Balance"
            },
            "confidence": 0.1637323
          },
          {
            "bbox": {
              "x": 0.9816104,
              "y": 0.2189898,
              "width": 0.0208748,
              "height": 0.1681586,
              "brand": "New Balance"
            },
            "confidence": 0.1994071
          },
          {
            "bbox": {
              "x": 0.0666004,
              "y": 0.0460358,
              "width": 0.0785288,
              "height": 0.0626598,
              "brand": "Under Armour"
            },
            "confidence": 0.2817453
          },
          {
            "bbox": {
              "x": 0.2040258,
              "y": 0.4133632,
              "width": 0.0382704,
              "height": 0.0632992,
              "brand": "North Face"
            },
            "confidence": 0.4656409
          }
        ]
      }
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
