from flask import Flask, request, render_template
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)

# Load data
df = pd.read_excel("data.xlsx")
titles = df["title"].tolist()

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
embeddings = vectorizer.fit_transform(titles)

@app.route('/', methods=['GET', 'POST'])
def recommend():
    recommendations = []

    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form['user_input']

        # Transform user input to the same vector space
        user_input_embedding = vectorizer.transform([user_input])

        # Find the most similar titles
        distances = cosine_similarity(user_input_embedding, embeddings)
        indices = distances.argsort()[0][-7:][::-1]  # Get the top 5 similar titles

        # Prepare recommendations
        for i in range(1, 6):
            recommendations.append({
                'title': df['title'][indices[i]],
                'year': df['year'][indices[i]],
                'abstract': df['abstract'][indices[i]][:200]+"..."
            })

    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
