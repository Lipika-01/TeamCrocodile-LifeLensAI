import os
import pickle
import pandas as pd

def get_bp_category(sys, dia):
    if sys < 120 and dia < 80:
        return 0 # Normal
    elif 120 <= sys <= 129 and dia < 80:
        return 1 # Elevated
    elif 130 <= sys <= 139 or 80 <= dia <= 89:
        return 2 # High BP (Stage 1)
    else:
        return 3 # High BP (Stage 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return 0 # Underweight
    elif 18.5 <= bmi < 25:
        return 1 # Normal
    elif 25 <= bmi < 30:
        return 2 # Overweight
    else:
        return 3 # Obese

def get_glucose_category(glucose):
    if glucose < 100:
        return 0 # Normal
    elif 100 <= glucose <= 125:
        return 1 # Prediabetes
    else:
        return 2 # Diabetes

class HealthcarePredictor:
    def __init__(self):
        self.diabetes_model = None
        self.hyper_model = None
        self.heart_model = None
        self._load_models()

    def _load_models(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'models')
        
        try:
            with open(os.path.join(models_dir, 'diabetes_model.pkl'), 'rb') as f:
                self.diabetes_model = pickle.load(f)
            
            with open(os.path.join(models_dir, 'hypertension_model.pkl'), 'rb') as f:
                self.hyper_model = pickle.load(f)
            
            with open(os.path.join(models_dir, 'heart_model.pkl'), 'rb') as f:
                self.heart_model = pickle.load(f)
                
            print("Optimized Pipelines loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")

    def predict_diabetes(self, glucose, bmi, age, bp, insulin):
        if not self.diabetes_model: return None
        
        bp_ctg = get_bp_category(bp, 80) # Using 80 as arbitrary dia for diabetes logic mapping
        bmi_ctg = get_bmi_category(bmi)
        glu_ctg = get_glucose_category(glucose)
        
        features = [[glucose, bmi, age, bp, insulin, bp_ctg, bmi_ctg, glu_ctg]]
        columns = ['Glucose', 'BMI', 'Age', 'BloodPressure', 'Insulin', 'BP_category', 'BMI_category', 'Glucose_category']
        df = pd.DataFrame(features, columns=columns)
        
        prediction = self.diabetes_model.predict(df)[0]
        probability = self.diabetes_model.predict_proba(df)[0]
        
        prob_positive = probability[1] * 100
        if prob_positive < 30: risk = "Low"
        elif prob_positive < 60: risk = "Medium"
        else: risk = "High"

        return {
            "prediction": int(prediction),
            "probability_percent": round(prob_positive, 1),
            "risk_level": risk,
            "status": "Positive" if prediction == 1 else "Negative"
        }

    def predict_hypertension(self, ap_hi, ap_lo, bmi, age, cholesterol):
        if not self.hyper_model: return None
        
        bp_ctg = get_bp_category(ap_hi, ap_lo)
        bmi_ctg = get_bmi_category(bmi)
        
        features = [[ap_hi, ap_lo, bmi, age, cholesterol, bp_ctg, bmi_ctg]]
        columns = ['ap_hi', 'ap_lo', 'BMI', 'age', 'cholesterol', 'BP_category', 'BMI_category']
        df = pd.DataFrame(features, columns=columns)
        
        prediction = self.hyper_model.predict(df)[0]
        probability = self.hyper_model.predict_proba(df)[0]
        
        prob_positive = probability[1] * 100
        if prob_positive < 40: risk = "Low"
        elif prob_positive < 70: risk = "Medium"
        else: risk = "High"

        return {
            "prediction": int(prediction),
            "probability_percent": round(prob_positive, 1),
            "risk_level": risk,
            "status": "Positive" if prediction == 1 else "Negative"
        }

    def predict_heart_disease(self, age, cp, trestbps, chol, thalach, oldpeak, exang, diabetes_res, hyper_res):
        if not self.heart_model: return None
        
        bp_ctg = get_bp_category(trestbps, 80)
        
        features = [[age, cp, trestbps, chol, thalach, oldpeak, exang, diabetes_res, hyper_res, bp_ctg]]
        columns = ['age', 'cp', 'trestbps', 'chol', 'thalach', 'oldpeak', 'exang', 'diabetes_result', 'hypertension_result', 'BP_category']
        df = pd.DataFrame(features, columns=columns)
        
        prediction = self.heart_model.predict(df)[0]
        probability = self.heart_model.predict_proba(df)[0]
        
        prob_positive = probability[1] * 100
        if prob_positive < 30: risk = "Low"
        elif prob_positive < 60: risk = "Medium"
        else: risk = "High"

        return {
            "prediction": int(prediction),
            "probability_percent": round(prob_positive, 1),
            "risk_level": risk,
            "status": "Positive" if prediction == 1 else "Negative"
        }

predictor = HealthcarePredictor()
