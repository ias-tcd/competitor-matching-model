from .process import process

input_image_path = "C:/Users/pengh/Pictures/test/adidas_shoes.jpg"
inferences = process(input_image_path, ".")

for inference in inferences:
    print("x: ", inference.bounding_box.x)
    print("y: ", inference.bounding_box.y)
    print("Width: ", inference.bounding_box.w)
    print("Height: ", inference.bounding_box.h)
    print("Confidence score: ", inference.confidence)
    print("")
