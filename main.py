from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import logging

app = FastAPI()

# Set up logging to monitor webhook activity
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


# Define models for the nested structure
class Category(BaseModel):
    id: int
    url: str
    name: str
    description: Optional[str]
    date_modified: str
    img: str
    parent: Optional[str]


class Brand(BaseModel):
    id: int
    url: str
    name: str
    description: Optional[str]
    date_modified: str
    img: str


class Variant(BaseModel):
    id: int
    v1: Optional[str]
    v2: Optional[str]
    v3: Optional[str]
    quantity: int
    sku: str
    barcode: str
    price: str
    weight: str
    images: List[str]
    p1: Optional[str]
    p2: Optional[str]
    p3: Optional[str]
    delivery_price: Optional[str]


class ProductUpdatePayload(BaseModel):
    id: int
    url: str
    name: str
    description: str
    tracking: str
    shipping: str
    digital: str
    new: str
    active: str
    date_added: str
    date_modified: str
    category: Category
    brand: Brand
    tags: List[str]
    variants: List[Variant]
    images: List[str]
    publicFiles: List[str]


@app.get("/")
async def root():
    """
    Simple health check endpoint to confirm the app is running.
    """
    return {"message": "FastAPI webhook service is running!"}


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Endpoint to receive webhook data from CloudCart.
    """
    try:
        # Parse the incoming JSON payload
        payload = await request.json()
        logging.info(f"Payload received: {payload}")

        # Validate and parse the payload using the Pydantic model
        product = ProductUpdatePayload(**payload)

        # Process the product data (e.g., log or save it to the database)
        logging.info(f"Product update received for: {product.name} (ID: {product.id})")

        # Respond with a success message
        return {"status": "success", "message": "Webhook received", "product": product.dict()}
    except ValidationError as e:
        # Handle validation errors from Pydantic
        logging.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")
    except Exception as e:
        # Handle other errors
        logging.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
