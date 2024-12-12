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
    
    response = client.post(
        "/run/",
        data={"prompt": "Describe this image"},
        files={"image": ("test_image.jpg", image_data, "image/jpeg")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "answer" in json_response
    # add your own tests here
    # assert json_response["answer"] == "The image is 100x100 pixels and is in JPEG format."

def test_run_action_unsupported_file_type():
    response = client.post(
        "/run/",
        files={"image": ("test_image.txt", b"fake text data", "text/plain")},
        data={"prompt": "Describe this text"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "File type not supported"

def test_run_action_missing_prompt():
    # Create a test image
    image_data = create_test_image()
    
    response = client.post(
        "/run/",
        files={"image": ("test_image.jpg", image_data, "image/jpeg")}
    )
    
    assert response.status_code == 422
    assert "value_error.missing" in str(response.json())

def test_run_action_processing_failure():
    # Simulate a corrupted image file
    broken_image_data = b"not really an image"
    
    response = client.post(
        "/run/",
        files={"image": ("broken_image.jpg", broken_image_data, "image/jpeg")},
        data={"prompt": "Describe this broken image"}
    )
    
    assert response.status_code == 500
    assert "An error occurred" in response.json()["detail"]