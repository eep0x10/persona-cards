# syntax=docker/dockerfile:1
FROM node:22-bookworm-slim AS frontend
WORKDIR /build/app
COPY app/package.json app/package-lock.json ./
RUN npm ci
COPY app/index.html app/vite.config.js ./
COPY app/src ./src
COPY app/public ./public
COPY deck/illustration_sheets_5_2.json /build/deck/illustration_sheets_5_2.json
RUN npm run build

FROM python:3.12-slim-bookworm AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY app/requirements.lock.txt ./requirements.lock.txt
RUN python -m pip install --disable-pip-version-check -r requirements.lock.txt \
    && groupadd --gid 10001 persona \
    && useradd --uid 10001 --gid persona --no-create-home --shell /usr/sbin/nologin persona
COPY --chown=10001:10001 app/server.py ./server.py
COPY --chown=10001:10001 app/public/deck.json ./public/deck.json
COPY --chown=10001:10001 app/public/inspirations.json ./public/inspirations.json
COPY --from=frontend --chown=10001:10001 /build/app/dist ./dist
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import json, urllib.request; r=json.load(urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)); assert r['status']=='ok'"]
CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--no-proxy-headers"]
