from pydantic import BaseModel

class DocumentCreate(BaseModel):
    user_id: str
    title: str
    content: str