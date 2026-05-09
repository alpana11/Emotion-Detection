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
features = [
    "battery", "camera", "display", "sound", "performance",
    "service", "food", "quality", "price"
]

# -------------------------------
# Text correction (NEW 🔥)
# -------------------------------
def correct_text(text):
    corrections = {
        "wosre": "worse",
        "gud": "good",
        "bd": "bad"
    }
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    return text

# -------------------------------
# BUT logic
# -------------------------------
def handle_but_logic(text):
    text = text.lower()
    if "but" in text:
        parts = text.split("but")
        return parts[-1]   # focus on second part
    return text

# -------------------------------
# Aspect-based analysis
# -------------------------------
def analyze_aspects(text):
    text = text.lower()
    result = {}

    # Handle both "and" + "but"
    parts = text.replace("and", "but").split("but")

    for part in parts:
        part = part.strip()
        words = part.split()

        for feature in features:
            if feature in words:
                if "not good" in part or "not great" in part:
                    result[feature] = "Not Satisfied "
                elif any(w in part for w in ["bad", "worst", "worse", "poor", "terrible"]):
                    result[feature] = "Not Satisfied "
                elif any(w in part for w in ["good", "great", "excellent", "amazing", "nice", "best"]):
                    result[feature] = "Satisfied "
                else:
                    result[feature] = "Neutral "

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

        # 🔥 Fix spelling issues
        text = correct_text(text)

        # Apply BUT logic
        processed_text = handle_but_logic(text)

        # Convert text to vector
        vector = vectorizer.transform([processed_text])

        # RAW prediction
        raw_prediction = model.predict(vector)[0]

        # FINAL prediction
        prediction = raw_prediction

        # Aspect analysis
        aspects = analyze_aspects(text)

        # Count sentiments
        satisfied_count = sum(1 for v in aspects.values() if "Satisfied" in v)
        not_satisfied_count = sum(1 for v in aspects.values() if "Not" in v)

        # Override if mixed
        if satisfied_count > 0 and not_satisfied_count > 0:
            prediction = "Neutral"

        # -------------------------------
        # Backend Output (Clean)
        # -------------------------------
    
        print("FINAL PREDICTION:", prediction)
        print("Feature Analysis:")

        if aspects:
            for feature, value in aspects.items():
                print(f"{feature} → {value}")
        else:
            print("No features detected")


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
    