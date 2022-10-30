
from fastapi.testclient import TestClient
from main import app
import numpy as np
import cv2
from PIL import Image
from io import BytesIO

# # function to read 
# def read_image(path):
#     with open(path, "rb") as f:
#         return bytearray(f.read())

# create input image
image = np.full((1200, 1200,3), 250, dtype="uint8")
cv2.putText(
    image,
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
    (80, 250),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.2,
    0,
    3,
)

# save input image to disk
input_image_path = "input_image.png"
cv2.imwrite(input_image_path, image)

# send image to server and get response
client = TestClient(app)
file = {'upload_file': open(input_image_path,'rb')}
response = client.post("/augment", files = file)

# decode bytes array back into image
image_augmented = Image.open(BytesIO(response.content))
image_augmented_numpy = np.asarray(image_augmented)

# save the augmented image
cv2.imwrite("augmented_image.png", image_augmented_numpy)