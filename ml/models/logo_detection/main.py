from process import process

input_image_path = ""
inferences = process(input_image_path)

for inference in inferences:
    print("x: ", inference.boundingBox.x)
    print("y: ", inference.boundingBox.y)
    print("Width: ", inference.boundingBox.w)
    print("Height: ", inference.boundingBox.h)
    print("Confidence score: ", inference.confidence)
    print("")
