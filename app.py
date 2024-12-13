from flask import Flask, render_template, request
from transformers import pipeline
import re

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Define mood keywords
mood_keywords = {
    'happy': ['joy', 'happy', 'excited', 'fun', 'love','cheerful', 'content', 'delighted', 'excited', 'grateful', 'energetic', 'lively', 'upbeat', 'blissful', 'optimistic','shocked', 'astonished', 'amazed', 'stunned', 'surprised', 'speechless', 'startled', 'dumbfounded', 'flabbergasted', 'astounded'],
    'sad': ['sad', 'down', 'depressed', 'cry', 'lonely','low','sorrowful', 'heartbroken', 'gloomy', 'melancholy', 'mournful', 'despair', 'miserable', 'teary', 'downcast', 'disappointed'],
    'angry': ['angry', 'mad', 'frustrated', 'rage', 'irritated','furious', 'enraged', 'livid', 'annoyed', 'upset', 'hostile', 'bitter', 'fuming', 'irritated', 'mad'],
    'neutral': ['okay', 'fine', 'neutral', 'calm', 'bored','indifferent', 'apathetic', 'calm', 'unbothered', 'peaceful', 'relaxed', 'steady', 'composed', 'reserved', 'unperturbed'],
    'romantic': ['romantic', 'love', 'passion', 'heart', 'couple','affection', 'intimate', 'relationship', 'sweet', 'caring', 'heartwarming', 'flirt', 'connection', 'passion', 'date'],
}

# Function to perform mood analysis
def analyze_mood(text: str) -> str:
    sentiment = sentiment_analyzer(text)[0]
    sentiment_label = sentiment['label']
    sentiment_score = sentiment['score']

    mood = 'neutral'  # Default mood
    if sentiment_label == 'POSITIVE' and sentiment_score > 0.7:
        mood = 'happy'
    elif sentiment_label == 'NEGATIVE' and sentiment_score > 0.7:
        mood = 'sad'
    elif sentiment_label == 'NEUTRAL':
        mood = 'neutral'

    # Check for mood-related keywords
    for mood_key, keywords in mood_keywords.items():
        if any(re.search(r'\b' + keyword + r'\b', text, re.IGNORECASE) for keyword in keywords):
            mood = mood_key
            break

    return mood

