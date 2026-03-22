from fastapi import FastAPI, HTTPException, Depends
from model import Product
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
import db_model
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

db_model.Base.metadata.create_all(bind=engine)

products = [
    Product(id=1, name="IPhone", description="Buy iphone", price=10000, quantity=3),
    Product(id=2, name="Samsung", description="Buy samsung", price=12000, quantity=5)
]

def db_init():
    db = session()
    count = db.query(db_model.Product).count()  # ✅ FIXED
    if count == 0:
        for product in products:
            db.add(db_model.Product(**product.model_dump()))
    db.commit()
    db.close()

db_init()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet():
    return "This is home page"

# ✅ FIX: match frontend
@app.get("/products/")
def all_product(db: Session = Depends(get_db)):
    return db.query(db_model.Product).all()

@app.get("/products/{id}")
def product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products/")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(db_model.Product(**product.model_dump()))
    db.commit()
    return {"message": "Product added successfully"}

@app.put("/products/{id}")
def update_product(id: int, new_product: Product, db: Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if db_product:
        db_product.name = new_product.name
        db_product.description = new_product.description
        db_product.price = new_product.price
        db_product.quantity = new_product.quantity
        db.commit()
        return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="No product found")

@app.delete("/products/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="No product found")