# noshow_iq/preprocess.py
import pandas as pd
import numpy as np

RENAME_MAP = {
    'No-show': 'no_show',
    'Hipertension': 'hypertension',
    'Handcap': 'handicap',
    'SMS_received': 'sms_received',
    'ScheduledDay': 'scheduled_day',
    'AppointmentDay': 'appointment_day',
}

def load_raw(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df.rename(columns=RENAME_MAP)

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['scheduled_day'] = pd.to_datetime(df['scheduled_day'], utc=True)
    df['appointment_day'] = pd.to_datetime(df['appointment_day'], utc=True)
    df = df[df['Age'] >= 0]
    df = df[df['Age'] <= 110]
    df['no_show'] = (df['no_show'] == 'Yes').astype(int)
    return df

def engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['days_in_advance'] = (
        df['appointment_day'].dt.normalize()
        - df['scheduled_day'].dt.normalize()
    ).dt.days
    df.loc[df['days_in_advance'] < 0, 'days_in_advance'] = 0
    df['appointment_dow'] = df['appointment_day'].dt.dayofweek
    df['age_group'] = pd.cut(
        df['Age'], bins=[-1, 12, 18, 35, 60, 120],
        labels=['child', 'teen', 'young_adult', 'adult', 'senior']
    )
    return df

def prepare(df: pd.DataFrame):
    df = clean(df)
    df = engineer(df)
    df = pd.get_dummies(df, columns=['Gender', 'age_group'], drop_first=True)
    drop_cols = ('no_show', 'PatientId', 'AppointmentID',
                 'scheduled_day', 'appointment_day', 'Neighbourhood')
    feature_cols = [c for c in df.columns if c not in drop_cols]
    return df[feature_cols], df['no_show']

def prepare_single(record: dict) -> dict:
    df = pd.DataFrame([record])
    if 'no_show' not in df.columns:
        df['no_show'] = 0
    df = clean(df)
    df = engineer(df)
    df = pd.get_dummies(df, columns=['Gender', 'age_group'], drop_first=True)
    return df.iloc[0].to_dict()