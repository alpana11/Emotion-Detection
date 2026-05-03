from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import string
import nltk
from nltk.corpus import stopwords

# Initialize app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # 🔥 IMPORTANT LINE

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = text.replace("not bad", "notbad")
    text = text.replace("not good", "notgood")
    text = "".join([c for c in text if c not in string.punctuation])
    words = text.split()
    words = [w for w in words if w not in stop_words or w == "not"]
    return " ".join(words)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json.get('text')   # safer
    cleaned = clean_text(data)
    vector = vectorizer.transform([cleaned])
    result = model.predict(vector)[0]
    return jsonify({"prediction": result})

if __name__ == '__main__':
    app.run(debug=True)