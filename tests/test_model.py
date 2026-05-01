# tests/test_model.py
from unittest.mock import patch
from noshow_iq import model


@patch('noshow_iq.model.load')
def test_predict_high_risk(mock_load):
    # Mock the RandomForest model so it doesn't need the real .pkl file
    class MockModel:
        def predict_proba(self, X):
            # Force the mock model to predict an 85% chance of a no-show
            return [[0.15, 0.85]]

    mock_load.return_value = (
        MockModel(),
        ['Age', 'days_in_advance', 'appointment_dow']
    )
    # Pass dummy record to the predict function
    record = {'Age': 30, 'days_in_advance': 5, 'appointment_dow': 2}
    result = model.predict(record)
    # Assert that the logic correctly categorizes 85% as HIGH risk
    assert result['risk_level'] == 'HIGH'
    assert result['probability'] == 0.85
    assert 'double-booking' in result['recommendation']


@patch('noshow_iq.model.load')
def test_predict_low_risk(mock_load):
    class MockModel:
        def predict_proba(self, X):
            # Force the mock model to predict a 10% chance of a no-show
            return [[0.90, 0.10]]

    mock_load.return_value = (
        MockModel(),
        ['Age', 'days_in_advance', 'appointment_dow']
    )
    record = {'Age': 55, 'days_in_advance': 2, 'appointment_dow': 1}
    result = model.predict(record)
    # Assert that the logic correctly categorizes 10% as LOW risk
    assert result['risk_level'] == 'LOW'
    assert result['probability'] == 0.10
    assert result['recommendation'] == 'No action needed.'
