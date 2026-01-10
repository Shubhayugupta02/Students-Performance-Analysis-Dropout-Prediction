# Student Performance Analysis & Dropout Risk Prediction using Machine Learning

This project focuses on analyzing student academic performance and predicting dropout risk using machine learning and data-driven analytics. The system helps identify students who may require early academic intervention based on multiple academic and behavioral factors.

---

## Problem Statement
Educational institutions often lack early-warning systems to identify students at risk of poor academic performance or dropout. Manual analysis is time-consuming and reactive. This project aims to provide an automated, data-driven solution to predict student risk levels in advance.

---

## Solution Overview
The system collects academic indicators such as marks, attendance, study hours, and failure history, then evaluates student risk using multiple predictive approaches. Results are visualized through an interactive web dashboard for easy interpretation.

---

## Key Features
- Student risk prediction (Low / Medium / High)
- Multiple prediction approaches:
  - Rule-based logic
  - Logistic Regression
  - Random Forest
- Continuous risk score (0–100)
- Prediction confidence visualization
- Interactive dashboards and charts
- Prediction history tracking
- Early warning alerts for high-risk students
- Secure cloud-based data storage

---

## Technologies Used

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn (Logistic Regression, Random Forest)
- Data preprocessing and feature scaling

### Database
- Firebase Firestore (real-time NoSQL database)

### Frontend
- HTML, CSS, JavaScript
- Google Charts for data visualization
- Responsive UI with cyber-neon design

### Deployment
- Render (Free Tier)

---

## Dataset
- Student academic dataset (`student_mat.csv`)
- Features include attendance, grades, failures, and study habits
- Dataset used for training and evaluating ML models

---

## Dashboard & Visualization
- Risk distribution (Pie chart)
- Attendance trend over time (Line chart)
- Performance score comparison (Bar chart)
- Model-based confidence indicators

---

## Security & Configuration
- Firebase credentials are **not stored in the repository**
- Sensitive keys are managed using environment variables
- `.gitignore` is used to prevent accidental key exposure

---

## Deployment Notes
This application is deployed on **Render Free Tier**.  
Due to platform limitations, the app may experience a **cold start delay (2–5 minutes)** after inactivity. Once active, the application runs normally.

---

## Future Enhancements
- Personalized academic improvement roadmap
- Advanced explainable AI (feature-level insights)
- Model performance comparison dashboard
- Student profile-wise analytics
- Role-based access for institutions

---

## Conclusion
This project demonstrates how machine learning and modern web technologies can be combined to build an intelligent academic risk prediction system. It provides a practical solution for early identification of students who may need support, enabling proactive educational interventions.

---

## Author
Developed as part of an academic and innovation project for student performance analysis and dropout risk prediction.
