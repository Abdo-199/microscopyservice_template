from fastapi import APIRouter, FastAPI, File, Form, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.models.response_models import ResponseModel
from PIL import Image

app = FastAPI()
router = APIRouter()

@router.get("/", summary="Get Service Description")
async def get_service_description():
    """
    Provides a brief description of the service.
    """
    return {"description": "This microservice provides a textual description of uploaded images with an optional prompt."}

@router.get("/response-format/", summary="Get Run Action Response Format")
async def get_response_format():
    """
    Describes the type of response returned by the run_action endpoint.
    """
    response_description = {
        "content_type": "application/json",
        "description": "The response is a JSON object containing a textual description of the image and additional information based on the provided prompt."
    }
    return JSONResponse(content=response_description)

@router.post("/run/", 
             summary="Process an uploaded image with a prompt",
             response_model=ResponseModel)
async def run_action(
    prompt: str = Form(...), 
    image: UploadFile = File(...) 
):
    """
    Provide a textual description of the uploaded image, incorporating information from a provided prompt.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File type not supported")

    try:
        with Image.open(image.file) as image:
            # Extract basic information from the image
            width, height = image.size
            image_format = image.format

            # Generate a description of the image
            description = f"The image is {width}x{height} pixels and is in {image_format} format."

            return {"answer": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

