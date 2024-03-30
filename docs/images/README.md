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
{
  [
    {
        "image": {
            "id": "7b6857c5-33cd-4cb8-af8f-f63e5b75eff9",
            "source": "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/Screenshot%202024-03-29%20at%2013.50.48.png",
            "user": "53947785-3749-410f-879f-82ca9efb7846"
        },
        "analysis": {
            "id": "0f9ab166-8e8e-4535-b1e7-a594ecbd404e",
            "image": "7b6857c5-33cd-4cb8-af8f-f63e5b75eff9",
            "user": "53947785-3749-410f-879f-82ca9efb7846",
            "detections": {
                "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/Screenshot%202024-03-29%20at%2013.50.48.png": [
                    {
                        "bbox": {
                            "x1": 0.7169118,
                            "y1": 0.8469917,
                            "x2": 1.1612395,
                            "y2": 0.901971
                        },
                        "confidence": 0.1828757
                    },
                    {
                        "bbox": {
                            "x1": 0.1538866,
                            "y1": 0.8469917,
                            "x2": 0.3902311,
                            "y2": 0.8936722
                        },
                        "confidence": 0.2011037
                    },
                    {
                        "bbox": {
                            "x1": 0.9852941,
                            "y1": 0.9849585,
                            "x2": 1.0147059,
                            "y2": 1.0129668
                        },
                        "confidence": 0.2324943
                    },
                    {
                        "bbox": {
                            "x1": 0.5084034,
                            "y1": 0.4393153,
                            "x2": 1.0609244,
                            "y2": 0.6830912
                        },
                        "confidence": 0.8227977
                    }
                ]
            }
        }
    },
    {
        "image": {
            "id": "86e99ffc-cc8c-4b4e-8085-7979efa4dedb",
            "source": "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/Screenshot%202024-02-24%20at%2000.11.19.png",
            "user": "53947785-3749-410f-879f-82ca9efb7846"
        },
        "analysis": {
            "id": "72061532-ca4c-4d57-b3f0-6def3f212860",
            "image": "86e99ffc-cc8c-4b4e-8085-7979efa4dedb",
            "user": "53947785-3749-410f-879f-82ca9efb7846",
            "detections": {
                "https://ias-tcd.s3.eu-west-1.amazonaws.com/images/Screenshot%202024-02-24%20at%2000.11.19.png": [
                    {
                        "bbox": {
                            "x1": 0.0536779,
                            "y1": 0.1476982,
                            "x2": 0.1192843,
                            "y2": 0.17711
                        },
                        "confidence": 0.0987038
                    },
                    {
                        "bbox": {
                            "x1": 0.9828529,
                            "y1": 0.266624,
                            "x2": 1.0012426,
                            "y2": 0.3331202
                        },
                        "confidence": 0.1191955
                    },
                    {
                        "bbox": {
                            "x1": 0.2629225,
                            "y1": 0.1473785,
                            "x2": 0.3116303,
                            "y2": 0.1735933
                        },
                        "confidence": 0.1240576
                    },
                    {
                        "bbox": {
                            "x1": 0.2447813,
                            "y1": 0.9574808,
                            "x2": 0.3327535,
                            "y2": 1.0348465
                        },
                        "confidence": 0.1637323
                    },
                    {
                        "bbox": {
                            "x1": 0.9816104,
                            "y1": 0.2189898,
                            "x2": 1.0024852,
                            "y2": 0.3871484
                        },
                        "confidence": 0.1994071
                    },
                    {
                        "bbox": {
                            "x1": 0.0666004,
                            "y1": 0.0460358,
                            "x2": 0.1451292,
                            "y2": 0.1086956
                        },
                        "confidence": 0.2817453
                    },
                    {
                        "bbox": {
                            "x1": 0.2040258,
                            "y1": 0.4133632,
                            "x2": 0.2422962,
                            "y2": 0.4766624
                        },
                        "confidence": 0.4656409
                    }
                ]
            }
        }
    }
]
}
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
