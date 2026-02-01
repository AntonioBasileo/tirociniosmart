# TirocinioSmart

TirocinioSmart è una piattaforma web per la gestione digitale dei tirocini universitari, pensata per semplificare e automatizzare i processi tra studenti, aziende e amministrazione universitaria.

## Funzionalità principali
- **Gestione utenti**: autenticazione JWT, ruoli/gruppi, permessi granulari (admin, azienda, studente, staff).
- **Registrazione tirocini**: creazione, modifica, conferma e gestione delle richieste di tirocinio.
- **Gestione aziende**: CRUD aziende, assegnazione permessi, visualizzazione e ricerca.
- **API REST**: tutte le operazioni sono esposte tramite API RESTful, con protezione tramite middleware JWT.
- **Sicurezza**: gestione sicura delle credenziali, secret JWT, password hashing, controllo permessi e gruppi.
- **Docker**: ambiente di sviluppo e produzione containerizzato (Dockerfile, docker-compose).
- **Database**: MySQL, con migrazioni Django e gestione automatica dei dati.

## Architettura
- **Backend**: Django 4.x, Django REST Framework, MySQL.
- **Struttura moduli**:
  - `app/` contiene i modelli, le view REST, i DTO, le API gateway e i test.
  - `security/` gestisce autenticazione, middleware JWT, utility, permessi/gruppi custom.
  - `templates/` per eventuali pagine HTML (admin, documentazione, ecc).
  - `docker-compose.yml`, `Dockerfile`, `entrypoint.sh` per la gestione container.
  - `secrets/` per le chiavi JWT e password DB (non versionare in produzione!).

## Come avviare l'applicazione
1. **Configurazione ambiente**
   - Installa Docker Desktop.
   - Crea i file di secret in `secrets/` (`jwt_secret_key.txt`, `mysql_password.txt`).
2. **Build e avvio**
   ```bash
   ./run.sh
   ```
3. **Accesso API**
   - Le API sono esposte su `http://localhost:8001/tirocinio-smart/`
   - Esempi endpoint:
     - Autenticazione: `/auth/login`, `/auth/register-user`, `/auth/register-admin-user`
     - Aziende: `/api/company/all`, `/api/company/<pk>`
     - Tirocini: `/api/training-register/`, `/api/training-register/<pk>`

## Sicurezza e permessi
- JWT usato per autenticazione stateless.
- Middleware custom per validazione token e assegnazione utente.
- Permessi e gruppi gestiti tramite Django e custom logic (assegnazione automatica all'atto della registrazione).

## Sviluppo e test
- Tutte le logiche sono testabili tramite API REST (vedi `app/tests.py`).
- Per testare endpoint protetti, autenticarsi e passare il token JWT nell'header `Authorization: Bearer <token>`.
- Per aggiungere nuovi modelli, view o permessi, seguire la struttura modulare e le best practice Django.

## Note importanti
- Non versionare i file in `secrets/` su repository pubblici.
- In produzione, impostare variabili d'ambiente sicure e usare chiavi JWT robuste.
- Per personalizzare i permessi/gruppi, modificare le view in `security/view/auth_view.py` e i DTO in `app/dto/trainingDTOs.py`.

## Autori
- Progetto sviluppato da Antonio Basileo.

---

Per domande, bug o richieste di supporto, apri una issue su GitHub o contatta l'autore.
