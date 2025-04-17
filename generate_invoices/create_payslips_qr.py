import os
import csv
import argparse
import requests
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# --- Configuration ---
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
TEMPLATE_FILE = 'payslip_template.html'
CSV_FILE = 'addresses.csv'
QR_API_URL = "https://www.codecrete.net/qrbill-api/bill/image"
DEBUG_MAX = 5  # <--- HARD LIMIT FOR TESTING

CREDITOR_INFO = {
    "name": "Breitschträff",
    "street": "Optingenstr",
    "houseNo": "12",
    "postalCode": "3013",
    "town": "Bern",
    "countryCode": "CH",
    "iban": "CH4431999123000889012",
    "reference": "210000000003139471430009017",
}

# --- Ensure output directory exists ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Setup Jinja2 environment ---
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template(TEMPLATE_FILE)

# --- Read CSV ---
def read_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# --- Generate QR Bill with Codecrete API ---
def generate_qr_bill(person, index, qr_mode='embedded'):
    for field in ['name', 'Strasse', 'plz', 'ort']:
        if not person.get(field) or person[field].strip() == "":
            print(f"⚠️ Missing or empty field {field} for {person}")

    qr_path = os.path.join(OUTPUT_DIR, f"qr_{index}.png")

    payload = {
        "currency": "CHF",
        "amount": None,  # user-defined by payer
        "account": CREDITOR_INFO["iban"],
        "reference": CREDITOR_INFO["reference"],
        "unstructuredMessage": "Mitgliederbeitrag",
        "creditor": {
            "name": CREDITOR_INFO["name"],
            "street": CREDITOR_INFO["street"],
            "houseNo": CREDITOR_INFO["houseNo"],
            "postalCode": CREDITOR_INFO["postalCode"],
            "town": CREDITOR_INFO["town"],
            "countryCode": CREDITOR_INFO["countryCode"]
        },
        "debtor": {
            "name": person['name'].strip(),
            "street": person['Strasse'].strip(),
            "postalCode": person['plz'].strip(),
            "town": person['ort'].strip(),
            "countryCode": "CH"
        },
        "format": {
            "language": "de",
            "graphicsFormat": "png",
            "outputSize": "qr-bill-only"
        }
    }

    try:
        print("Sending payload:", json.dumps(payload, indent=2, ensure_ascii=False))
        response = requests.post(QR_API_URL, json=payload)
        if response.status_code == 200:
            with open(qr_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"❌ Failed QR for {person['name']}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception for {person['name']}: {e}")
        return False

# --- Generate Individual Payslips ---
def generate_individual_pdfs(data, qr_mode='embedded'):
    for i, person in enumerate(data, start=1):
        if i > DEBUG_MAX:
            print(f"✅ Reached debug max of {DEBUG_MAX} payslips. Stopping.")
            break

        qr_ok = generate_qr_bill(person, i, qr_mode=qr_mode)
        if qr_mode == 'embedded' and not qr_ok:
            continue

        html = template.render(recipients=[person], qr_index=i)
        filename = f"payslip_{i}_{person['name']}.pdf".replace(" ", "_")
        HTML(string=html).write_pdf(os.path.join(OUTPUT_DIR, filename))

# --- Main execution ---
def main(mode='combined', qr_mode='embedded'):
    data = read_csv(CSV_FILE)

    if mode == 'individual':
        generate_individual_pdfs(data, qr_mode=qr_mode)
    else:
        print("Only 'individual' mode currently supported with QR.")

# --- CLI Parser ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['individual', 'combined'], default='individual')
    parser.add_argument('--qr-mode', choices=['embedded', 'separate'], default='embedded')
    args = parser.parse_args()
    main(mode=args.mode, qr_mode=args.qr_mode)
