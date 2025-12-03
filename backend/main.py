from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Simple Product API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

products = [
    Product(id=1, name="Shoes", price=120.0, description="Running shoes"),
    Product(id=2, name="T-shirt", price=25.0, description="Cotton shirt"),
]

@app.get("/products", response_model=List[Product])
def get_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for p in products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products", response_model=Product)
def create_product(product: Product):
    for p in products:
        if p.id == product.id:
            raise HTTPException(status_code=400, detail="ID already exists")
    products.append(product)
    return product

# ✅ Add this new route at the very bottom
@app.get("/")
def home():
    return {
        "message": "FastAPI is running inside Docker 🚀",
        "author": "Jann Kevin Polagne",
        "project": "WEB_API Dockerized"
    }
