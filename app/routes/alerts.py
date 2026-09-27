from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from db_models import Hotspot

router = APIRouter()


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    """Return high priority alerts — Industrial Fire + Gas Flare only"""
    try:
        alerts = db.query(Hotspot).filter(
            Hotspot.fire_type.in_([
                'Industrial Fire',
                'Gas Flare'
            ])
        ).all()

        result = []
        for h in alerts:
            result.append({
                "id": h.id,
                "latitude": h.latitude,
                "longitude": h.longitude,
                "fire_type": h.fire_type,
                "confidence_score": h.confidence_score,
                "is_chronic": h.is_chronic,
                "frp": h.frp,
                "satellite": h.satellite,
                "acq_date": h.acq_date,
                "acq_time": h.acq_time,
                "priority": "HIGH" if h.frp and h.frp > 50 else "MEDIUM"
            })

        # Sort by FRP — highest intensity first
        result.sort(key=lambda x: x['frp'] or 0, reverse=True)

        return {"total": len(result), "alerts": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/chronic")
def get_chronic_alerts(db: Session = Depends(get_db)):
    """Return only chronic fire sources like Jharia"""
    try:
        chronic = db.query(Hotspot).filter(
            Hotspot.is_chronic == 'yes'
        ).all()

        result = []
        for h in chronic:
            result.append({
                "id": h.id,
                "latitude": h.latitude,
                "longitude": h.longitude,
                "fire_type": h.fire_type,
                "confidence_score": h.confidence_score,
                "frp": h.frp,
                "acq_date": h.acq_date
            })

        return {"total": len(result), "chronic_sources": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/summary")
def get_summary(db: Session = Depends(get_db)):
    """Dashboard summary — count by fire type"""
    try:
        total = db.query(Hotspot).count()
        industrial = db.query(Hotspot).filter(
            Hotspot.fire_type == 'Industrial Fire'
        ).count()
        wildfire = db.query(Hotspot).filter(
            Hotspot.fire_type == 'Wildfire'
        ).count()
        agricultural = db.query(Hotspot).filter(
            Hotspot.fire_type == 'Agricultural Burning'
        ).count()
        gas_flare = db.query(Hotspot).filter(
            Hotspot.fire_type == 'Gas Flare'
        ).count()
        chronic = db.query(Hotspot).filter(
            Hotspot.is_chronic == 'yes'
        ).count()

        return {
            "total_hotspots": total,
            "industrial_fire": industrial,
            "wildfire": wildfire,
            "agricultural_burning": agricultural,
            "gas_flare": gas_flare,
            "chronic_sources": chronic
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))