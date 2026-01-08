import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("dataset/student_mat.csv", sep=";")

df["attendance"] = 100 - (df["absences"] * 2)
df["attendance"] = df["attendance"].clip(lower=0)

df["final_score"] = (df["G1"] + df["G2"] + df["G3"]) / 3

low_cut = df["final_score"].quantile(0.33)
high_cut = df["final_score"].quantile(0.66)

def risk_label(score):
    if score >= high_cut:
        return 0
    elif score >= low_cut:
        return 1
    else:
        return 2

df["risk"] = df["final_score"].apply(risk_label)

print("Risk distribution:")
print(df["risk"].value_counts())

features = [
    "attendance",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2"
]

X = df[features]
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

log_model = LogisticRegression(max_iter=3000)
rf_model = RandomForestClassifier(
    n_estimators=400,
    max_depth=12,
    random_state=42
)

log_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

log_acc = accuracy_score(y_test, log_model.predict(X_test)) * 100
rf_acc = accuracy_score(y_test, rf_model.predict(X_test)) * 100

PACK = {
    "models": {
        "logistic": {
            "model": log_model,
            "accuracy": round(log_acc, 2)
        },
        "random_forest": {
            "model": rf_model,
            "accuracy": round(rf_acc, 2)
        }
    },
    "scaler": scaler,
    "features": features,
    "cuts": {
        "low": float(low_cut),
        "high": float(high_cut)
    }
}

with open("model/student_models.pkl", "wb") as f:
    pickle.dump(PACK, f)

print("Models trained & saved")
print("Logistic Accuracy:", log_acc)
print("RandomForest Accuracy:", rf_acc)
