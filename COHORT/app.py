import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client variable
client = None

def get_openai_client():
    global client
    if not client:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
    return client

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    """
    Handle the blog content submission and generate social media posts.
    """
    data = request.json
    blog_content = data.get('content')

    if not blog_content:
        return jsonify({'error': 'No content provided'}), 400

    try:
        # Get the client
        client_instance = get_openai_client()
        if not client_instance:
            # Smart Mock: Use the user's input to make it relatable
            snippet = blog_content[:100] + "..." if len(blog_content) > 100 else blog_content
            
            return jsonify({
                'linkedin': f"�️ **The Society Papers: On Matters of Note**\n\nDearest Professional Network,\n\nIt has come to my attention that a new thought has entered the marketplace: \"{snippet}\"\n\nOne cannot simply ignore such a development. In my latest correspondence, I explore the depths of this topic with the rigor it demands. The successful courtier of business knows that knowledge is power.\n\nDo partake in the full article. It would be a scandal to miss it.\n\n#ThoughtLeadership #TheSeason #ProfessionalExcellence",
                
                'twitter': f"1/5 🧵 Extra! Extra! Lady Whistledown reports on: {snippet}\n\n2/5 One must ask: is this the future we were promised? 🧐\n\n3/5 The Ton is abuzz with speculation. My take? It is bold, it is daring.\n\n4/5 Do not be a wallflower in this debate. Read the full account! �\n\n5/5 Link in bio. #Trending #Whistledown #SocialSeason",
                
                'instagram': f"Dearest Gentle Reader, 🌸\n\nTonight, we discuss a matter of great import: \"{snippet}\"\n\nAre you the Diamond of the season, or merely a face in the crowd? 💎\n\nI have penned a guide to ensure you remain the talk of the Ton.\n\nLink in bio. Do hurry.\n\n#BridgertonVibes #SocialStrategy #DiamondOfTheSeason #LadyWhistledown"
            })

        # IMPROVED PROMPT for "Big and Impressive" output
        prompt = f"""
        You are a world-class social media strategist for a premium brand. 
        Your task is to repurpose the following blog post into high-impact, viral-ready social media content.
        
        The Tone must be: **Authoritative, Engaging, and Slightly Witty (Bridgerton-esque elegance is a plus but keep it professional)**.

        Blog Content:
        {blog_content[:4000]}

        ### 1. LinkedIn Post (Professional & Insightful)
        - **Hook**: Start with a provocative question or bold statement.
        - **Body**: 3-4 short, punchy paragraphs summarizing the key insight. Use bullet points if compliant.
        - **Conclusion**: strong Call to Action (CTA).
        - **Hashtags**: 3-5 relevant, high-traffic hashtags.

        ### 2. Twitter/X Thread (Viral & Punchy)
        - Create a thread of 5 tweets.
        - **Tweet 1**: The Hook (Must stop the scroll).
        - **Tweets 2-4**: Key value bombs 💣.
        - **Tweet 5**: The CTA and link placeholder.

        ### 3. Instagram Caption (Visual & Storytelling)
        - **Headline**: Catchy title with emojis.
        - **Body**: A short micro-story or 'Behind the Scenes' vibe.
        - **CTA**: "Link in Bio".
        - **Hashtags**: 10-15 relevant tags.

        FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:
        [LINKEDIN]
        (Content)

        [TWITTER]
        (Content)

        [INSTAGRAM]
        (Content)
        """

        response = client_instance.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful social media assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        generated_text = response.choices[0].message.content

        # Parse the response (simple parsing based on markers)
        linkedin_content = ""
        twitter_content = ""
        instagram_content = ""

        current_section = None
        lines = generated_text.split('\n')
        
        for line in lines:
            if '[LINKEDIN]' in line:
                current_section = 'linkedin'
            elif '[TWITTER]' in line:
                current_section = 'twitter'
            elif '[INSTAGRAM]' in line:
                current_section = 'instagram'
            else:
                if current_section == 'linkedin':
                    linkedin_content += line + "\n"
                elif current_section == 'twitter':
                    twitter_content += line + "\n"
                elif current_section == 'instagram':
                    instagram_content += line + "\n"

        return jsonify({
            'linkedin': linkedin_content.strip(),
            'twitter': twitter_content.strip(),
            'instagram': instagram_content.strip()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
