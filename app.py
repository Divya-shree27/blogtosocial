"""
AI Blog-to-Social Content Generator
A Flask web application that transforms blog posts into social media content using OpenAI's API.
"""

import os
from flask import Flask, render_template, request, flash, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def generate_social_content(blog_text):
    """
    Generate platform-specific social media content from blog text using OpenAI API.
    
    Args:
        blog_text (str): The original blog post content
        
    Returns:
        dict: Contains generated content for LinkedIn, Twitter, and Instagram
    """
    try:
        # Create prompts for each platform
        prompts = {
            'linkedin': f"""
            Transform this blog post into a professional LinkedIn post. Make it engaging, 
            professional, and include relevant hashtags. Keep it under 300 words.
            
            Blog content: {blog_text}
            """,
            
            'twitter': f"""
            Create a Twitter/X thread of exactly 3 tweets from this blog post. 
            Each tweet should be under 280 characters and connected with thread numbers (1/3, 2/3, 3/3).
            Make them engaging and include relevant hashtags.
            
            Blog content: {blog_text}
            """,
            
            'instagram': f"""
            Transform this blog post into an Instagram caption. Make it engaging, 
            include relevant hashtags, and add emojis. Keep it under 400 words.
            
            Blog content: {blog_text}
            """
        }
        
        generated_content = {}
        
        # Generate content for each platform
        for platform, prompt in prompts.items():
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a social media content expert who creates engaging, platform-specific posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            generated_content[platform] = response.choices[0].message.content.strip()
        
        return generated_content
        
    except Exception as e:
        # Log the error and return None to handle gracefully
        print(f"Error generating content: {str(e)}")
        return None

@app.route('/')
def index():
    """
    Render the main page with the blog input form.
    """
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """
    Handle form submission and generate social media content.
    """
    # Get blog text from form
    blog_text = request.form.get('blog_text', '').strip()
    
    # Validate input
    if not blog_text:
        flash('Please enter some blog content to transform.', 'error')
        return redirect(url_for('index'))
    
    if len(blog_text) < 50:
        flash('Please enter at least 50 characters of blog content.', 'error')
        return redirect(url_for('index'))
    
    # Check if API key is configured
    if not os.environ.get('OPENAI_API_KEY'):
        flash('OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable.', 'error')
        return redirect(url_for('index'))
    
    # Generate social media content
    generated_content = generate_social_content(blog_text)
    
    if generated_content is None:
        flash('Error generating content. Please try again.', 'error')
        return redirect(url_for('index'))
    
    # Render results page with generated content
    return render_template('results.html', 
                         original_text=blog_text,
                         linkedin_post=generated_content['linkedin'],
                         twitter_thread=generated_content['twitter'],
                         instagram_caption=generated_content['instagram'])

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    flash('An internal error occurred. Please try again.', 'error')
    return render_template('index.html'), 500

if __name__ == '__main__':
    # Run the Flask app
    # Use environment variables for configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)