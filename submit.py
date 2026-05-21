import json
import hmac
import hashlib
import os
import requests
from datetime import datetime, timezone

URL = "https://b12.io/apply/submission"

SECRET = os.environ["B12_SIGNING_SECRET"]

repository = os.environ["GITHUB_REPOSITORY"]
run_id = os.environ["GITHUB_RUN_ID"]

payload = {
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    "name": "Dema Shehadeh",
    "email": "dema.shehadeh03@gmail.com",
    "resume_link": "https://1drv.ms/b/c/06f894f0b403a8c4/IQDXATzsKxl6QKEZ56y_nsUAAV-sTv25n7Y1eveEXVdATTs?e=Nv0Gd1",
    "repository_link": f"https://github.com/{repository}",
    "action_run_link": f"https://github.com/{repository}/actions/runs/{run_id}"
}

body = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":")
).encode("utf-8")

signature = hmac.new(
    SECRET.encode("utf-8"),
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}"
}

response = requests.post(
    URL,
    data=body,
    headers=headers
)

response.raise_for_status()

receipt = response.json()["receipt"]

print("Receipt:", receipt)
