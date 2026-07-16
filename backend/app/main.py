from fastapi import FastAPI, UploadFile, File

from app.routers.uploads import save_upload
from app.services.parser import extract_pdf

app = FastAPI()


@app.get("/")
def home():
    return {"message": "PlantBrain AI Backend"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = save_upload(file)

    document = extract_pdf(file_path)

    return {
        "filename": file.filename,
        "pages": document["pages"],
        "words": document["words"],
        "text": document["text"][:1000]
    }