from fastapi import File, UploadFile,FastAPI
from fastapi.responses import FileResponse
import numpy as np


app = FastAPI()


@app.post("/")
async def upload(file: UploadFile = File(...)):
    message = "Done!"
    out_response = None
    read_status  = 1
    
    try:
         contents = await file.read()
         np_array = np.fromstring(contents, np.uint8)
         
         
         # augmented_image = open('augmented_image.png', 'wb')
         # augmented_image.write(base64.b64decode((np_array)))
         # augmented_image.close()                
         
         # image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
         # cv2.imwrite("augmented_image.png", image)
         # out_response = FileResponse("augmented_image.png")
    except:
        message = "There was an error in uploading the file."
        read_status = 0

        
    return out_response if out_response is not None else message
