from pydantic import BaseModel

class News(BaseModel):
    title: str
    content: str
    category_name: str