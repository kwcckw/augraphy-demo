from fastapi import File, UploadFile,FastAPI
from fastapi.responses import FileResponse
from augraphy import *
import cv2
import numpy as np
import os
import io
from starlette.responses import StreamingResponse

app = FastAPI()


@app.post("/")
async def upload(file: UploadFile = File(...)):
    message = "Augmentation done!"
    out_response = None
    read_status  = 1
    # current_path = os.path.abspath(os.getcwd()) + "/"
    
    try:
         contents = await file.read()
    except:
        message = "There was an error in uploading the file."
        read_status = 0
   
    if read_status:
        try:
            augmented_image = augment_image(contents)
            
            _, img_bytes = cv2.imencode(".png", augmented_image)
            out_response = StreamingResponse(io.BytesIO(img_bytes.tobytes()), media_type="image/png")
            # out_response = FileResponse(current_path+ "augmented_image.png")
        except Exception:
            message = Exception #"Invalid file type!"   
        
    return out_response if out_response is not None else message



def augment_image(contents: str):
    # current_path = os.path.abspath(os.getcwd()) + "/"
    np_array = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    augmented_image = image
    
    # cv2.imwrite(current_path+"input_image.png", image)
    
    ink_phase   = [InkBleed(p=1)]
    paper_phase = [DirtyRollers(p=1)]
    post_phase  = [WaterMark(p=1)]
    pipeline    = AugraphyPipeline(ink_phase, paper_phase, post_phase)
    
    data_output = pipeline.augment(image)
    augmented_image = data_output["output"]
    
    
    # cv2.imwrite(current_path+"augmented_image.png", augmented_image)

    return augmented_image