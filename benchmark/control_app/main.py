from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/ok")
async def ok():
    return {"message": "ok"}


@app.get("/error")
async def error():
    raise HTTPException(status_code=500, detail="Something went wrong")
