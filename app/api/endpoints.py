from fastapi import APIRouter, FastAPI, File, Form, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from app.models.response_models import ResponseModel
from PIL import Image, ImageFilter
import io
import base64

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

def process_image(image: Image.Image) -> Image.Image:
    """Apply some processing (e.g., a filter) to the image."""
    # Example: Applying a Gaussian Blur filter
    return image.filter(ImageFilter.GaussianBlur(5))

@router.post("/run/", 
             summary="Process an uploaded image with a prompt")
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
            # Process the image (for example, applying a filter)
            processed_img = process_image(image)

            # Convert the processed image to a byte array
            img_byte_array = io.BytesIO()
            processed_img.save(img_byte_array, format="PNG")
            img_byte_array.seek(0)

            # Encode the processed image to base64
            img_base64 = base64.b64encode(img_byte_array.getvalue()).decode("utf-8")
            img_tag = f'<img src="data:image/png;base64,{img_base64}" />'

            # Generate a description (based on the original image or prompt)
            description = f"Processed image with applied filter: {prompt}"

            # Return the processed image and description in HTML format
            return HTMLResponse(content=f"<html><body>{img_tag}<br>{description}</body></html>")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

