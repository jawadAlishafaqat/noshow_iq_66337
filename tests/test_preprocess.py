import pandas as pd
from noshow_iq.preprocess import clean, engineer, RENAME_MAP


def make_sample():
    return pd.DataFrame({
        'no_show': ['No', 'Yes', 'No'],
        'Age': [-1, 25, 45],
        'scheduled_day': ['2026-01-01T08:00:00Z'] * 3,
        'appointment_day': ['2026-01-10T10:00:00Z'] * 3,
        'Gender': ['F', 'M', 'F'],
        'Scholarship': [0, 1, 0],
        'hypertension': [0, 0, 1],
        'Diabetes': [0, 0, 0],
        'Alcoholism': [0, 0, 0],
        'handicap': [0, 0, 0],
        'sms_received': [1, 0, 1],
    })


def test_clean_removes_negative_age():
    df = make_sample()
    cleaned = clean(df)
    assert (cleaned['Age'] >= 0).all()


def test_clean_encodes_no_show():
    df = make_sample()
    cleaned = clean(df)
    assert set(cleaned['no_show'].unique()).issubset({0, 1})


def test_engineer_days_in_advance():
    df = make_sample()
    cleaned = clean(df)
    engineered = engineer(cleaned)
    assert 'days_in_advance' in engineered.columns
    assert (engineered['days_in_advance'] >= 0).all()


def test_rename_map_fixes_misspellings():
    assert 'Hipertension' in RENAME_MAP
    assert 'Handcap' in RENAME_MAP
    assert RENAME_MAP['Hipertension'] == 'hypertension'
    assert RENAME_MAP['Handcap'] == 'handicap'