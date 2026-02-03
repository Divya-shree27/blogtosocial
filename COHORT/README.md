# AI Blog-to-Social Content Generator

A Flask-based web application that uses AI to repurpose blog content into platform-specific posts for LinkedIn, Twitter/X, and Instagram.

## Project Structure
```
/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend user interface
├── static/
│   └── style.css       # Custom styling
└── README.md           # Documentation
```

## Features
- **Instant Transformation**: Paste any blog post and get social media content in seconds.
- **Platform-Optimized**:
  - **LinkedIn**: Professional tone with defined structure.
  - **Twitter/X**: Punchy threads ready to post.
  - **Instagram**: Engaging captions with hashtags.
- **Clean UI**: A dark-themed, responsive interface built with modern CSS.

## Setup Instructions

### Prerequisites
- Python 3.8+
- An OpenAI API Key

### Local Installation
1. **Clone the project** (or navigate to the folder).
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up API Key**:
   Create a `.env` file in the root directory and add:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   *Alternatively, export it as an environment variable.*

5. **Run the application**:
   ```bash
   python app.py
   ```
6. **Access**: Open your browser and go to `http://127.0.0.1:5000`

## Deployment (Render)

1. **GitHub**: Push this repository to GitHub.
2. **Render Dashboard**:
   - Create a new **Web Service**.
   - Connect your GitHub repository.
3. **Settings**:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. **Environment Variables**:
   - Add `OPENAI_API_KEY` in the Render environment settings.

## Technology Stack
- **Backend**: Flask (Python)
- **AI Engine**: OpenAI GPT-3.5-Turbo
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
