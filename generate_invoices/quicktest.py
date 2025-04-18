# bill = QRBill(
#     account="CH82 3002 4016 6052 9450 8",  # Creditor's IBAN
#     creditor={
#         "name": "Quartierzentrum Breitsch-Träff",
#         "street": "Breitenrainplatz 27",
#         "pcode": "3014",
#         "city": "Bern",
#         "country": "CH"
#     },
#     debtor={
#         "name": "Uherkovich Henrik P.1a",
#         "street": "Monbijoustrasse 20",
#         "pcode": "3011",
#         "city": "Bern",
#         "country": "CH"
#     },
#     amount="150.50",
#     currency="CHF",
#     reference="21 00000 00003 13947 14300 09017",
#     additional_info="Invoice 2024-045 - Web Development Services"
# )
import segno
import os

# payload_lines = [
#     # ... (header remains same)
#     "CH8230024016605294508",          # IBAN without spaces
#     "K",                              # Address type: Combined elements
    
#     # --- Creditor Section ---        # Lines 6-11
#     "Quartierzentrum Breitsch-Träff",
#     "Breitenrainplatz 27",            # Combined street + number
#     "",                               # Leave empty for 'K' type
#     "",                               # Leave empty for 'K' type
#     "",                               # Leave empty for 'K' type
#     "CH",
    
#     # --- Ultimate Creditor ---       # Lines 12-16 (all empty)
#     "", "", "", "", "",
    
#     # --- Debtor Section ---          # Lines 17-22
#     "Uherkovich Henrik P.1a",
#     "Monbijoustrasse 20",             # Combined street + number
#     "",                               # Leave empty for 'K' type
#     "",                               # Leave empty for 'K' type
#     "",                               # Leave empty for 'K' type
#     "CH",
    
#     # --- Payment Details ---         # Lines 23-28
#     "199.95",
#     "CHF",                            # Must be CHF/EUR
#     "21000000000313947143000901",     # Reference without spaces
#     "Abonnement für 2020",
#     "",                               # Trailer
#     "EPD"
# ]


def generate_valid_qr_bill(filename):
    payload_lines = [
        "SPC",                          # 01: QR type
        "0200",                         # 02: Version
        "1",                            # 03: Coding: UTF-8
        "CH8230024016605294508",        # 04: QR-IBAN (NO SPACES!)
        "K",                            # 05: Address type (structured)
        # --- Creditor Section ---
        "Quartierzentrum Breitsch-Träff",  # 06: Name
        "Breitenrainplatz 27",          # 07: Street + number (COMBINED)
        "",                             # 08: House number (EMPTY for structured)
        "3014",                         # 09: ZIP
        "Bern",                         # 10: City
        "CH",                           # 11: Country
        # --- Ultimate Creditor (empty) ---
        "", "", "", "", "",
        # --- Debtor Section ---
        "Uherkovich Henrik P.1a",       # 17: Name
        "Monbijoustrasse 20",           # 18: Street + number (COMBINED)
        "",                             # 19: House number (EMPTY)
        "3011",                         # 20: ZIP
        "Bern",                         # 21: City
        "CH",                           # 22: Country
        # --- Payment Details ---
        "199.95",                       # 23: Amount
        "CHF",                          # 24: Currency
        "21000000000313947143000901",   # 25: Reference (NO SPACES!)
        "Abonnement für 2020",          # 26: Unstructured message
        "",                             # 27: Trailer
        "", "", "",                      # 28-30: Alternative procedures
        "EPD"                           # 31: End marker
    ]

    # Validate structure
    assert len(payload_lines) == 31, f"Expected 31 lines, got {len(payload_lines)}"
    
    # Create output directory
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Generate QR code
    payload = "\n".join(payload_lines)
    qr = segno.make(payload, error='M')
    qr.save(filename, scale=4)
    print(f"✅ QR code saved to {filename}")

generate_valid_qr_bill("output/qr_bill_correct.png")
