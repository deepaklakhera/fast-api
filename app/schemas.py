from pydantic import BaseModel, Field

class Article(BaseModel):
    name: str = Field(...,min_length=3)
    price: float = Field(None,ge = 1)
    
    class Config:
        from_attributes = True    