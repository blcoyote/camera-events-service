

BFF for Frigate NVR

local running:

preferrably in a virtual environment

```bash

python -m pip install -r requirements.txt

python -m uvicorn main:app --reload --env-file .env


```

Requires google firebase serviceAccountKey.json contents base64'd into UVICORN_FIREBASE_CREDENTIALS env variable for firebase notification and authentication.

json.loads(base64.b64decode(os.getenv("UVICORN_FIREBASE_CREDENTIALS")))

it's also possible to authenticate to a local database/sqlite on the unversioned endpoints. (really, use v2)
