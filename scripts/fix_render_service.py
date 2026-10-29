import urllib.request
import json

api_key = 'rnd_HgZ3znAgnVDaHU6UST24AB4NIGub'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

service_id = 'srv-dbhihc2fngtc73bom86g'
dollar = chr(36) # '$'
start_cmd = f"python -m uvicorn app.main:app --host 0.0.0.0 --port {dollar}PORT --app-dir backend"

payload = {
    "serviceDetails": {
        "envSpecificDetails": {
            "startCommand": start_cmd
        }
    }
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(f'https://api.render.com/v1/services/{service_id}', data=data, headers=headers, method='PATCH')
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("startCommand set to:", res.get('serviceDetails', {}).get('envSpecificDetails', {}).get('startCommand'))

# Also set environment variables on service
env_vars = [
    {"key": "PYTHON_VERSION", "value": "3.11.9"},
    {"key": "STT_PROVIDER", "value": "fallback"},
    {"key": "DEBUG", "value": "false"}
]

req_env = urllib.request.Request(
    f'https://api.render.com/v1/services/{service_id}/env-vars',
    data=json.dumps(env_vars).encode('utf-8'),
    headers=headers,
    method='PUT'
)
try:
    with urllib.request.urlopen(req_env) as resp:
        print("Env vars configured successfully!")
except Exception as e:
    print("Env vars update:", e)
