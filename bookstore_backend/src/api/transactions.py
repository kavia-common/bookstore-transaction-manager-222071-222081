from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.security import get_current_user
from src.models.models import Transaction, User
from src.schemas.transactions import (
    TransactionCreate,
    TransactionList,
    TransactionOut,
    TransactionSummary,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get(
    "",
    response_model=TransactionList,
    summary="List transactions",
    description="List transactions for the current user with pagination.",
)
def list_transactions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Max number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionList:
    """List transactions for the current authenticated user."""
    q = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    total = q.count()
    items = q.order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
    return TransactionList(items=items, total=total)


@router.get(
    "/summary",
    response_model=TransactionSummary,
    summary="Transactions summary",
    description="Get count and total amount for current user's transactions.",
)
def transactions_summary(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> TransactionSummary:
    """Return summary stats for current user's transactions."""
    count = db.query(func.count(Transaction.id)).filter(Transaction.user_id == current_user.id).scalar() or 0
    total_amount = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.user_id == current_user.id)
        .scalar()
        or Decimal("0")
    )
    return TransactionSummary(count=int(count), total_amount=Decimal(total_amount))


@router.post(
    "",
    response_model=TransactionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create transaction",
    description="Create a new transaction for the current user.",
)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    """Create a transaction owned by current user."""
    tx = Transaction(user_id=current_user.id, book_title=payload.book_title, amount=payload.amount, notes=payload.notes)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.put(
    "/{transaction_id}",
    response_model=TransactionOut,
    summary="Update transaction",
    description="Update a transaction by id, only if it belongs to the current user.",
)
def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionOut:
    """Update an existing transaction owned by current user."""
    tx = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    if payload.book_title is not None:
        tx.book_title = payload.book_title
    if payload.amount is not None:
        tx.amount = payload.amount
    if payload.notes is not None:
        tx.notes = payload.notes

    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete transaction",
    description="Delete a transaction by id, only if it belongs to the current user.",
)
def delete_transaction(
    transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> None:
    """Delete an existing transaction owned by current user."""
    tx = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    db.delete(tx)
    db.commit()
    return None
