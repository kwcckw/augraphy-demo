from fastapi import FastAPI, File, UploadFile, Form, status
from fastapi.exceptions import HTTPException
from augraphy import *
import cv2
import numpy as np
import os
import io
from starlette.responses import StreamingResponse
import aiofiles

app = FastAPI()
CHUNK_SIZE = 16 * 16


@app.post("/")
async def upload(file: UploadFile = File(...), file_name: str = Form(...)):
    message = "Augmentation done!"
    out_response = None
    read_status  = 1

    try:
        filepath = os.path.join('./', os.path.basename(file.filename))
        async with aiofiles.open(filepath, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
        image = cv2.imread(filepath)
        
    except Exception:
        read_status = 0
        message = "There was an error uploading the file"
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='There was an error uploading the file')

    finally:
        await file.close()

    # read successfully, proceed with augmentation
    if read_status:
        try:
            augmented_image = augment_image(image)     
            _, img_bytes = cv2.imencode(".png", augmented_image)
            out_response = StreamingResponse(io.BytesIO(img_bytes.tobytes()), media_type="image/png")
        except Exception:
            message = Exception #"Invalid file type!"   
        
    return out_response if out_response is not None else message



def augment_image(image):

    ink_phase   = [InkBleed(p=1)]
    paper_phase = [DirtyRollers(p=1)]
    post_phase  = [WaterMark(p=1)]
    pipeline    = AugraphyPipeline(ink_phase, paper_phase, post_phase)
    
    data_output = pipeline.augment(image)
    augmented_image = data_output["output"]

    return augmented_image