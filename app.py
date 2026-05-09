from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

app = Flask(__name__)
CORS(app)

features = [
    "battery", "camera", "display", "sound", "performance",
    "service", "food", "quality", "price"
]

def correct_text(text):
    corrections = {
        "wosre": "worse",
        "gud": "good",
        "bd": "bad"
    }
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    return text

def handle_but_logic(text):
    text = text.lower()
    if "but" in text:
        parts = text.split("but")
        return parts[-1]   
    return text

def analyze_aspects(text):
    text = text.lower()
    result = {}
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


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"error": "Empty input"}), 400

     
        text = correct_text(text)

        processed_text = handle_but_logic(text)

        vector = vectorizer.transform([processed_text])

        raw_prediction = model.predict(vector)[0]
        
        prediction = raw_prediction

        aspects = analyze_aspects(text)

        satisfied_count = sum(1 for v in aspects.values() if "Satisfied" in v)
        not_satisfied_count = sum(1 for v in aspects.values() if "Not" in v)

        if satisfied_count > 0 and not_satisfied_count > 0:
            prediction = "Neutral"

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
    
if __name__ == '__main__':
    app.run(debug=True)
    