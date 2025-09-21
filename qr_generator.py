import io

import qrcode
import yaml


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

    return f"""BEGIN:VCARD
VERSION:3.0
N:Hermawan;Patrick;;;
FN:{data['name']}
GENDER:M
EMAIL:{data['personal_data']['email']}
TEL:{data['personal_data']['phone_number'].replace("-", "")}
ADR;TYPE=home:;;;Jakarta;Jakarta;;Indonesia
GEO:-6.21462;106.84513
ORG:{data['title']}
ROLE:{data['title']}
TITLE:{data['title']}
NOTE:{data['summary']}
URL:https://resumepatrick.streamlit.app
END:VCARD"""
