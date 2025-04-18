<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

## Swiss QR-Bill: List of All 31 Fields in Correct Sequence

Below is the complete, correct sequence of the 31 fields required for a Swiss QR-bill, including the technical name, a sample value, and an explanation for each field. This is based on the official Swiss Implementation Guidelines for the QR-bill[^1][^2].


| \# | Technical Name | Sample Value | Explanation |
| :-- | :-- | :-- | :-- |
| 1 | QRType | SPC | Identification of QR Code type (Swiss Payments Code) |
| 2 | Version | 0200 | Version of the QR-bill standard (fixed: "0200") |
| 3 | Coding | 1 | Coding type (1 = UTF-8 text encoding) |
| 4 | IBAN | CH4431999123000889012 | QR-IBAN or IBAN of the creditor |
| 5 | Cdtr.AddressType | S | Address type: S = structured, K = combined |
| 6 | Cdtr.Name | Muster \& Söhne AG | Name of the creditor (account holder) |
| 7 | Cdtr.Street | Musterstrasse | Street name of creditor |
| 8 | Cdtr.HouseNo | 12 | House number of creditor |
| 9 | Cdtr.PostalCode | 8000 | Postal code of creditor |
| 10 | Cdtr.Town | Zürich | Town/city of creditor |
| 11 | Cdtr.Country | CH | Country code of creditor (ISO 3166-1 alpha-2) |
| 12 | UltCred.Name |  | Ultimate creditor name (optional, usually empty) |
| 13 | UltCred.Street |  | Ultimate creditor street (optional) |
| 14 | UltCred.HouseNo |  | Ultimate creditor house number (optional) |
| 15 | UltCred.PostalCode |  | Ultimate creditor postal code (optional) |
| 16 | UltCred.Town |  | Ultimate creditor town (optional) |
| 17 | UltCred.Country |  | Ultimate creditor country (optional) |
| 18 | Amount | 199.95 | Amount to be paid (blank if open amount) |
| 19 | Currency | CHF | Currency: CHF or EUR |
| 20 | UltDbtr.AddressType | S | Debtor address type: S = structured, K = combined |
| 21 | UltDbtr.Name | Erika Musterfrau | Name of the debtor |
| 22 | UltDbtr.Street | Beispielweg | Street name of debtor |
| 23 | UltDbtr.HouseNo | 5 | House number of debtor |
| 24 | UltDbtr.PostalCode | 4000 | Postal code of debtor |
| 25 | UltDbtr.Town | Basel | Town/city of debtor |
| 26 | UltDbtr.Country | CH | Country code of debtor (ISO 3166-1 alpha-2) |
| 27 | ReferenceType | QRR | Reference type: QRR (QR reference), SCOR, or NON |
| 28 | Reference | 210000000003139471430009017 | Reference number (depends on ReferenceType) |
| 29 | UnstructuredMessage | Rechnung 2025-123 | Unstructured message (optional, max 140 chars) |
| 30 | Trailer | EPD | End of payload data indicator (fixed: "EPD") |
| 31 | BillInformation |  | Additional information for biller (optional, max 140 chars) |

### Field Details \& Explanations

- **QRType (SPC):** Identifies the QR code as a Swiss Payment Code.
- **Version (0200):** Specifies the version of the QR-bill standard; currently only "0200" is valid.
- **Coding (1):** Indicates UTF-8 character encoding.
- **IBAN:** The account number to which the payment will be credited. Must be a valid Swiss QR-IBAN or standard IBAN.
- **AddressType (S/K):** Specifies if the address fields are structured (S) or combined (K).
- **Creditor Address Fields:** Name, street, house number, postal code, town, and country of the creditor.
- **Ultimate Creditor:** Optional fields for the ultimate beneficiary, typically left empty.
- **Amount:** The payment amount; if left blank, the payer can fill it in.
- **Currency:** CHF or EUR only.
- **Debtor Address Fields:** Address type, name, street, house number, postal code, town, and country of the debtor.
- **ReferenceType:** QRR for QR reference, SCOR for creditor reference, NON for none.
- **Reference:** The actual reference number, format depends on ReferenceType.
- **UnstructuredMessage:** Free text (optional), e.g., invoice number or purpose.
- **Trailer (EPD):** Marks the end of the QR-bill data.
- **BillInformation:** Additional information for the biller, not printed on the payment part (optional).

All fields must be present in this exact order, even if some are left empty (except for certain trailing optional fields, which may be omitted if not used)[^1][^2].

> For the most authoritative and detailed technical descriptions, refer to the official [Swiss QR-bill Implementation Guidelines, Table 7][^1][^2].

<div style="text-align: center">⁂</div>

[^1]: https://www.six-group.com/dam/download/banking-services/standardization/qr-bill/ig-qr-bill-v2.2-en.pdf

[^2]: https://www.six-group.com/dam/download/banking-services/standardization/qr-bill/ig-qr-bill-v2.3-en.pdf

[^3]: https://www.moneyland.ch/en/qr-bill-payment-slips-switzerland

[^4]: https://advendio.atlassian.net/wiki/spaces/SO/pages/1857290241/6.3.11+Generating+Swiss+QR+Bills

[^5]: https://www.onlinedruck.ch/download/bcm-e802ab1e157ab324c4fde25427a864814b753d7b

[^6]: https://www.six-group.com/dam/download/banking-services/standardization/qr-bill/style-guide-qr-bill-en.pdf

[^7]: https://mirrors.mit.edu/CTAN/macros/latex/contrib/qrbill/qrbill.pdf

[^8]: https://github.com/sprain/php-swiss-qr-bill

