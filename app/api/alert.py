from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdateStatus
from app.core.database import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# --- 1. CREARE UN ALERT ---
@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    new_alert = Alert(
        user_id=alert_data.user_id,
        target_price=alert_data.target_price,
        direction=alert_data.direction,
        status="ACTIVE"
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

# --- 2. VEDERE GLI ALERT (Tutti quelli di un utente) ---
@router.get("/{user_id}", response_model=List[AlertResponse])
def get_user_alerts(user_id: int, db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.user_id == user_id).all()
    return alerts

# --- 3. ATTIVARE / DISATTIVARE UN ALERT ---
@router.patch("/{alert_id}/status", response_model=AlertResponse)
def update_alert_status(alert_id: int, status_data: AlertUpdateStatus, db: Session = Depends(get_db)):
    # Controlliamo che i valori inseriti siano validi
    if status_data.status not in ["ACTIVE", "INACTIVE"]:
        raise HTTPException(status_code=400, detail="Stato non valido. Usa 'ACTIVE' o 'INACTIVE'.")

    # Cerchiamo l'alert nel database
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert non trovato")

    # Aggiorniamo lo stato
    alert.status = status_data.status
    db.commit()
    db.refresh(alert)
    
    return alert

# --- 4. ELIMINARE UN ALERT ---
@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    # Cerchiamo l'alert nel database
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert non trovato")

    # Lo eliminiamo fisicamente dal database
    db.delete(alert)
    db.commit()
    return # Nessun contenuto da restituire per un 204