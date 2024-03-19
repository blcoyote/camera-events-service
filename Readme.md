

BFF for Frigate NVR

local running:

preferrably in a virtual environment

```bash

python -m pip install -r requirements.txt

python -m uvicorn main:app --reload --env-file .env


```

Requires serviceAccountKey.json for firebase notification and authentication.
it's also possible to authenticate to a local database/sqlite.