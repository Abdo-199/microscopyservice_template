import numpy as np
import torch
from PIL import Image, ImageEnhance, ImageFilter, ImageStat

def uint2single(img):
    return np.float32(img / 255.0)

def single2uint(img):
    return np.uint8((img.clip(0, 1) * 255.0).round())

def single2tensor(img):
    return torch.from_numpy(np.ascontiguousarray(img)).permute(2, 0, 1).float().unsqueeze(0)

def tensor2uint(img):
    img = img.data.squeeze().float().clamp_(0, 1).cpu().numpy()
    if img.ndim == 3:
        img = np.transpose(img, (1, 2, 0))
    return np.uint8((img * 255.0).round())

def pil2unit(image: Image.Image):
    img_array = np.array(image.convert('L'), dtype=np.uint8)
    img_array = np.expand_dims(img_array, axis=2)
    return img_array

def is_high_quality(img, resolution_threshold=100000, clarity_threshold=50):

    # Check resolution
    width, height = img.size
    if width * height < resolution_threshold:
        return False

    # Check clarity
    img_gray = img.convert('L')
    sharpness = ImageEnhance.Sharpness(img_gray).enhance(3.0).filter(ImageFilter.FIND_EDGES)
    image_clarity = sharpness.convert('L')
    image_var = ImageStat.Stat(image_clarity).stddev[0]
    if image_var < clarity_threshold:
        return False

    return True
