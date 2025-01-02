from fastapi.testclient import TestClient
from app.main import app
from PIL import Image
import io

client = TestClient(app)

def test_description():
    response = client.get("/")
    assert response.status_code == 200
    assert "description" in response.json()

def create_test_image() -> bytes:
    # Create an in-memory image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def test_run_action_success():
    # Prepare the image data
    image_data = create_test_image()
    
    # Send a valid request to the /run/ endpoint
    response = client.post(
        "/run/",
        files={"image": ("test_image.jpg", image_data, "image/jpeg")},
        data={"noise_level": 25}
    )
    
    # Assert that the response is successful
    assert response.status_code == 200
    
    # Validate response content
    json_response = response.json()
    assert "clarity" in json_response
    assert "output_path" in json_response
    
    # Additional validation
    assert json_response["clarity"] in ["good", "bad"]
    assert json_response["output_path"].endswith("_out.png")

def test_run_action_unsupported_file_type():
    response = client.post(
        "/run/",
        files={"image": ("test_image.txt", b"fake text data", "text/plain")},
        data={"noise_level": 25}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PNG and JPEG images are supported."

def test_run_action_missing_prompt():
    # Create a test image
    image_data = create_test_image()
    
    response = client.post(
        "/run/",
        files={"image": ("test_image.jpg", image_data, "image/jpeg")},
        data={"noise_level":70}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid noise level. Please provide a valid noise level: 25 or 50."

def test_run_action_processing_failure():
    # Simulate a corrupted image file
    broken_image_data = b"not really an image"
    
    response = client.post(
        "/run/",
        files={"image": ("broken_image.jpg", broken_image_data, "image/jpeg")},
        data={"noise_level": 25}
    )
    
    assert response.status_code == 500
    assert "An error occurred" in response.json()["detail"]