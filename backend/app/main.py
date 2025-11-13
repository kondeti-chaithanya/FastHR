from fastapi import FastAPI

app = FastAPI(title="FastHR")

@app.get("/")
def root():
    return {"message": "FastHR Backend Running"}
