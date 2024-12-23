import os
import torch
import numpy as np
from PIL import Image
from .SCUNET import SCUNet
from .utils import uint2single, single2tensor, tensor2uint, pil2unit
from app.core.config import settings


class Denoiser:
    def __init__(self, noise_level: int):
        """
        Initialize the Denoiser with a specific noise level.
        Automatically loads the corresponding SCUNet model.
        """
        self.noise_level = noise_level
        self.device = settings.DEVICE
        self.model = self._load_model()

    def _load_model(self):
        """
        Load the SCUNet model corresponding to the specified noise level.
        """
        model_name = f'scunet_gray_{self.noise_level}'
        model_path = os.path.join(settings.MODEL_ZOO_PATH, f"{model_name}.pth")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        model = SCUNet(in_nc=1, config=[4, 4, 4, 4, 4, 4, 4], dim=64)
        model.load_state_dict(torch.load(model_path, map_location=self.device), strict=True)
        model.to(self.device)
        model.eval()
        return model

    def denoise(self, image: Image.Image) -> Image.Image:
        """
        Denoise the input image using the loaded model.

        :param image: Input image (PIL format).
        :return: Denoised image (PIL format, grayscale).
        """
        # Preprocess image
        img_unit = pil2unit(image)
        img_single = uint2single(img_unit)
        img_tensor = single2tensor(img_single).to(self.device)

        # Perform denoising
        with torch.no_grad():
            denoised_tensor = self._test_onesplit(img_tensor)

        # Postprocess image
        denoised_img = tensor2uint(denoised_tensor)
        denoised_img_pil = Image.fromarray(denoised_img.squeeze(), mode='L')
        return denoised_img_pil

    def _test_onesplit(self, img_tensor, refield=64, min_size=256, sf=1, modulo=1):
        """
        Split the input image tensor for efficient processing and apply the model.
        """
        h, w = img_tensor.size()[-2:]

        top = slice(0, (h // 2 // refield + 1) * refield)
        bottom = slice(h - (h // 2 // refield + 1) * refield, h)
        left = slice(0, (w // 2 // refield + 1) * refield)
        right = slice(w - (w // 2 // refield + 1) * refield, w)

        Ls = [
            img_tensor[..., top, left],
            img_tensor[..., top, right],
            img_tensor[..., bottom, left],
            img_tensor[..., bottom, right],
        ]
        Es = [self.model(L) for L in Ls]

        b, c = Es[0].size()[:2]
        E = torch.zeros(b, c, sf * h, sf * w).type_as(img_tensor)

        E[..., : h // 2 * sf, : w // 2 * sf] = Es[0][..., : h // 2 * sf, : w // 2 * sf]
        E[..., : h // 2 * sf, w // 2 * sf : w * sf] = Es[1][..., : h // 2 * sf, (-w + w // 2) * sf :]
        E[..., h // 2 * sf : h * sf, : w // 2 * sf] = Es[2][..., (-h + h // 2) * sf :, : w // 2 * sf]
        E[..., h // 2 * sf : h * sf, w // 2 * sf : w * sf] = Es[3][..., (-h + h // 2) * sf :, (-w + w // 2) * sf :]
        return E
