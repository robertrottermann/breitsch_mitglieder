
# 🔁 Sync Odoo 18 Enterprise Docker Stack Between Machines

This guide helps you **copy your complete Odoo 18 Enterprise stack** from your desktop to another device (e.g., laptop), including database and attachments, using Docker volumes.

---

## 🧱 What’s Included

- Odoo database (`odoo-db-data`)
- Odoo filestore (`odoo-web-data`)
- Configuration, addons, enterprise modules
- Docker Compose setup

---

## 💻 On Desktop: Create Volume Backups

From inside your project folder (e.g., `~/mitglieder`):

```bash
docker run --rm -v mitglieder_odoo-db-data:/volume -v $(pwd):/backup alpine tar czf /backup/db_volume.tar.gz -C /volume .
docker run --rm -v mitglieder_odoo-web-data:/volume -v $(pwd):/backup alpine tar czf /backup/web_volume.tar.gz -C /volume .
```

📁 This creates:

- `db_volume.tar.gz`
- `web_volume.tar.gz`

These contain all your data and can be copied to your laptop.

---

## 🚚 Transfer Files to Laptop

Use `scp`, USB stick, or any sync method. For example:

```bash
scp db_volume.tar.gz web_volume.tar.gz user@laptop-ip:~
```

---

## 💻 On Laptop: Restore Volumes

Place the backups in your new project folder, e.g., `~/mitglieder`.

```bash
mkdir -p ~/mitglieder/backup
mv db_volume.tar.gz web_volume.tar.gz ~/mitglieder/backup
cd ~/mitglieder/backup
```

Now recreate and restore the volumes:

```bash
docker volume create mitglieder_odoo-db-data
docker volume create mitglieder_odoo-web-data

docker run --rm -v mitglieder_odoo-db-data:/volume -v $(pwd):/backup alpine tar xzf /backup/db_volume.tar.gz -C /volume
docker run --rm -v mitglieder_odoo-web-data:/volume -v $(pwd):/backup alpine tar xzf /backup/web_volume.tar.gz -C /volume
```

---

## ▶️ Launch the Stack

```bash
cd ~/mitglieder
docker compose up -d
```

Then open:

```
http://localhost:8069
```

You’ll see the same data and configuration as on your desktop.

---

## 🧼 Optional: Avoid Auto-Prefixed Volume Names

To use simpler names like `odoo-db-data`, add this to the top of your `docker-compose.yaml`:

```yaml
name: mitglieder
```

This disables the automatic prefixing of volume names by the project folder name.

---

## ✅ You're Done!

You now have a fully working Odoo stack on your laptop, identical to your desktop setup.

Let me know if you'd like to automate this with a sync script or use bind mounts instead of volumes.
