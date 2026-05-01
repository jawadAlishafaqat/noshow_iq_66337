from fastapi.testclient import TestClient
from unittest.mock import patch
from noshow_iq.api import app

client = TestClient(app=app)


def test_health_returns_200():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


@patch('noshow_iq.api.db.log_prediction')
@patch('noshow_iq.api.prepare_single')
@patch('noshow_iq.api.model.predict')
def test_predict_returns_risk_level(mock_predict, mock_prepare, mock_log):
    mock_prepare.return_value = {
        'Age': 45, 'days_in_advance': 7,
        'appointment_dow': 4, 'sms_received': 0,
        'Scholarship': 0, 'hypertension': 0,
        'Diabetes': 0, 'Alcoholism': 0, 'handicap': 0,
    }
    mock_predict.return_value = {
        'risk_level': 'HIGH',
        'probability': 0.75,
        'recommendation': 'Test rec'
    }
    payload = {
        'Gender': 'F', 'Age': 45,
        'scheduled_day': '2026-04-25T08:00:00Z',
        'appointment_day': '2026-05-02T10:00:00Z'
    }
    r = client.post('/predict', json=payload)
    assert r.status_code == 200
    assert r.json()['risk_level'] in ['LOW', 'MEDIUM', 'HIGH']


def test_invalid_age_returns_422():
    payload = {
        'Gender': 'F', 'Age': -5,
        'scheduled_day': '2026-04-25T08:00:00Z',
        'appointment_day': '2026-05-02T10:00:00Z'
    }
    r = client.post('/predict', json=payload)
    assert r.status_code == 422
