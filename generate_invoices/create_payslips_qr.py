import os
import csv
import re
import segno
import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Configuration
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
CSV_FILE = 'addresses.csv'
DEBUG_MAX = 1  # Set to None for all entries
BESR_ID = "210000"  # Replace with your bank-assigned ID

# Creditor Information (Quartierzentrum Breitsch-Träff)
CREDITOR_INFO = {
    "name": "Quartierzentrum Breitsch-Träff",
    "street": "Breitenrainplatz",
    "houseNo": "27",
    "postalCode": "3014",
    "town": "Bern",
    "countryCode": "CH",
    "iban": "CH8230024016605294508"
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_qr_reference(member_id):
    """Generate 27-digit ISO 11649 reference with check digit"""
    base = f"{BESR_ID}{member_id:020d}"
    total = 0
    weights = [1, 2] * (len(base) // 2 + 1)
    for i, digit in enumerate(reversed(base)):
        product = int(digit) * weights[i]
        total += sum(int(d) for d in str(product))
    check = (10 - (total % 10)) % 10
    return f"{base}{check}"

def sanitize_filename(name):
    """Create filesystem-safe filenames"""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)[:50]

def validate_address(row):
    required_fields = ['Strasse', 'plz', 'ort']
    return all(row.get(field) for field in required_fields)

def generate_qr_codes(data):
    """Generate QR codes for valid entries"""
    for i, person in enumerate(data, start=1):
        if DEBUG_MAX and i > DEBUG_MAX: break
        
        reference = generate_qr_reference(i)
        person['reference'] = reference
        person['reference_formatted'] = ' '.join([reference[i:i+5] for i in range(0, 27, 5)])

        payload = [
            "SPC", "0200", "1",
            CREDITOR_INFO["iban"].replace(" ", ""),
            "K",
            CREDITOR_INFO["name"],
            f"{CREDITOR_INFO['street']} {CREDITOR_INFO['houseNo']}",
            "", "", "", "",
            CREDITOR_INFO["countryCode"],
            *[""]*5,
            person.get('name', ''),
            person.get('Strasse', ''),
            "", "", "",
            person.get('countryCode', 'CH'),
            "199.95", "CHF",
            reference,
            f"Mitgliederbeitrag {datetime.datetime.now().year}",
            *[""]*3, "EPD"
        ]
        
        qr_path = os.path.join(OUTPUT_DIR, f"qr_{i}.png")
        if not os.path.exists(qr_path):
            segno.make("\n".join(payload), error='M').save(qr_path, scale=4)

def read_csv():
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        return [row for row in csv.DictReader(f) if validate_address(row)]

def generate_pdfs():
    data = read_csv()
    current_year = datetime.datetime.now().year
    generate_qr_codes(data)

    template = env.get_template('main.html')

    for i, person in enumerate(data, start=1):
        if DEBUG_MAX and i > DEBUG_MAX: break

        context = {
            'member': {
                'name_full': f"{person.get('vorname', '').strip()} {person['name'].strip()}".strip(),
                'address_line': person['Strasse'].strip(),
                'city_line': f"{person['plz']} {person['ort']}",
                'membership_type': person.get('mitgliedart', 'Mitglied'),
                'reference': person['reference_formatted']
            },
            'creditor': CREDITOR_INFO,
            'current_year': current_year,
            'qr_index': i
        }

        try:
            html = template.render(context)
            with open('xx.html', 'w', encoding='utf-8') as f:
                f.write(html)
            pdf_name = f"payslip_{i}_{sanitize_filename(context['member']['name_full'])}.pdf"
            HTML(string=html, base_url=os.path.abspath(OUTPUT_DIR)).write_pdf(
                os.path.join(OUTPUT_DIR, pdf_name)
            )
            print(f"✅ Created {pdf_name}")
        except Exception as e:
            print(f"⚠️ Error generating PDF for row {i}: {str(e)}")

if __name__ == '__main__':
    generate_pdfs()
