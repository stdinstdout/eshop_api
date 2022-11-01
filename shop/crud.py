from fastapi import HTTPException

from sqlalchemy.orm import Session

from datetime import datetime
from typing import List

from . import models, schemas

# item is a shop item
# goods is a plural form of shopitem

# GET

def get_item_by_id(db: Session, shopitem_id: int):
    return db.query(models.ShopItem).get(shopitem_id)


def get_goods_in_categories(db: Session, category_id: int):
    inst: models.Category = db.query(models.Category).get(category_id)
    if inst:
        return inst.items
    else:
        return None


def get_all_categories(db: Session):
    return db.query(models.Category).all()


# CREATE

def create_good(db: Session, item: schemas.CreateShopItem):

    item = models.ShopItem(**item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item



def create_goods(db: Session, goods: List[schemas.CreateShopItem]):

    cats = set((x[0] for x in db.query(models.Category.id).all()))
    added_goods = []

    for item in goods:
        if item.category_id in cats:
            added_goods.append(
                models.ShopItem(
                    **item.dict(),
                    added_time=datetime.now(),
                    updated_time=datetime.now()
                    )
                )
        else:
            raise HTTPException(status_code=402, detail=str(cats))

    db.add_all(added_goods)
    db.commit()
    list(map(db.refresh, added_goods))

    return added_goods

    
 

def create_category(db: Session, category: str):
    
    cat = models.Category(name=category)

    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def create_categories(db: Session,  categories: List[str]):
    
    added_cats = []

    for category in categories:
        cat = models.Category(name=category)
        added_cats.append(cat)

    db.add_all(added_cats)
    db.commit()
    list(map(db.refresh, added_cats))

    return added_cats