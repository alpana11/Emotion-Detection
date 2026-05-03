# 🧠 Emotion Detection System with Aspect-Based Analysis

A smart web application that analyzes customer feedback and detects both:

* Overall emotion (Happy 😄 / Angry 😡 / Neutral 😐)
* Feature-level sentiment (Battery ✅ / Camera ❌ etc.)

This helps businesses and shopkeepers understand exactly **what customers like and dislike** in their products.

---

## 🚀 Features

* ✅ Emotion Detection using Machine Learning (TF-IDF + LinearSVC)
* ✅ Aspect-Based Sentiment Analysis (Feature-wise insights)
* ✅ Real-time feedback prediction
* ✅ Clean and modern UI
* ✅ Recent feedback history
* ✅ Handles mixed reviews (e.g., good battery but bad camera)

---

## 🧪 Example

### Input:

Battery is good but camera is bad

### Output:

Emotion: Neutral 😐

Feature Analysis:
battery → Satisfied ✅
camera → Not Satisfied ❌

---

## 🏗️ Project Structure

Emotion-Detection/
│
├── app.py                # Flask backend
├── model.pkl            # Trained ML model
├── vectorizer.pkl       # TF-IDF vectorizer
│
├── index.html           # Main UI
├── login.html           # Login page
├── dashboard.html       # Dashboard UI
│
└── README.md

---

## ⚙️ Tech Stack

* 🐍 Python (Flask)
* 🤖 Machine Learning (Scikit-learn)
* 📊 TF-IDF Vectorization
* 🌐 HTML, CSS, JavaScript
* 🔗 REST API (Fetch)

---

## 🔧 Installation & Setup

### 1️⃣ Clone the repository

git clone https://github.com/your-username/emotion-detection.git
cd emotion-detection

### 2️⃣ Install dependencies

pip install flask flask-cors scikit-learn

### 3️⃣ Run the backend

python app.py

Server will start at:
http://127.0.0.1:5000

### 4️⃣ Open frontend

Open this file in browser:
index.html

---

## 🔌 API Endpoint

### POST /predict

### Request:

{
"text": "Battery is good but camera is bad"
}

### Response:

{
"prediction": "Neutral",
"aspects": {
"battery": "Satisfied ✅",
"camera": "Not Satisfied ❌"
}
}

---

## 📊 Use Case

This system is useful for:

* 🛍️ Shopkeepers analyzing customer feedback
* 📱 Product review analysis
* 🏢 Businesses understanding customer sentiment
* 📈 Improving specific product features
* ⭐ Understanding customer satisfaction in detail

---

## ⚠️ Limitations

* Aspect analysis is rule-based (not fully AI yet)
* Limited to predefined features (battery, camera, etc.)
* Cannot fully understand complex sentences

---

## 🔮 Future Improvements

* 🔥 Train advanced NLP model (BERT / Deep Learning)
* 📊 Add charts and analytics dashboard
* 🌍 Deploy on cloud (AWS / Render / Railway)
* 📱 Mobile app version
* 🧠 Smart aspect detection using AI (no hardcoded features)

---



