from fastapi import File, UploadFile,FastAPI
from fastapi.responses import FileResponse
from augraphy import *
import cv2
import numpy as np

app = FastAPI()


@app.post("/augment")
async def upload(file: UploadFile = File(...)):
    message = "Augmentation done!"
    out_response = None
    read_status  = 1
    
    
    try:
         contents = await file.read()
    except:
        message = "There was an error in uploading the file."
        read_status = 0
   
    if read_status:
        try:
            augmented_image = augment_image(contents)
            out_response = FileResponse("augmented_image.png")
        except Exception:
            message = Exception #"Invalid file type!"   
        
    return out_response if out_response is not None else message



def augment_image(contents: str):
    
    np_array = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    augmented_image = image
    
    # cv2.imwrite("input_image.png", image)
    
    # ink_phase   = [InkBleed(p=1)]
    # paper_phase = [DirtyRollers(p=1)]
    # post_phase  = [WaterMark(p=1)]
    # pipeline    = AugraphyPipeline(ink_phase, paper_phase, post_phase)
    
    # data_output = pipeline.augment(image)
    # augmented_image = data_output["output"]
    
    
    cv2.imwrite("augmented_image.png", augmented_image)

    return augmented_image