FROM python:3.14-slim
RUN pip install --no-cache-dir --root-user-action=ignore --disable-pip-version-check psycopg2-binary
WORKDIR /app
COPY . .
# idle so you can open a terminal in it: docker compose exec python bash
CMD ["sleep", "infinity"]
