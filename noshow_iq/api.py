# noshow_iq/api.py
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from . import model, db
from .preprocess import prepare_single
from .schema import Appointment

app = FastAPI(title='NoShowIQ', version='1.0')


@app.get('/health')
def health():
    return {'status': 'ok', 'time': datetime.now(timezone.utc).isoformat()}


@app.post('/predict')
def predict(appt: Appointment):
    try:
        raw = appt.model_dump()
        features = prepare_single(raw)
        result = model.predict(features)
    except Exception as e:
        raise HTTPException(500, str(e))
    db.log_prediction(raw_input=raw, cleaned=features, result=result)
    return result


@app.get('/history')
def history():
    return db.last_n_predictions(20)


@app.get('/stats')
def stats():
    return db.aggregate_stats()
