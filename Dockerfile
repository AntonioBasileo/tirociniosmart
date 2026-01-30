# Dockerfile
FROM python:3.9-slim

# Env: niente .pyc, log immediati
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir
WORKDIR /tirociniosmart

COPY requirements.txt ./

# Utente non-root
RUN addgroup --system tirociniosmart && adduser --system --ingroup tirociniosmart tirociniosmart-user

COPY app ./app
COPY manage.py ./manage.py
COPY templates ./templates
COPY tirociniosmart ./tirociniosmart
COPY entrypoint.sh ./entrypoint.sh
COPY requirements.txt ./requirements.txt

# Dipendenze Python (prima del codice per sfruttare cache Docker)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Permessi
RUN chown -R tirociniosmart-user:tirociniosmart . && \
    chmod +x entrypoint.sh

USER tirociniosmart-user

# Avvio server
ENTRYPOINT ["./entrypoint.sh"]