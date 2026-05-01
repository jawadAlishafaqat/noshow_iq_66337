import os
from datetime import datetime, timezone
from pymongo import MongoClient

_client = None


def _get_db():
    global _client
    if _client is None:
        uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
        _client = MongoClient(
            uri,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
    return _client['noshow_iq']


def log_prediction(raw_input: dict, cleaned: dict, result: dict):
    db = _get_db()
    doc = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "raw_input": raw_input,
        "cleaned_features": cleaned,
        "risk_level": result["risk_level"],
        "probability": result["probability"],
        "recommendation": result["recommendation"]
    }
    db.predictions.insert_one(doc)


def last_n_predictions(n: int):
    db = _get_db()
    cursor = db.predictions.find({}, {"_id": 0}).sort("timestamp", -1).limit(n)
    return list(cursor)


def aggregate_stats():
    db = _get_db()
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_predictions": {"$sum": 1},
                "high_risk_count": {
                    "$sum": {"$cond": [{"$eq": ["$risk_level", "HIGH"]}, 1, 0]}
                },
                "low_risk_count": {
                    "$sum": {"$cond": [{"$eq": ["$risk_level", "LOW"]}, 1, 0]}
                },
                "average_probability": {"$avg": "$probability"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "total_predictions": 1,
                "high_risk_count": 1,
                "low_risk_count": 1,
                "average_probability": {"$round": ["$average_probability", 2]}
            }
        }
    ]

    res = list(db.predictions.aggregate(pipeline))
    if not res:
        return {
            "total_predictions": 0,
            "high_risk_count": 0,
            "low_risk_count": 0,
            "average_probability": 0.0
        }

    stats = res[0]
    last_run = db.training_runs.find_one(sort=[("timestamp", -1)])

    if last_run:
        stats["last_trained"] = last_run["timestamp"]
    else:
        stats["last_trained"] = "No training runs found"

    return stats