# Function to get song recommendations based on mood
def get_songs_for_mood(mood: str):
    mood_songs = {
        'happy': ['<a href="https://open.spotify.com/track/3dUAyP58gBCiqCHCMCRnuQ" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/2gKNWPBrI2IRBl2RRUtoEb" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/7MtXu7mXRMdICKyTOb8CuR" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/0hujsbFzpm9RjOs4mnVclo" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/4ZNIkO2j6K2c0Nm8zWXmdn" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/1ifMH14KizpUxIdRVyPsSZ" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/6D2LwdOQ5gjoFrpkoO5fvu" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/6Vq4ePrJPZ2vU6DXnZGcVD" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/6Yqw4HtJuFXleJtgzYXWzT" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/5n1FBtJgcDePfo8q6hBQPu" target="_blank">Song</a>'],
        'sad': [
            '<a href="https://open.spotify.com/track/18r28YOE2nO8hU0bv0lmcv" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/0xNiDPK4YdZ51ALxSid0QV" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/29ffQxBUZLJdN3kiPndB9n" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/4k9RLcTWZog34sIXt23Ibr" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/5Mo0zkOAPtR2rW9kL29X37" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/5VIY9V6s886MPB1mL0PqBr" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/3geKpJNdURFqbA8OqaR7vr" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/5jDcZCA2NJEvk7Kwa6bcE1" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/0fb1PMDfxtOdU0tMD4JlRg" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/5PDx7sVGIIdAlKhdSiUnUj" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/15MG8SOfiHto8HpSQ5Wr0m" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/21pL3j6ZqI2icRLm9bpVM9" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/4mIOdOh49kfRSZBwvylulK" target="_blank">Song</a>',
            '<a href="https://open.spotify.com/track/25PuswEm4kNdKi1wRANLQO" target="_blank">Song</a>',
        ],
        'neutral': ['<a href="https://open.spotify.com/track/3uEpN8gvEULB7MUNX9DQ18" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/2QhpL0cdNWdrvd6g22ePVu" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/4IoL5eSdPTk44UjQf0fk4m" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/1ifMH14KizpUxIdRVyPsSZ" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/0JLLcOdBUKfDtzY0seXQHC" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/0xNiDPK4YdZ51ALxSid0QV" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/0k0isUYnsgYBKjJQykg3uN" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/album/1qcByVSWvB4ozRusDGENer" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/0fYTkcBMtjtP4hzoOxGgSF" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/6vI8sSx4J3oa9It51ZzVZC" target="_blank">Song</a>',
                    '<a href="https://open.spotify.com/track/2DDOQBKGmkv7bPoYF1bELz" target="_blank">Song</a>',
                    ],
        'angry': ['<a href="https://open.spotify.com/track/0hRvv4dQbcfL9R7Gpoacda" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/7LSlA4HRXqhJJeQjq3Hm4R" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/2PtYsJUrW7GFQ2RbpVslG4" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/5zGHViDOEuNaZySWpLgPw6" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/4HB1ILmewz18T9jGNHmmBe" target="_blank">Song</a>',
                  '<a href="https://open.spotify.com/track/40Z8bpGJPxjClb4NK8j0LJ" target="_blank">Song</a>',
                  ],
        'romantic': ['<a href="https://open.spotify.com/track/5dG3KI5rIUwiUQNNr3Y1to" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/46ZWVfAlTic02K5deefyDu" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/5ReOjb2X6TCkMfYoHuVW1b" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/3nCqpSpwxuO4gYF1wGS6WM" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/6Zp14O0N7iNLTrKYSOsOJh" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/3XwpSZtT3clAjJqVW0Cgoi" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/14IWkBxGSiWYYzJa2ho5ZM" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/1kYg9IZJ9QwrnHaJztmK5n" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/7L2D6W7e8mn0zf8cH78Ch4" target="_blank">Song</a>',
                     '<a href="https://open.spotify.com/track/28xt5x1wwoMfVYI9zfIwRx" target="_blank">RSong</a>',
                     '<a href="https://open.spotify.com/track/2rDPTKSWgUbFuV1jFzPqvE" target="_blank">Song</a>'
                     ],
    }
    return mood_songs.get(mood, [])
def get_mood_enhancing_playlist(mood):
    happy = get_songs_for_mood('happy')
    sad = get_songs_for_mood('sad')
    neutral = get_songs_for_mood('neutral')
    romantic = get_songs_for_mood('romantic')
    
    if mood == "sad":
        return sad[:3] + neutral[:3] + romantic[:3] + happy[:3]
    elif mood == "neutral":
        return neutral[:3] + romantic[:3] + happy[:3]
    elif mood == "romantic":
        return romantic[:3] + happy[:3] + neutral[:3]
    elif mood == "happy":
        return happy[:6] + romantic[:6]
    else:
        return neutral

@app.route('/', methods=['GET', 'POST'])
def index():
    songs = None  # Initialize songs to None or empty list to prevent NameError
    if request.method == 'POST':
        # Get the text from the form
        paragraph1 = request.form['paragraph1']
        paragraph2 = request.form['paragraph2']

        # Combine both paragraphs if the second one is provided
        combined_text = paragraph1 + " " + paragraph2 if paragraph2 else paragraph1
        
        # Analyze the mood and get song recommendations
        mood = analyze_mood(combined_text)
        
        # Get mood-enhancing playlist
        songs = get_mood_enhancing_playlist(mood)
        
        # Return the enhanced playlist and mood to the template
        return render_template('index.html', mood=mood, songs=songs)
    
    # Handle GET request by rendering the template with no mood or songs
    return render_template('index.html', mood=None, songs=songs)


if __name__ == '__main__':
    app.run(debug=False)
