from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, Depends, FastAPI, HTTPException, Query

from sqlalchemy.orm import Session

from typing import List, Union
from functools import lru_cache

from .database import SessionLocal, engine
from . import config, models
from . import crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app.add_middleware(
#     TrustedHostMiddleware, 
#     allowed_hosts=["*"], 
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache()
def get_settings():
    return config.Settings()  # type: ignore


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.post('/import/goods')
def import_goods(goods: List[schemas.CreateShopItem] = Body(..., embed=True), db: Session = Depends(get_db)):
    return crud.create_goods(db, goods)


@app.post('/import/categories')
def import_categories(categories: List[str]  = Body(..., embed=True), db: Session = Depends(get_db)):
    return crud.create_categories(db, categories)


@app.get('/item/{id}')
def get_item(id: int, db: Session = Depends(get_db)):
    return crud.get_item_by_id(db, id)


@app.get('/items')
def get_items_page(
        categories_id: Union[str, None], 
        items_per_page: int = Query(20, gt=0), 
        page_number: int = Query(1, ge=1), 
        db: Session = Depends(get_db)
        ):
    
    if categories_id and items_per_page:
        return crud.get_items(db, list(map(int, categories_id.split(','))), page_number, items_per_page)
    
    else:
        return crud.get_items(db, None, page_number, items_per_page)


@app.get('/items/category/{category_id}')
def get_items_in_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_goods_in_categories(db, category_id)


@app.get('/items/categories/')
def get_categories(db: Session = Depends(get_db)):
    return crud.get_all_categories(db)

