import sys
import requests


def check(name, ok, detail=''):
    status = 'PASS' if ok else 'FAIL'
    print(f'[{status}] {name}  {detail}')
    return ok


def main(base):
    base = base.rstrip('/')
    results = []

    r = requests.get(f'{base}/health', timeout=60)
    results.append(check('GET /health', r.status_code == 200, r.text[:80]))

    payload = {
        'Gender': 'F', 'Age': 45,
        'scheduled_day': '2026-04-25T08:00:00Z',
        'appointment_day': '2026-05-02T10:00:00Z',
        'Scholarship': 0, 'hypertension': 1, 'Diabetes': 0,
        'Alcoholism': 0, 'handicap': 0, 'sms_received': 1,
    }
    r = requests.post(f'{base}/predict', json=payload, timeout=60)
    body = r.json() if r.ok else {}
    results.append(check(
        'POST /predict',
        r.status_code == 200 and body.get('risk_level') in ('LOW', 'MEDIUM', 'HIGH'),
        f'risk={body.get("risk_level")} prob={body.get("probability")}'
    ))

    r = requests.get(f'{base}/stats', timeout=60)
    body = r.json() if r.ok else {}
    results.append(check(
        'GET /stats',
        r.status_code == 200 and 'total_predictions' in body,
        f'total={body.get("total_predictions")}'
    ))

    sys.exit(0 if all(results) else 1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python smoke_test.py <base_url>')
        sys.exit(2)
    main(sys.argv[1])
