# AI Blog-to-Social Content Generator

A Flask-based web application that transforms blog posts into platform-specific social media content using AI.

## Features

- Convert blog posts to LinkedIn posts
- Generate Twitter/X threads (3 tweets)
- Create Instagram captions
- Clean, minimal web interface
- AI-powered content transformation

## Project Structure

```
ai-blog-to-social/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main input form
│   └── results.html      # Generated content display
├── static/
│   └── style.css         # Basic styling
└── README.md             # This file
```

## Setup Instructions

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your OpenAI API key:
   ```bash
   set OPENAI_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open http://localhost:5000 in your browser

### Deployment on Render

1. Push your code to GitHub
2. Connect your GitHub repository to Render
3. Set the following environment variables in Render:
   - `OPENAI_API_KEY`: Your OpenAI API key
4. Deploy with these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

## Usage

1. Paste your blog post content into the text area
2. Click "Generate Social Media Content"
3. View the AI-generated content for LinkedIn, Twitter/X, and Instagram
4. Copy and use the generated content on your social platforms