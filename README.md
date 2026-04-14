# LifeLensAI: Predictive Healthcare Intelligence Platform

![LifeLensAI Status](https://img.shields.io/badge/Status-Premium--Development-crimson?style=for-the-badge)
![Tech-Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20MongoDB%20|%20Scikit--Learn-blue?style=for-the-badge)

LifeLensAI is a flagship healthcare intelligence system designed to provide proactive diagnostic insights through a high-fidelity "Medical Minimalism" interface. By synthesizing clinical benchmarks and physiological data through advanced Machine Learning models, the platform empowers users to monitor and mitigate health risks with AI-driven precision.

## 🚀 Key Features

*   **Global Health Intelligence Hub:** Interactive Draggable Ticker featuring bespoke 3D medical visuals for core disease modules.
*   **Comprehensive Diagnostic Suite:**
    *   **Metabolic:** Diabetes Mellitus (Glycemic dysregulation analysis).
    *   **Vascular:** Hypertension Panel (Arterial health evaluation).
    *   **Cardiac:** Cardia Intelligence (Multi-layered cardiovascular stress engine).
    *   **Oncology:** Breast Health (Cellular variance) and Lung Carcinoma (Lifestyle/Exposure profiling).
*   **Premium Glassmorphism UI:** A sophisticated "Soft Glassmorphism" interface with a dynamic Zig-Zag workflow and interactive diagnostic sidebars.
*   **Smart Medical Reporting:** Dynamic clinical reports powered by **Google Gemini Pro AI**, featuring 6-point personalized guidance.

## 🛠️ Technology Stack

*   **Backend:** Python / FastAPI / Uvicorn
*   **Machine Learning:** Scikit-Learn (Random Forest, Gradient Boosting, Logistic Regression)
*   **Database:** MongoDB (Local instance for medical history storage)
*   **AI Engine:** Google Gemini Pro API (Generative Insights & Clinical Logic)
*   **Frontend:** Vanilla CSS / Modern JS (Custom Draggable Scroll Architecture)

## 📁 Repository Structure

```
LifeLensAI/
├── core/               # Database and configuration
├── datasets/           # Clinical CSV datasets for ML training
├── frontend/           # Premium Glassmorphism UI
│   ├── assets/         # Branding and medical visuals
│   ├── css/            # Medical Minimalism design system
│   └── js/             # Auth guards and draggable UI logic
├── models/             # Trained ML serializations (.pkl)
├── routes/             # RESTful API Endpoints
├── services/           # Predictor and AI Intelligence Logic
├── .env                # Secure configuration (API Keys)
└── train_models.py     # ML Training Pipeline
```

## 🔐 Platform Access

For testing and demonstration, use the following global credentials:

| Field     | Value      |
| --------- | ---------- |
| **Username** | `testuser` |
| **Password** | `testuser` |

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.9+
- MongoDB Compass (running on `localhost:27017`)
- Google Gemini API Key (stored in `.env`)

### 2. Installation & Launch
```powershell
# Clone the repository
git clone https://github.com/Lipika-01/TeamCrocodile-LifeLensAI.git

# Install dependencies
pip install -r requirements.txt

# Train Intelligence Models (Required first time)
python train_models.py

# Launch the Platform
python app.py
```
Access the landing page at `http://localhost:8080/index.html`.

## 🛡️ Medical Disclaimer
LifeLensAI is an artificial intelligence-driven assistant for informational purposes only. It is NOT a substitute for professional medical advice, clinical diagnosis, or treatment. Always consult a licensed physician for any medical concerns.
