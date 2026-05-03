from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

# -------------------------------
# Load model and vectorizer
# -------------------------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# -------------------------------
# Flask setup
# -------------------------------
app = Flask(__name__)
CORS(app)

# -------------------------------
# Feature list (aspects)
# -------------------------------
features = ["battery", "camera", "display", "sound", "performance"]

# -------------------------------
# Sentiment keywords
# -------------------------------
positive_words = ["good", "great", "excellent", "amazing", "nice", "best"]
negative_words = ["bad", "worst", "poor", "terrible", "not good", "not great"]

# -------------------------------
# BUT logic (IMPORTANT FIX)
# -------------------------------
def handle_but_logic(text):
    text = text.lower()
    if "but" in text:
        parts = text.split("but")
        return parts[-1]   # take second part
    return text

# -------------------------------
# Aspect-based analysis
# -------------------------------
def analyze_aspects(text):
    text = text.lower()
    result = {}

    # Split sentence on "but"
    parts = text.split("but")

    for part in parts:
        words = part.split()

        for feature in features:
            if feature in words:
                if "not good" in part or "not great" in part:
                    result[feature] = "Not Satisfied ❌"
                elif any(w in part for w in ["bad", "worst", "poor", "terrible"]):
                    result[feature] = "Not Satisfied ❌"
                elif any(w in part for w in ["good", "great", "excellent", "amazing", "nice", "best"]):
                    result[feature] = "Satisfied ✅"
                else:
                    result[feature] = "Neutral 😐"

    return result

# -------------------------------
# API route
# -------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "Empty input"}), 400

        # 👉 APPLY BUT LOGIC HERE
        processed_text = handle_but_logic(text)

        # Overall prediction (using processed text)
        vector = vectorizer.transform([processed_text])
        prediction = model.predict(vector)[0]

        # Aspect prediction (use original text)
        aspects = analyze_aspects(text)

        # Count satisfied vs not satisfied aspects
        satisfied_count = sum(1 for v in aspects.values() if "Satisfied ✅" in v)
        not_satisfied_count = sum(1 for v in aspects.values() if "Not Satisfied ❌" in v)

        # If both positive and negative aspects exist, override prediction to Neutral
        if satisfied_count > 0 and not_satisfied_count > 0:
            prediction = "Neutral"

        return jsonify({
            "prediction": prediction,
            "aspects": aspects
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Run server
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
    