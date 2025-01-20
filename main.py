from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime
import math

# Configure FastAPI with metadata for Swagger UI
app = FastAPI(
    title="Receipt Processor",
    description="""
    A service that processes receipts and awards points based on specific rules.
    
    ## Available Endpoints
    * POST /receipts/process - Process a new receipt
    * GET /receipts/{id}/points - Get points for a processed receipt
    """,
    version="1.0.0",
    docs_url="/"  # This makes Swagger UI appear at the root URL
)

# In-memory storage
receipts_db = {}

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str

class ReceiptResponse(BaseModel):
    id: str

class PointsResponse(BaseModel):
    points: int

def calculate_points(receipt: Receipt) -> int:
    points = 0
    
    # Rule 1: One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt.retailer)
    
    # Rule 2: 50 points if the total is a round dollar amount
    if float(receipt.total).is_integer():
        points += 50
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    if float(receipt.total) % 0.25 == 0:
        points += 25
    
    # Rule 4: 5 points for every two items
    points += (len(receipt.items) // 2) * 5
    
    # Rule 5: If description length is multiple of 3, multiply price by 0.2
    for item in receipt.items:
        description = item.shortDescription.strip()
        if len(description) % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)
    
    # Rule 7: 6 points if purchase date is odd
    purchase_date = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
    if purchase_date.day % 2 == 1:
        points += 6
    
    # Rule 8: 10 points if purchase time is between 2:00pm and 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, '%H:%M')
    if 14 <= purchase_time.hour < 16:
        points += 10
        
    return points

@app.post("/receipts/process")
async def process_receipt(receipt: Receipt) -> ReceiptResponse:
    receipt_id = str(uuid.uuid4())
    receipts_db[receipt_id] = receipt
    return ReceiptResponse(id=receipt_id)

@app.get("/receipts/{id}/points")
async def get_points(id: str) -> PointsResponse:
    receipt = receipts_db.get(id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    points = calculate_points(receipt)
    return PointsResponse(points=points)
