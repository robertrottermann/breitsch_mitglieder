
# 🔐 Reset Odoo User Password via SQL

This guide walks you through securely resetting a user's password in a local Odoo 18 Enterprise instance using the PostgreSQL command line and a Python hash generator.

---

## 🎯 Goal

Reset the password for user **`robert@redo2oo.ch`** to:

```
robert123
```

---

## 🧪 Step 1: Generate the Hashed Password (PBKDF2)

Run this Python one-liner in your terminal:

```bash
python3 -c "from passlib.context import CryptContext; print(CryptContext(schemes=['pbkdf2_sha512']).hash('robert123'))"
```

It will output something like:

```
$pbkdf2-sha512$25000$kL8...<long string>
```

Copy the **entire hash**.

---

## 🛠️ Step 2: Connect to the Odoo PostgreSQL Database

Enter the running Postgres container:

```bash
docker exec -it mitglieder-db-1 psql -U odoo -d odoo
```

---

## ✏️ Step 3: Update the Password via SQL

Inside the `psql` prompt, paste and run this (replace the hash with the one from Python):

```sql
UPDATE res_users
SET password = '$pbkdf2-sha512$25000$...'
WHERE login = 'robert@redo2oo.ch';
```

Then quit:

```sql
\q
```

---

## 🚀 Step 4: Log In

Go to:

```
http://localhost:8069
```

Log in with:

- **Username**: `robert@redo2oo.ch`
- **Password**: `robert123`

---

Let me know if you want to reset multiple users or export these steps as a Bash script.
