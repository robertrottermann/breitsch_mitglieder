
# 🐘 Run Odoo 18 Enterprise Locally with Docker Compose

This guide walks you through running a local clone of your Odoo 18 Enterprise backup using Docker Compose.

---

## 🛠️ Prerequisites

- Linux system (Ubuntu recommended)
- Docker & Docker Compose installed
- A valid Odoo Enterprise GitHub account (to clone the enterprise repo)
- Your backup `.zip` file downloaded from https://www.odoo.com/fr_FR/my/databases

---

## 👤 Step 1: Create a New Local User (Optional)

Create a dedicated user (optional but recommended for production-like separation):

```bash
sudo adduser breitsch
sudo usermod -aG docker breitsch
su - breitsch
```

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
cat backup/dump.sql | docker exec -i $(docker ps -qf "name=mitglieder_db") psql -U odoo -d odoo
```

Copy the filestore:

```bash
mkdir -p ./filestore
cp -r backup/filestore/* ./filestore/
```

---

## 🚀 Step 8: Launch Odoo

Start the full stack:

```bash
docker compose up -d
```

Then open in your browser:

```
http://localhost:8069
```

---

## 🧪 Notes for Local Testing

- All data is local, safe to test freely.
- Use `docker compose down` to stop everything.
- Use `docker compose logs -f` to watch logs.
- If port 8069 is busy, change it in `docker-compose.yaml`.

---

Let me know if you'd like to add:
- PgAdmin or Adminer
- Mailhog
- Auto backup jobs
