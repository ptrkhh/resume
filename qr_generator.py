import base64
import io

import qrcode
import yaml


def vcard_qr_datauri(fill="#0d1013", back="#ffffff", transparent=False):
    """QR of the vCard as a base64 data URI, for embedding directly in HTML.

    With transparent=True the light modules are dropped to alpha 0 so the QR
    reads as `fill`-coloured marks painted straight onto whatever is behind it.
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(vcard_content())
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill, back_color=back).convert("RGBA")
    if transparent:
        img.putdata([
            (r, g, b, 0) if r + g + b > 380 else (r, g, b, 255)
            for r, g, b, _ in img.getdata()
        ])
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def generate_vcard_qr():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(vcard_content())
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')

    return buf.getvalue()


def vcard_content():
    with open('patrick.yaml', 'r') as f:
        data = yaml.safe_load(f)

    first, _, last = data['name'].partition(" ")
    # Escape text values per RFC 2426: backslash, comma, semicolon, newline.
    # Without this, the comma in the summary truncates NOTE in strict readers.
    esc = lambda s: s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")
    company = data['experience'][0]['company']  # current employer -> ORG
    return f"""BEGIN:VCARD
VERSION:3.0
N:{last};{first};;;
FN:{esc(data['name'])}
GENDER:M
EMAIL:{data['personal_data']['email']}
TEL:{data['personal_data']['phone_number'].replace("-", "")}
ADR;TYPE=home:;;;Jakarta;Jakarta;;Indonesia
GEO:-6.21462;106.84513
ORG:{esc(company)}
ROLE:{esc(data['title'])}
TITLE:{esc(data['title'])}
NOTE:{esc(data['summary'])}
URL:https://contactpatrick.streamlit.app
END:VCARD"""
