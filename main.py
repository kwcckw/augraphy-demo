from fastapi import FastAPI, File, UploadFile, Form, status
from fastapi.exceptions import HTTPException
from augraphy import *
import cv2
import numpy as np
import os
import io
from time import time
from starlette.responses import StreamingResponse
import aiofiles


app = FastAPI()
CHUNK_SIZE = 512 * 512


@app.post("/")
async def augment_basic(file: UploadFile = File(...)):
    message = "Augmentation done!"
    out_response = None
    read_status  = 1
    time_elapsed = 0

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
            start_time = time()
            augmented_image = augment_image_basic(image)    
            time_elapsed = time() - start_time           
            _, img_bytes = cv2.imencode(".png", augmented_image)
            out_response = StreamingResponse(io.BytesIO(img_bytes.tobytes()), headers={"time_elapsed":str(time_elapsed)}, media_type="image/png")
        except Exception:
            message = Exception #"Invalid file type!"   
    
    return out_response if out_response is not None else message

@app.post("/augment_default")
async def augment_default(file: UploadFile = File(...)):
    message = "Augmentation done!"
    out_response = None
    read_status  = 1
    time_elapsed = 0

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
            start_time = time()
            augmented_image = augment_image_default(image)
            time_elapsed = time() - start_time     
            _, img_bytes = cv2.imencode(".png", augmented_image)
            out_response = StreamingResponse(io.BytesIO(img_bytes.tobytes()), headers={"time_elapsed":str(time_elapsed)}, media_type="image/png")
        except Exception:
            message = Exception #"Invalid file type!"   
        
    return out_response if out_response is not None else message


def augment_image_basic(image):

    ink_phase   = [InkBleed(p=1)]
    paper_phase = [DirtyRollers(p=1)]
    post_phase  = [WaterMark(p=1)]
    pipeline    = AugraphyPipeline(ink_phase, paper_phase, post_phase)
    
    data_output = pipeline.augment(image)
    augmented_image = data_output["output"]

    return augmented_image


def augment_image_default(image):
    
    data_output = default_augment(image)
    augmented_image = data_output["output"]

    return augmented_image

