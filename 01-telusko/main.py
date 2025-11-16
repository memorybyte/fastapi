from models import Product
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import session, engine
import database_models

from fastapi.middleware.cors import CORSMiddleware

# Create the tables associated with Base (i.e. h)
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origin=['http://localhost:3000'],
#     allow_methods=['*']
# )

products = [
    Product(id=1, name='Phone', description='Budget phone',
            price=99, quantity=10),
    Product(id=2, name='Laptop', description='Gaming Laptop',
            price=999, quantity=6),
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

    db.commit()


init_db()


@app.get('/')
def home():
    return {'message': 'Hello Wolrd !!!'}


@app.get('/products')
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()

    return db_products


@app.get('/product/{id}')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    # return list(filter(lambda p: p.id == id, products))

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    return db_product


@app.post('/product')
def add_product(product: Product, db: Session = Depends(get_db)):
    # products.append(product)
    # return product

    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put('/product')
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if id == products[i].id:
    #         products[i] = product
    #         return [product]
    # return []

    # Check if product exists
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        return {}

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()

    return {'message': 'updated'}


@app.delete('/product')
def delete_product(id: int, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if id == products[i].id:
    #         del products[i]
    #         return {'id': id}
    # return {}

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        return {'message': 'product not found'}

    db.delete(db_product)
    db.commit()
    return {'message': 'product deleted'}
