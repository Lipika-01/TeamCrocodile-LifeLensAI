# 🏥 LifeLensAI: Clinical Predictive Intelligence Platform

![LifeLensAI Banner](https://img.shields.io/badge/Precision-Clinical_Diagnostics-blue?style=for-the-badge)
![AI Stack](https://img.shields.io/badge/ML_Stack-FastAPI_%7C_Scikit--Learn_%7C_Gemini-darkgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Development-Core_Active-orange?style=for-the-badge)

**LifeLensAI** is an enterprise-grade healthcare analytics platform designed for early-stage disease detection. By merging high-fidelity machine learning for clinical tabular data with sophisticated imaging analysis, LifeLensAI provides clinicians and patients with actionable diagnostic insights and personalized health pathways.

---

## 🚀 System Workflow

LifeLensAI follows a rigorous clinical data pipeline to ensure diagnostic precision:

1.  **Patient Authentication**: Secure JWT-based access control to protect medical records.
2.  **Diagnostic Module Selection**: Users choose from specialized engines (Diabetes, Cardiac, Oncology, etc.).
3.  **Data Ingestion**:
    *   **Clinical Markers**: Manual entry of biomarkers (e.g., HbA1c, LDL, SBP).
    *   **Diagnostic Imaging**: Direct upload of Mammography or Neuro-scans (MRI).
4.  **AI Analysis Engine**:
    *   **Predictive Core**: Tabular data is processed via Scikit-Learn pipelines.
    *   **Vision Core**: Grayscale intensity profiling and anatomical calibration for imaging.
5.  **Intelligence Synthesis**: Google Gemini AI analyzes the ML output to generate natural-language reasoning and medical recommendations.
6.  **Comprehensive Reporting**: Generation of a multi-dimensional "Doctor Report" containing risk stratification and next steps.

---

## 🧬 Disease Intelligence Modules

### 🩸 Diabetes Mellitus
*   **Focus**: analyzes metabolic and glycemic biomarkers.
*   **Key Markers**: Fasting Blood Sugar (FBS), HbA1c, BMI, Insulin, and Postprandial Blood Sugar (PPBS).
*   **ML Approach**: Uses ensemble classification to detect pre-diabetic and diabetic patterns with a high-fidelity precision floor.

### 🫀 Heart Disease (Cardiac Events)
*   **Focus**: Stratifies risk for cardiovascular events.
*   **Key Markers**: Chest pain type (CP), Resting BP (Trestbps), Serum Cholesterol, Maximum Heart Rate (Thalach), and ST depression (Oldpeak).
*   **ML Approach**: Integrates comorbid risk factors (Diabetes/Hypertension status) to provide a holistic vascular health score.

### 🩺 Hypertension (Arterial Health)
*   **Focus**: Calculates vascular resistance and longitudinal arterial risk.
*   **Key Markers**: Systolic/Diastolic BP, LDL/HDL Cholesterol, and Triglycerides.
*   **ML Approach**: Combines dietary patterns with lipid density markers for vascular stratification.

### 🧠 Brain Tumor (Neuro-Imaging)
*   **Focus**: Automated identification of intracranial irregularities.
*   **Diagnostic Classes**: Glioma, Meningioma, Pituitary Hypertrophy, or Healthy.
*   **Vision Approach**: Employs **Neuro-Contouring Intensity Analysis** to detect regional hypertrophy and intensity variance in MRI grayscale data.

### 🎗️ Breast Cancer (Dual-Mode)
*   **Tabular Data**: Analyzes cellular variance metrics (Mean Radius, Texture, Perimeter, and Smoothness).
*   **Imaging Data**: Analyzes Mammography scans for localized hyper-dense mass clusters and irregular margins.
*   **ML Approach**: Parallel inference combining cellular architecture and mass density.

### 🚬 Lung Cancer
*   **Focus**: Risk factor exposure and symptomatic pattern matching.
*   **Key Markers**: Smoking/Alcohol history, fatigue, shortness of breath, and chest pain intensity.
*   **ML Approach**: Categorical risk profiling based on lifestyle exposure and physiological indicators.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) (Python-based Async Core) |
| **Machine Learning** | [Scikit-Learn](https://scikit-learn.org/) (Production-grade Tabular Pipelines) |
| **Vision Analysis** | PIL (Pillow), NumPy (Hardware-Independent Pixel Profiling) |
| **Generative AI** | [Google Gemini AI](https://aistudio.google.com/) (Clinical Reasoning & Recommendations) |
| **Database** | [MongoDB](https://www.mongodb.com/) (Non-Relational Medical Record Storage) |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES6+) |
| **Security** | JWT (JSON Web Tokens), Bcrypt Hashing |

---

## 🧠 How the ML Models Work

### 1. Tabular Data (Ensemble Pipelines)
LifeLensAI utilizes pre-trained Scikit-Learn models stored in serialized `.pkl` formats. 
*   **Normalization**: Input clinical markers are mapped to standardized units (e.g., mg/dL, mmHg).
*   **Inference**: Models utilize weighted features where glycemic markers (for Diabetes) or vascular markers (for Cardiac) carry higher diagnostic weight.
*   **Calibration**: Each output includes a "Clinical Calibration" layer that ensures result reliability even in demo environments, providing a confidence score alongside the prediction.

### 2. Vision Core (Clinical Intensity Profiling)
Unlike traditional heavy-weight CNNs, the imaging module uses an **Augmented Clinical Inference** system:
*   **Grayscale Conversion**: Normalizes image data to luminosity values.
*   **Anatomical Baseline**: Calculates a "Clinical Noise Floor" to filter out artifacting.
*   **Structural Variance**: Measures the "Density" and "Contrasting Patterns" of localized pixel clusters to detect malignant mass characteristics or neurological hypertrophy.

---

## ⚙️ Installation & Usage

### Prerequisites
*   Python 3.9+
*   MongoDB (Local or Atlas)
*   Google Gemini API Key

### Setup
1. Clone the repository and navigate to the root.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Configure the `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY=your_key_here
   MONGO_URI=mongodb://localhost:27017
   JWT_SECRET=your_secret_key
   ```
4. Run the development server:
   ```bash
   cd backend
   python app.py
   ```
5. Access the platform at `http://localhost:8000`.

---

> [!CAUTION]
> **Clinical Disclaimer**: LifeLensAI is a predictive intelligence platform intended for informational and research purposes. All AI-generated reports should be validated by board-certified medical professionals before clinical decision-making.
