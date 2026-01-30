#!/bin/bash
set -e

# 2. Spegnimento di eventuali container precedenti e pulizia volumi (opzionale)
# Nota: il flag -v cancella i dati del DB, rimuovilo se vuoi mantenere i dati tra i riavvii
echo "--- 🛑 Spegnimento container esistenti ---"
docker compose down

# Crea la cartella per il bind mount del volume MySQL (serve se non esiste ancora)
echo "--- 📁 Creazione cartella per il bind mount sql"
mkdir -p var/lib/mysql

# 3. Avvio dell'infrastruttura con Docker Compose
echo "--- 🐳 Avvio container con Docker Compose ---"
docker compose up --build

echo "--- ✅ Applicazione avviata con successo! ---"
echo "API disponibili su: http://localhost:8001/tirociniosmart"