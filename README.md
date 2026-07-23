# Interactive Resume - Patrick Hermawan

Interactive resume built with Streamlit: AI chatbot (Google Gemini), one-page
PDF resume, printable contact card, and vCard QR code — all generated from a
single `patrick.yaml`.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```
WeasyPrint needs Pango (`packages.txt` covers Streamlit Cloud; locally e.g.
`apt install libpango-1.0-0` or `pkg install pango` on Termux).

2. Set up Google Gemini API key in `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "your_api_key_here"
```

3. Run:
```bash
streamlit run resume.py
```

## Project Structure

- `resume.py` - Streamlit app
- `llm.py` - Gemini chatbot
- `pdf_generator.py` - HTML+CSS → PDF (WeasyPrint) for resume + contact card
- `qr_generator.py` - vCard + QR code
- `patrick.yaml` - all resume data
- `static/` - generated downloads (written at app startup, gitignored)

## Customization

1. Replace `patrick.yaml` content with your own
2. Adjust the prompt in `llm.py` and the CSS in `pdf_generator.py`
