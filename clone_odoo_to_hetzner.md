
# 🚀 Clone Odoo SaaS Instance to Hetzner with Docker Compose

This guide helps you clone your Odoo SaaS instance (e.g., `https://breitschtraeff.odoo.com/odoo/`) to a Hetzner server using Docker Compose.

---

## ✅ Prerequisites

- SSH access to Hetzner server
- Docker & Docker Compose installed
- Odoo backup file (from Odoo.com → Settings → Database → Backups)

---

## 🛠 Step 1: Install Docker & Docker Compose

```bash
ssh root@95.216.142.221

apt update
apt install -y ca-certificates curl gnupg lsb-release

install -m 0755 -d //etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

---

## 📂 Step 2: Prepare Project Directory

```bash
mkdir -p /opt/odoo
cd /opt/odoo
```

---

## 🧾 Step 3: Create `docker-compose.yaml`

```yaml
version: '3.1'

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
    image: odoo:16
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
      - ./config:/etc/odoo

volumes:
  odoo-db-data:
  odoo-web-data:
```

---

## 🔐 Step 4: Get Backup from Odoo.com

- Log in to [https://breitschtraeff.odoo.com](https://breitschtraeff.odoo.com)
- Go to Settings → Database → Manage Backups
- Download `.zip` file

---

## 📦 Step 5: Extract the Backup

```bash
apt install unzip
unzip your_backup.zip -d backup
```

Result:
- `dump.sql`
- `filestore/` folder

---

## 💾 Step 6: Import the Database

```bash
docker compose up -d db
cat backup/dump.sql | docker exec -i $(docker ps -qf "name=odoo_db") psql -U odoo -d odoo
```

---

## 📁 Step 7: Copy the Filestore

```bash
mkdir -p ./filestore
cp -r backup/filestore/* ./filestore/
```

Create `config/odoo.conf` with:

```ini
[options]
data_dir = /var/lib/odoo/.local/share/Odoo
addons_path = /mnt/extra-addons
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
```

Make sure it's mounted in `docker-compose.yaml`:

```yaml
- ./config:/etc/odoo
```

---

## 🚀 Step 8: Launch Odoo

```bash
docker compose up -d
```

Then open:

```
http://95.216.142.221:8069
```

---

## 🌐 Optional: Add HTTPS & Domain

Use Nginx + Certbot or Traefik for HTTPS support (let me know if you want help).
