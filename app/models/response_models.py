from pydantic import BaseModel

class ResponseModel(BaseModel):
    answer: str