import os
import pickle
import pandas as pd

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
                
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")

    def predict_diabetes(self, glucose, bmi, age, bp, insulin):
        if not self.diabetes_model:
            return None
        features = [[glucose, bmi, age, bp, insulin]]
        columns = ['Glucose', 'BMI', 'Age', 'BloodPressure', 'Insulin']
        df = pd.DataFrame(features, columns=columns)
        
        prediction = self.diabetes_model.predict(df)[0]
        probability = self.diabetes_model.predict_proba(df)[0]
        
        # Determine risk level
        prob_positive = probability[1] * 100
        if prob_positive < 33:
            risk = "Low"
        elif prob_positive < 66:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "prediction": int(prediction),
            "probability_percent": round(prob_positive, 2),
            "risk_level": risk,
            "status": "Positive" if prediction == 1 else "Negative"
        }

    def predict_hypertension(self, ap_hi, ap_lo, bmi, age, cholesterol):
        if not self.hyper_model:
            return None
        features = [[ap_hi, ap_lo, bmi, age, cholesterol]]
        columns = ['ap_hi', 'ap_lo', 'BMI', 'age', 'cholesterol']
        df = pd.DataFrame(features, columns=columns)
        
        prediction = self.hyper_model.predict(df)[0]
        probability = self.hyper_model.predict_proba(df)[0]
        
        prob_positive = probability[1] * 100
        if prob_positive < 30:
            risk = "Low"
        elif prob_positive < 60:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "prediction": int(prediction),
            "probability_percent": round(prob_positive, 2),
            "risk_level": risk,
            "status": "Positive" if prediction == 1 else "Negative"
        }

    def predict_heart_disease(self, age, cp, trestbps, chol, thalach, oldpeak, exang, diabetes_res, hyper_res):
        if not self.heart_model:
            return None
        features = [[age, cp, trestbps, chol, thalach, oldpeak, exang, diabetes_res, hyper_res]]
        columns = ['age', 'cp', 'trestbps', 'chol', 'thalach', 'oldpeak', 'exang', 'diabetes_result', 'hypertension_result']
        df = pd.DataFrame(features, columns=columns)
        
        prediction = self.heart_model.predict(df)[0]
        probability = self.heart_model.predict_proba(df)[0]
        
        prob_positive = probability[1] * 100
        if prob_positive < 35:
            risk = "Low"
        elif prob_positive < 65:
            risk = "Medium"
        else:
            risk = "High"

        return {
            "prediction": int(prediction),
            "probability_percent": round(prob_positive, 2),
            "risk_level": risk,
            "status": "Positive" if prediction == 1 else "Negative"
        }

predictor = HealthcarePredictor()
