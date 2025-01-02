from fastapi import APIRouter, FastAPI, File, Form, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from app.models.response_models import ResponseModel
from PIL import Image, ImageFilter
import io
import base64
import os

from app.models.denoiser import Denoiser
from app.models.utils import is_high_quality

app = FastAPI()
router = APIRouter()

@router.get("/", summary="Get Service Description")
async def get_service_description():
    """
    Provides a brief description of the service.
    """
    return {"description": "This microservice denoises the gray scale SEM images with two available noise levels ('25' for moderate noise, and '50' for images with more extreme noise)."}

@router.get("/response-format/", summary="Get Run Action Response Format")
async def get_response_format():
    """
    Describes the type of response returned by the run_action endpoint.
    """
    response_description = {
        "content_type": "application/json",
        "description": "The response is a JSON object containing a clarity assesment of the resault image and the path of the denoised image."
    }
    return JSONResponse(content=response_description)

def process_image(image: Image.Image) -> Image.Image:
    """Apply some processing (e.g., a filter) to the image."""
    # Example: Applying a Gaussian Blur filter
    return image.filter(ImageFilter.GaussianBlur(5))

@router.post("/run/", 
             summary="Available noise levels: 50, 25")
async def run_action(
    image: UploadFile = File(...), 
    noise_level: int = 50
):
    """
    Endpoint to denoise an uploaded image.
    :param image: The input image (uploaded file).
    :param noise_level: The desired noise level for denoising (integer).
    :return: The denoised image in grayscale.
    """
    if noise_level is None:
        raise HTTPException(status_code=422, detail="value_error.missing")
    # Validate noise level
    if noise_level not in [25, 50]:
        raise HTTPException(status_code=400, detail="Invalid noise level. Please provide a valid noise level: 25 or 50.")
    
    # Validate file type
    if image.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Only PNG and JPEG images are supported.")
    try:

        # Open the uploaded image
        with Image.open(image.file) as img:
            # Create Denoiser instance and denoise image
            denoiser = Denoiser(noise_level=noise_level)
            denoised_img = denoiser.denoise(img)

            is_good_quality = is_high_quality(denoised_img)

            # Save the denoised image
            output_path = os.path.join('outputs', f'{image.filename}_{noise_level}_out.png')
            os.makedirs('outputs', exist_ok=True)
            denoised_img.save(output_path, format='PNG')

            return {
                "clarity": "good" if is_good_quality else "bad",
                "output_path": str(output_path)
            }
    except (IOError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
