import os
import torch

class Config:
    AUTHOR = "Abdelrahman Elsharkawi"
    DESCRIPTION = "A FastAPI-based microservice."
    VERSION = "0.1.0"
    NAME = "TinyMicrocopyService: SCUNET denoising"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_ZOO_PATH = os.path.join(BASE_DIR, '../models/model_zoo')
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

settings = Config()
