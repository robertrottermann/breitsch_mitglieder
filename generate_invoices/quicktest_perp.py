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
        "CH8230024016605294508",  # QR-IBAN (must be valid for QRR references)

        # 05: Cdtr.AdrTp (S or K)
        "S",  # S = structured address, K = combined

        # 06–11: Creditor (Cdtr) Address
        "Quartierzentrum Breitsch-Träff",  # 06: Cdtr.Nm - Creditor name
        "Breitenrainplatz",                # 07: Cdtr.StrtNm - Street name
        "27",                              # 08: Cdtr.BldgNb - House number
        "3013",                            # 09: Cdtr.PstCd - Postal code
        "Bern",                            # 10: Cdtr.TwnNm - City
        "CH",                              # 11: Cdtr.Ctry - Country code (ISO)

        # 12–16: Ultimate Creditor (UltmtCdtr) - Optional
        "",  # 12: UltmtCdtr.Nm - Name (leave empty if unused)
        "",  # 13: UltmtCdtr.StrtNm
        "",  # 14: UltmtCdtr.BldgNb
        "",  # 15: UltmtCdtr.PstCd
        "",  # 16: UltmtCdtr.TwnNm

        # 17–22: Payment Information
        "",      # 17: CcyAmtDate.Amt - Amount (blank = user decides)
        "",      # 18: UltmtCdtr.Ctry
        "",      # 19: UltmtDbtr.Nm - Name of initiating party (not used)
        "CHF",   # 20: CcyAmtDate.Ccy
        "S",     # 21: UltmtDbtr.AdrTp
        debtor_name,      # 22: UltmtDbtr.Name

        # 23–28: Debtor (Dbtr) Address
        debtor_name,       # 23: Dbtr.Nm - Debtor name
        debtor_street,     # 24: Dbtr.StrtNm - Street
        debtor_house_no,   # 25: Dbtr.BldgNb - House number
        debtor_postal,     # 26: Dbtr.PstCd - Postal code
        # debtor_town,       # 27: UltmtDbtr.Ctry 
        "CH",              # 28: Dbtr.Ctry - Country code

        # 29: RmtInf.Tp - Reference type (QRR = structured with check digit)
        "QRR",

        # 30: RmtInf.Ref - Reference number (must match IBAN type)
        "210000000003139471430009017",
        "", 
        # 31: Trailer - End of Data Indicator
        "EPD"
    ]

    assert len(payload_lines) == 31, f"Expected 31 lines, got {len(payload_lines)}"

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
