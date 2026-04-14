# LifeLensAI: Predictive Healthcare Intelligence Platform

![LifeLensAI Banner](https://img.shields.io/badge/Status-Development-crimson?style=for-the-badge)
![Tech-Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20MongoDB%20|%20Scikit--Learn-blue?style=for-the-badge)

LifeLensAI is a premium, flagship healthcare intelligence system designed to provide proactive diagnostic insights. By synthesizing clinical benchmarks and physiological data through advanced Machine Learning models, the platform empowers users to monitor and mitigate health risks with AI-driven precision.

## 🚀 Key Features

*   **Flagship Diagnostic Hub:** Centralized access to intelligence modules for Diabetes, Hypertension, and Heart Disease.
*   **Oncology & Respiratory (Coming Soon):** Advanced modules for Breast and Lung Cancer detection.
*   **Medical Minimalism UI:** A sophisticated "Soft Glassmorphism" interface designed for clarity and a premium feel.
*   **Intelligence History:** Persistent diagnostic tracking with MongoDB, allowing users to review clinical trends over time.
*   **Smart Medical Reporting:** Dynamic reports powered by Google Gemini AI, featuring 6-point clinical guidance (Nutrition, Movement, Routine, etc.).

## 🛠️ Technology Stack

*   **Backend:** Python / FastAPI / Uvicorn
*   **Machine Learning:** Scikit-Learn (Random Forest, Gradient Boosting, Logistic Regression)
*   **Database:** MongoDB (Local instance)
*   **AI Engine:** Google Gemini Pro API (Generative Insights)
*   **Frontend:** HTML5 / Vanilla CSS / Modern JS (Glassmorphism design system)

## 📁 Repository Structure

```
LifeLensAI/
├── core/               # Database and configuration
├── datasets/           # Clinical CSV datasets
├── frontend/           # Glassmorphism UI components
├── models/             # Trained ML serializations (.pkl)
├── routes/             # API Endpoints
├── services/           # Predictor and AI Logic
├── .env                # Secure configuration
├── app.py              # Main Application Entry
└── train_models.py     # ML Training Pipeline
```

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.9+
- MongoDB Compass (running on `localhost:27017`)
- Google Gemini API Key

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/your-username/LifeLensAI.git
# Navigate to project
cd LifeLensAI
# Install dependencies
pip install -r requirements.txt
```

### 3. Training the Intelligence Engine
```powershell
python train_models.py
```

### 4. Launching the Platform
```powershell
python app.py
```
Access the dashboard at `http://localhost:8080/dashboard.html`.

## 🛡️ Medical Disclaimer
LifeLensAI is an artificial intelligence-driven assistant for informational purposes only. It is NOT a substitute for professional medical advice, clinical diagnosis, or treatment. Always consult a licensed physician for any medical concerns.
