from fastapi import APIRouter, Depends, Query , HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Article
from ..models import Article as ArticleModel
from typing import List,Optional
  

router = APIRouter()

@router.get("/home", response_model=List[Article])
async def read_articles(db: Session = Depends(get_db)):
    return db.query(ArticleModel).all()

@router.get("/filter", response_model=List[Article])
async def filter_articles(
    name: Optional[str] = Query(None, description="Filter articles by name"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    db: Session = Depends(get_db)
):
    query = db.query(ArticleModel)
    print(name, min_price, max_price)
    if name:
        query = query.filter(ArticleModel.name.ilike(f"%{name}%"))
    
    if min_price is not None:
        query = query.filter(ArticleModel.price >= min_price)
    
    if max_price is not None:
        query = query.filter(ArticleModel.price <= max_price)
    
    return query.all()

@router.get("/{article_id}", response_model=Article)
async def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/", response_model=Article)
async def create_article(article: Article,db: Session = Depends(get_db)):
    db_article = ArticleModel(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.put("/{article_id}",response_model=Article)
async def update_article(article_id: int, article: Article, db: Session = Depends(get_db)):
    db_article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(db_article)
    db.commit()
    return {"message": "Article deleted successfully"}

