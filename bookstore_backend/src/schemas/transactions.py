from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    book_title: str = Field(..., description="Title of the book")
    amount: Decimal = Field(..., description="Transaction amount (positive for purchase, negative for refund)")
    notes: Optional[str] = Field(default=None, description="Optional notes for the transaction")


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    book_title: Optional[str] = Field(default=None, description="Updated book title")
    amount: Optional[Decimal] = Field(default=None, description="Updated amount")
    notes: Optional[str] = Field(default=None, description="Updated notes")


class TransactionOut(TransactionBase):
    id: int = Field(..., description="Transaction identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True


class TransactionList(BaseModel):
    items: List[TransactionOut] = Field(..., description="List of transactions for the current user")
    total: int = Field(..., description="Total number of transactions")


class TransactionSummary(BaseModel):
    count: int = Field(..., description="Number of transactions")
    total_amount: Decimal = Field(..., description="Sum of transaction amounts")
