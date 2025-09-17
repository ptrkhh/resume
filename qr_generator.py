import io
import qrcode
import streamlit as st


def generate_vcard_qr():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(vcard_content())
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')

    return buf.getvalue()


def vcard_content():
    return f"""BEGIN:VCARD
        VERSION:3.0
        FN:{st.session_state.patrick['name']}
        ORG:{st.session_state.patrick['title']}
        EMAIL:{st.session_state.patrick['personal_data']['email']}
        TEL:{st.session_state.patrick['personal_data']['phone_number'].replace("-", "")}
        ADR:;;{st.session_state.patrick['personal_data']['current_location']};;;;
        URL:https://resumepatrick.streamlit.app
        END:VCARD"""
