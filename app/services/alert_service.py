from sqlalchemy.orm import Session
from app.models.alert import Alert  # Il modello creato in precedenza

def check_and_trigger_alerts(db: Session, current_price: float):
    """
    Scansiona gli alert attivi e li fa scattare se il prezzo corrente
    soddisfa la condizione (sopra o sotto la soglia).
    """
    # 1. Gestione alert "BELOW": scattano se il prezzo corrente è MINORE o UGUALE alla soglia
    db.query(Alert).filter(
        Alert.status == "ACTIVE",
        Alert.direction == "BELOW",
        Alert.target_price >= current_price
    ).update({"status": "TRIGGERED"}, synchronize_session=False)

    # 2. Gestione alert "ABOVE": scattano se il prezzo corrente è MAGGIORE o UGUALE alla soglia
    db.query(Alert).filter(
        Alert.status == "ACTIVE",
        Alert.direction == "ABOVE",
        Alert.target_price <= current_price
    ).update({"status": "TRIGGERED"}, synchronize_session=False)

    # Salva definitivamente i cambi di stato sul database
    db.commit()