#!/bin/bash

# Script to reset Odoo user passwords using hashed values
# Run this from the directory where your Odoo Docker project lives (e.g., ~/mitglieder)

# Define the container name
DB_CONTAINER="mitglieder-db-1"

# Define users and their new passwords here
declare -A users
users=(
  ["robert@redo2oo.ch"]="coco2dil"
  ["tom.kloeti@gmx.ch"]="coco2dil"
  ["ursula.z@gmx.ch"]="coco2dil"
)

# Generate hashes and prepare SQL update commands
echo "Generating SQL statements..."
sql_file="update_passwords.sql"
echo "-- SQL script to update Odoo user passwords" > $sql_file

for user in "${!users[@]}"; do
  password="${users[$user]}"
  hash=$(python3 -c "from passlib.context import CryptContext; print(CryptContext(schemes=['pbkdf2_sha512']).hash('$password'))")
  echo "UPDATE res_users SET password = '$hash' WHERE login = '$user';" >> $sql_file
done

echo "\q" >> $sql_file

# Copy and execute inside the Postgres container
echo "Copying SQL file to container and executing..."
docker cp "$sql_file" "$DB_CONTAINER":/tmp/$sql_file
docker exec -i "$DB_CONTAINER" psql -U odoo -d odoo -f /tmp/$sql_file

# Cleanup
echo "Cleaning up..."
rm "$sql_file"
docker exec "$DB_CONTAINER" rm /tmp/$sql_file

echo "✅ Passwords updated."
