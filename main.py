from fastapi import File, UploadFile,FastAPI, Request, Response


app = FastAPI()


@app.get("/")
async def root2():
    return {"message": "Hello World"}

@app.get("/get")
async def get_name(name:str):
    return {"name": name}
    
@app.post("/get2")
async def get_number(number:int):
    return {"number": number*2}
    
    
@app.post("/get3")
async def get_name2(name2:str):
    return {"name": name2}