import pandas as pd
import numpy as np
import pickle
import re
import nltk
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# NLTK setup
nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')

# --- Preprocessing Function ---
def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)
    text = text.lower()
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

# --- Load Dataset ---
print("Loading dataset...")
df = pd.read_csv("fake_news.csv")  # Dataset with 'text' and 'label' columns
df.dropna(inplace=True)
df['text'] = df['text'].apply(clean_text)

# --- Train/Test Split ---
X = df['text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Vectorization ---
vectorizer = TfidfVectorizer(max_df=0.7)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# --- Model Training ---
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# --- Evaluation ---
y_pred = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# --- Save model and vectorizer ---
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

# --- Flask API Setup ---
app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route('/')
def home():
    return "Fake News Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = clean_text(data['text'])
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return jsonify({'prediction': prediction})

# --- Run Flask App ---
if __name__ == '__main__':
    app.run(debug=True)
