import io
import qrcode


def generate_vcard_qr(person_data):
    """Generate vCard QR code for contact information"""
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{person_data['name']}
ORG:{person_data['title']}
EMAIL:{person_data['personal_data']['email']}
TEL:{person_data['personal_data']['phone_number'].replace("-","")}
ADR:;;{person_data['personal_data']['current_location']};;;;
URL:https://resumepatrick.streamlit.app
END:VCARD"""

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(vcard)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')

    return buf.getvalue()
