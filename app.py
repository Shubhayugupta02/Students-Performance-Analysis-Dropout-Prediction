from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from firebase_config import db
import pickle
import numpy as np
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "student_models.pkl")

MODELS = {}
SCALER = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        PACK = pickle.load(f)
        MODELS = PACK.get("models", {})
        SCALER = PACK.get("scaler", None)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/prediction")
def prediction():
    return render_template("predict.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

def rule_engine(attendance, marks, study_hours, failures):
    score = 0

    score += 40 if marks >= 60 else 25 if marks >= 30 else 10
    score += 30 if failures == 0 else 18 if failures <= 2 else 5
    score += 20 if attendance > 75 else 12 if attendance >= 40 else 5
    score += 10 if study_hours > 4 else 6 if study_hours >= 2 else 2

    return score

def score_to_risk(score):
    if score >= 70:
        return "LOW"
    elif score >= 40:
        return "MEDIUM"
    return "HIGH"

@app.route("/predict", methods=["POST"])
def predict():
    d = request.json

    model_name = d.get("model", "rule")
    attendance = int(d["attendance"])
    marks = int(d["marks"])
    study_hours = int(d["study_hours"])
    failures = int(d["failures"])

    score = rule_engine(attendance, marks, study_hours, failures)
    risk = score_to_risk(score)

    confidence = 0

    if model_name == "rule" or model_name not in MODELS:
        confidence = min(95, 60 + score // 2)

    else:
        X = np.array([[attendance, study_hours, failures, abs(100 - attendance), marks, marks]])

        X_scaled = SCALER.transform(X)
        model = MODELS[model_name]["model"]

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_scaled)[0]
            confidence = int(max(probs) * 100)
        else:
            confidence = MODELS[model_name].get("accuracy", 75)

        confidence = max(55, min(confidence, 97))

    importance = {
        "Marks": 45,
        "Failures": 30,
        "Attendance": 15,
        "Study Hours": 10
    }

    alert = risk == "HIGH"

    db.collection("predictions").add({
        "attendance": attendance,
        "marks": marks,
        "study_hours": study_hours,
        "failures": failures,
        "risk": risk,
        "score": score,
        "confidence": confidence,
        "model": model_name,
        "timestamp": datetime.utcnow()
    })

    return jsonify({
        "risk": risk,
        "score": score,
        "confidence": confidence,
        "importance": importance,
        "alert": alert
    })

@app.route("/api/dashboard-data")
def dashboard_data():
    docs = db.collection("predictions").order_by("timestamp").stream()

    low = medium = high = 0
    attendance = []
    scores = []
    times = []
    risks = []

    for d in docs:
        r = d.to_dict()

        if r["risk"] == "LOW":
            low += 1
        elif r["risk"] == "MEDIUM":
            medium += 1
        else:
            high += 1

        attendance.append(r["attendance"])
        scores.append(r["score"])
        times.append(r["timestamp"].strftime("%H:%M"))
        risks.append(r["risk"])

    return jsonify({
        "low": low,
        "medium": medium,
        "high": high,
        "attendance": attendance,
        "scores": scores,
        "times": times,
        "risks": risks
    })

@app.route("/history")
def history():
    docs = db.collection("predictions").order_by("timestamp", direction="DESCENDING").stream()
    return render_template("history.html", records=[d.to_dict() for d in docs])

@app.route("/clear-data", methods=["POST"])
def clear():
    docs = db.collection("predictions").stream()
    for d in docs:
        d.reference.delete()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
