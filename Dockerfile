FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./ /app

LABEL traefik.http.routers.cameraevents.rule="Host(`cameraevents.elcoyote.dk`)"
LABEL traefik.http.routers.cameraevents.tls="true"
LABEL traefik.http.routers.cameraevents.tls.certresolver="lets-encrypt"
LABEL traefik.http.services.cameraevents.loadbalancer.server.port="80"