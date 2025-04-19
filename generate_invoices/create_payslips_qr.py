import os
import csv
import argparse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# --- Configuration ---
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
TEMPLATE_FILE = 'payslip_template_with_qr.html'
CSV_FILE = 'addresses.csv'
DEBUG_MAX = 5  # Limit number of generated payslips for testing

# --- Creditor Data (used in template) ---
CREDITOR_INFO = {
    "name": "Quartierzentrum Breitsch-Träff",
    "street": "Breitenrainplatz",
    "houseNo": "27",
    "postalCode": "3014",
    "town": "Bern",
    "countryCode": "CH",
    "iban": "CH8230024016605294508",
    "reference": "210000000003139471430009017"
}

# --- Ensure output folder exists ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Setup Jinja2 templating ---
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template(TEMPLATE_FILE)

# --- Read members CSV ---
def read_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# --- Generate individual PDF pages with QR code ---
def generate_individual_pdfs(data):
    for i, person in enumerate(data, start=1):
        if i > DEBUG_MAX:
            print(f"✅ Reached debug limit ({DEBUG_MAX}).")
            break

        qr_filename = f"qr_{i}.png"
        qr_path = os.path.join(OUTPUT_DIR, qr_filename)

        if not os.path.exists(qr_path):
            print(f"⚠️ Missing QR code file: {qr_path}. Skipping {person['name']}.")
            continue

        html = template.render(
            recipients=[person],
            qr_index=i,
            output_dir=OUTPUT_DIR,
            creditor=CREDITOR_INFO
        )

        sanitized_name = person['name'].replace(" ", "_")
        pdf_filename = f"payslip_{i}_{sanitized_name}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
        HTML(string=html).write_pdf(pdf_path)
        print(f"✅ Created {pdf_filename}")

# --- Entry point ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['individual'], default='individual')
    args = parser.parse_args()

    data = read_csv(CSV_FILE)
    if args.mode == 'individual':
        generate_individual_pdfs(data)
    else:
        print("Only individual mode is supported.")
