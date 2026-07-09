from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.price_service import PriceService

router = APIRouter(prefix="/prices", tags=["Prezzi Brent"])

@router.get("/current")
def get_current_brent_price(db: Session = Depends(get_db)):
    """Endpoint per ottenere il prezzo in tempo reale."""
    try:
        service = PriceService(db)
        brent_value = service.update_and_get_price()
        return {
            "status": "success",
            "data": {
                "id": brent_value.id,
                "price": brent_value.value,
                "timestamp": brent_value.timestamp,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/history")
def get_brent_history(db: Session = Depends(get_db)):
    """Endpoint per consultare lo storico dei prezzi del Brent precedentemente salvati."""
    service = PriceService(db)
    history = service.get_price_history()
    return {
        "status": "success",
        "data": [
            {
                "id": item.id,
                "price": item.value,
                "timestamp": item.timestamp,
            }
            for item in history
        ],
    }