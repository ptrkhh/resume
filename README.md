# Interactive Resume - Patrick Hermawan

A modern, interactive resume built with Streamlit featuring an AI chatbot assistant powered by Google Gemini.

## Features

- **Interactive AI Assistant**: Chat with an AI bot that knows about Patrick's background, experience, and interests
- **Professional Design**: Clean, responsive layout with gradient styling and professional cards
- **Contact Integration**: Direct links to LinkedIn, email, WhatsApp, and Telegram
- **Resume Download**: One-click access to downloadable resume
- **Comprehensive Sections**: Experience, education, projects, and technical skills

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Gemini API key in `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "your_api_key_here"
```

3. Run the application:
```bash
streamlit run resume.py
```

## Tech Stack

- **Frontend**: Streamlit with custom CSS
- **AI**: Google Gemini via LangChain
- **Data**: JSON-based resume content
- **Styling**: Custom CSS with gradient themes

## Project Structure

- `resume.py` - Main Streamlit application
- `llm.py` - AI chatbot integration
- `patrick.json` - Resume data and personal information
- `requirements.txt` - Python dependencies
- `.streamlit/secrets.toml` - API keys (not tracked)

## Customization

To adapt this for your own resume:
1. Update `patrick.json` with your information
2. Modify the AI prompt in `llm.py`
3. Adjust styling in `resume.py` CSS section
4. Update contact links and resume download URL