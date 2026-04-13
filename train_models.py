import pandas as pd
import numpy as np
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Ensure models directory exists
os.makedirs('models', exist_ok=True)

# ---------------------------------------------------------
# 1. DIABETES MODEL
# ---------------------------------------------------------
print("Training Diabetes Model...")
diabetes_path = 'datasets/diabetes.csv'
if os.path.exists(diabetes_path):
    df_diabetes = pd.read_csv(diabetes_path)
    
    # Replace 0 values with NaN to calculate median correctly, then fill
    cols_with_zeros = ['Glucose', 'BloodPressure', 'BMI', 'Insulin']
    for col in cols_with_zeros:
        df_diabetes[col] = df_diabetes[col].replace(0, np.nan)
        median_val = df_diabetes[col].median()
        df_diabetes[col] = df_diabetes[col].fillna(median_val)
        
    features_diabetes = ['Glucose', 'BMI', 'Age', 'BloodPressure', 'Insulin']
    X_diabetes = df_diabetes[features_diabetes]
    y_diabetes = df_diabetes['Outcome']
    
    model_diabetes = LogisticRegression(max_iter=1000)
    model_diabetes.fit(X_diabetes, y_diabetes)
    
    with open('models/diabetes_model.pkl', 'wb') as f:
        pickle.dump(model_diabetes, f)
    print("Saved diabetes_model.pkl")
else:
    print(f"Error: {diabetes_path} not found.")

# ---------------------------------------------------------
# 2. HYPERTENSION MODEL
# ---------------------------------------------------------
print("\nTraining Hypertension Model...")
hyper_path = 'datasets/clean_hypertension.csv'
if os.path.exists(hyper_path):
    df_hyper = pd.read_csv(hyper_path)
    
    # Dataset already seems partially cleaned (age in years, BMI exists).
    # Removing unrealistic BP values
    df_hyper = df_hyper[(df_hyper['ap_hi'] < 300) & (df_hyper['ap_hi'] > 40)]
    df_hyper = df_hyper[(df_hyper['ap_lo'] < 200) & (df_hyper['ap_lo'] > 20)]
    
    # Custom target: 1 if ap_hi >= 140 OR ap_lo >= 90 else 0
    df_hyper['hypertension_target'] = np.where((df_hyper['ap_hi'] >= 140) | (df_hyper['ap_lo'] >= 90), 1, 0)
    
    features_hyper = ['ap_hi', 'ap_lo', 'BMI', 'age', 'cholesterol']
    X_hyper = df_hyper[features_hyper]
    y_hyper = df_hyper['hypertension_target']
    
    # Using Random Forest
    model_hyper = RandomForestClassifier(n_estimators=100, random_state=42)
    model_hyper.fit(X_hyper, y_hyper)
    
    with open('models/hypertension_model.pkl', 'wb') as f:
        pickle.dump(model_hyper, f)
    print("Saved hypertension_model.pkl")
else:
    print(f"Error: {hyper_path} not found.")

# ---------------------------------------------------------
# 3. HEART DISEASE MODEL
# ---------------------------------------------------------
print("\nTraining Heart Disease Model...")
heart_path = 'datasets/heart.csv'
if os.path.exists(heart_path):
    df_heart = pd.read_csv(heart_path)
    
    # Synthesize 'diabetes_result' and 'hypertension_result' for training
    # fbs > 120 is denoted as 1 in the dataset, representing diabetes risk
    df_heart['diabetes_result'] = df_heart['fbs']
    
    # trestbps >= 140 is considered hypertension
    df_heart['hypertension_result'] = np.where(df_heart['trestbps'] >= 140, 1, 0)
    
    # Feature selection as requested
    features_heart = [
        'age', 'cp', 'trestbps', 'chol', 'thalach', 'oldpeak', 'exang',
        'diabetes_result', 'hypertension_result'
    ]
    X_heart = df_heart[features_heart]
    y_heart = df_heart['target']
    
    model_heart = RandomForestClassifier(n_estimators=100, random_state=42)
    model_heart.fit(X_heart, y_heart)
    
    with open('models/heart_model.pkl', 'wb') as f:
        pickle.dump(model_heart, f)
    print("Saved heart_model.pkl")
else:
    print(f"Error: {heart_path} not found.")

print("\nModel training complete.")
