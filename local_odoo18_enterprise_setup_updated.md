
# 🐘 Run Odoo 18 Enterprise Locally with Docker Compose

This guide walks you through running a local clone of your Odoo 18 Enterprise backup using Docker Compose — now including secure password reset for users.

---

## 🛠️ Prerequisites

- Linux system (Ubuntu recommended)
- Docker & Docker Compose installed
- A valid Odoo Enterprise GitHub account (to clone the enterprise repo)
- Your backup `.zip` file downloaded from https://www.odoo.com/fr_FR/my/databases
- Python with `passlib` installed (for password hashing):
  ```bash
  pip install passlib
  ```

---

## 👤 Step 1: Create a New Local User (Optional)

Create a dedicated user (optional but recommended for production-like separation):

```bash
sudo adduser breitsch
sudo usermod -aG docker breitsch
su - breitsch
```

Password suggestion: `breitsch@99`

---

## 📁 Step 2: Prepare Local Project Structure

```bash
mkdir -p ~/mitglieder
cd ~/mitglieder
```

Place the following folders/files:

- `addons/` (your custom or community addons, can be empty)
- `enterprise/` (see below)
- `config/odoo.conf` (see below)
- `backup/` containing:
  - `dump.sql`
  - `filestore/`

---

## 💼 Step 3: Clone the Odoo Enterprise Repo

```bash
cd ~/mitglieder
git clone https://github.com/odoo/enterprise.git
```

You must have access rights to this private repo.

---

## ⚙️ Step 4: Create `odoo.conf`

Create `~/mitglieder/config/odoo.conf`:

```ini
[options]
data_dir = /var/lib/odoo/.local/share/Odoo
addons_path = /mnt/extra-addons,/mnt/enterprise
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
admin_passwd = admin
logfile = /var/log/odoo/odoo.log
```

---

## 🧱 Step 5: Create `docker-compose.yaml`

Place this in `~/mitglieder/docker-compose.yaml`:

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: odoo
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:18
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
      - ./enterprise:/mnt/enterprise
      - ./config:/etc/odoo

volumes:
  odoo-db-data:
  odoo-web-data:
```

---

## 📦 Step 6: Extract the Backup

Place the downloaded `.zip` in `~/mitglieder` and run:

```bash
unzip your_backup.zip -d backup
```

This gives you:
- `backup/dump.sql`
- `backup/filestore/`

---

## 🧠 Step 7: Load Database & Filestore

Start the database:

```bash
docker compose up -d db
```

Import the SQL dump:

```bash
docker exec -i mitglieder-db-1 psql -U odoo -d odoo < backup/dump.sql
```

Copy the filestore:

```bash
mkdir -p ./filestore
cp -r backup/filestore/* ./filestore/
```

---

## 🔐 Step 8: Reset User Passwords (Securely)

Install `passlib` if not already:

```bash
pip install passlib
```

Generate a hashed password:

```bash
python3 -c "from passlib.context import CryptContext; print(CryptContext(schemes=['pbkdf2_sha512']).hash('robert123'))"
```

Update the user in PostgreSQL:

```bash
docker exec -it mitglieder-db-1 psql -U odoo -d odoo
```

Then in the SQL prompt:

```sql
UPDATE res_users SET password = '<HASH>' WHERE login = 'robert@redo2oo.ch';
\q
```

Replace `<HASH>` with the actual output from the Python script.

✅ You can also use the provided script `reset_multiple_odoo_passwords.sh` to reset multiple users at once.

---

## 🚀 Step 9: Launch Odoo

```bash
docker compose up -d
```

Open in your browser:

```
http://localhost:8069
```

---

## 🧪 Notes for Local Testing

- All data is local, safe to test freely.
- Use `docker compose down` to stop everything.
- Use `docker compose logs -f` to monitor.
- Change port 8069 if needed in `docker-compose.yaml`.

---

Let me know if you want a copy of the reset script or help with HTTPS, email, or backups.
