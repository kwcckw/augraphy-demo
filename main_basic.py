from fastapi import File, UploadFile,FastAPI, Request, Response
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str


@app.post("/get")
async def root(data: Item):
    return {"message": f"You wrote: '{data.text}'"}


@app.get("/a")
async def root2():
    return {"message": "Hello World"}

@app.get("/get4")
async def get_name(name:str):
    return {"name": name}
    
@app.post("/get2")
async def get_number2(data: Item):
    return {"message": f"You wrote: '{data.num}'"}
    
    
@app.post("/get3")
async def get_name2(name2:str):
    return {"name": name2}

