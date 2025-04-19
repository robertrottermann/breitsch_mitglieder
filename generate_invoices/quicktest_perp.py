import segno
import os

def generate_personal_qr_bill(
    filename,
    debtor_name="",
    debtor_street="",
    debtor_house_no="",
    debtor_postal="",
    debtor_town=""
):
    payload_lines = [
        # 01: Header - Identification of QR Code Type
        "SPC",  # Identification (Swiss Payments Code)

        # 02: Header - Version
        "0200",  # Version (02.00)

        # 03: Header - Coding Type
        "1",     # 1 = UTF-8 text encoding

        # 04: CdtrAcct.IBAN
        "CH8230024016605294508",  # QR-IBAN of creditor (must be valid for QRR references)

        # 05: Cdtr.AdrTp (S or K)
        "S",  # S = structured address, K = combined

        # 06–11: Creditor (Cdtr) Address
        "Quartierzentrum Breitsch-Träff",  # 06: Cdtr.Nm - Creditor name
        "Breitenrainplatz",                # 07: Cdtr.StrtNm - Street name
        "27",                              # 08: Cdtr.BldgNb - House number
        "3013",                            # 09: Cdtr.PstCd - Postal code
        "Bern",                            # 10: Cdtr.TwnNm - City
        "CH",                              # 11: Cdtr.Ctry - Country code (ISO)

        # 12–17: Ultimate Creditor (UltmtCdtr) - Optional
        "",  # 12: UltmtCdtr.Nm - Name (leave empty if unused)
        "",  # 13: UltmtCdtr.StrtNm
        "",  # 14: UltmtCdtr.BldgNb
        "",  # 15: UltmtCdtr.PstCd
        "",  # 16: UltmtCdtr.TwnNm
        "",  # 17: CcyAmtDate.Amt - Amount (blank = user decides)

        # 18–22: Payment Information  
        "",      # 18: Amount to be paid (blank if open amount)
        "",      # 19: Ccy - Currency (CHF) ????
        "CHF",   # 19: Curency - Currency (CHF)
        "S",     # 20: UltDbtr.AddressType S Debtor address type: S = structured, K = combined
        debtor_name, # 21: UltDbtr.Name Name of the debtor
 
        # 22–26: Debtor (Dbtr) Address
        debtor_street,     # 22: Dbtr.StrtNm - Street
        debtor_house_no,   # 23: Dbtr.BldgNb - House number
        debtor_postal,     # 24: Dbtr.PstCd - Postal code
        debtor_town,       # 25: UltmtDbtr.Ctry 
        "CH",              # 26: Dbtr.Ctry - Country code

        # 27: RmtInf.Tp - Reference type (QRR = structured with check digit)
        "QRR",

        # 28: Reference - Reference number (must match IBAN type)
        "210000000003139471430009017",

        # 29: UnstructuredMessage
        "Rechnung 2025-123",

        # 30: Trailer - End of Data Indicator
        "EPD",

        # 31:  BillInformation  Additional information for biller (optional, max 140 chars)
        # "Mitgliederbeitrag 2024"  # 31: BillInformation
    ]

    # assert len(payload_lines) == 30, f"Expected 31 lines, got {len(payload_lines)}"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    payload = "\n".join(payload_lines)
    qr = segno.make(payload.encode('utf-8'), error='M')
    qr.save(filename, scale=4)
    print(f"✅ Saved personalized QR bill to {filename}")


# 👇 Example usage
if __name__ == "__main__":
    generate_personal_qr_bill(
        filename="output/qr_bill_robert_r.png",
        debtor_name="Robert Rottermann",
        debtor_street="Optingenstrasse",
        debtor_house_no="12",
        debtor_postal="3013",
        debtor_town="Bern"
    )
