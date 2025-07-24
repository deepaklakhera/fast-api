from fastapi import FastAPI
from .database import engine
from .models import Base

from .routes import home,articles

Base.metadata.create_all(bind=engine)
        
app = FastAPI()

app.include_router(home.router)
app.include_router(articles.router,prefix='/api/articles',tags=['articles'])
