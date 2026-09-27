import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from db_models import Hotspot
from services.firms_fetch import fetch_hotspots
from services.enrichment import enrich_hotspots
from services.classifier import classify_hotspots
from services.alert_service import send_telegram_alert, send_summary_alert

router = APIRouter()


@router.get("/hotspots")
def get_hotspots(db: Session = Depends(get_db)):
    try:
        hotspots = db.query(Hotspot).all()
        result = []
        for h in hotspots:
            result.append({
                "id": h.id,
                "latitude": h.latitude,
                "longitude": h.longitude,
                "frp": h.frp,
                "brightness": h.brightness,
                "confidence": h.confidence,
                "satellite": h.satellite,
                "fire_type": h.fire_type,
                "confidence_score": h.confidence_score,
                "is_chronic": h.is_chronic,
                "industrial_nearby": None,
                "acq_date": h.acq_date,
                "acq_time": h.acq_time
            })
        return {"total": len(result), "hotspots": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/hotspots/clear")
def clear_hotspots(db: Session = Depends(get_db)):
    try:
        db.query(Hotspot).delete()
        db.commit()
        return {"message": "All hotspots cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hotspots/fetch")
def fetch_and_classify(days: int = 1, db: Session = Depends(get_db)):
    try:
        df = fetch_hotspots(days=days)
        if df.empty:
            return {"message": "No hotspots found"}

        df = enrich_hotspots(df)
        df = classify_hotspots(df)

        saved = 0
        industrial_count = 0
        gas_flare_count = 0
        wildfire_count = 0
        agricultural_count = 0

        for _, row in df.iterrows():
            hotspot = Hotspot(
                latitude=row.get('latitude'),
                longitude=row.get('longitude'),
                frp=row.get('frp'),
                brightness=row.get('brightness'),
                confidence=str(row.get('confidence', '')),
                satellite=str(row.get('satellite', '')),
                instrument=str(row.get('instrument', '')),
                acq_date=str(row.get('acq_date', '')),
                acq_time=str(row.get('acq_time', '')),
                fire_type=row.get('fire_type'),
                confidence_score=row.get('confidence_score'),
                is_chronic=row.get('is_chronic', 'no'),
            )
            db.add(hotspot)
            saved += 1

            fire_type = row.get('fire_type', '')
            frp = row.get('frp', 0) or 0
            confidence = row.get('confidence_score', 0) or 0

            if fire_type == 'Industrial Fire':
                industrial_count += 1
                if frp > 30:
                    send_telegram_alert(
                        fire_type=fire_type,
                        lat=row['latitude'],
                        lon=row['longitude'],
                        frp=frp,
                        confidence=round(confidence * 100),
                        date=str(row.get('acq_date', ''))
                    )

            elif fire_type == 'Gas Flare':
                gas_flare_count += 1
                send_telegram_alert(
                    fire_type=fire_type,
                    lat=row['latitude'],
                    lon=row['longitude'],
                    frp=frp,
                    confidence=round(confidence * 100),
                    date=str(row.get('acq_date', ''))
                )

            elif fire_type == 'Wildfire':
                wildfire_count += 1

            elif fire_type == 'Agricultural Burning':
                agricultural_count += 1

        db.commit()

        acq_date = str(df['acq_date'].iloc[0]) if len(df) > 0 else ''
        send_summary_alert(
            total=saved,
            industrial=industrial_count,
            wildfire=wildfire_count,
            agricultural=agricultural_count,
            gas_flare=gas_flare_count,
            date=acq_date
        )

        return {"message": f"{saved} hotspots classified and saved"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hotspots/filter")
def filter_hotspots(
    fire_type: str = None,
    is_chronic: str = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Hotspot)
        if fire_type:
            query = query.filter(Hotspot.fire_type == fire_type)
        if is_chronic:
            query = query.filter(Hotspot.is_chronic == is_chronic)
        hotspots = query.all()
        result = []
        for h in hotspots:
            result.append({
                "id": h.id,
                "latitude": h.latitude,
                "longitude": h.longitude,
                "fire_type": h.fire_type,
                "confidence_score": h.confidence_score,
                "is_chronic": h.is_chronic,
                "acq_date": h.acq_date
            })
        return {"total": len(result), "hotspots": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))