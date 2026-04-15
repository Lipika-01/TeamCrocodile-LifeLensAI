import pandas as pd
import numpy as np
import pickle
import os
import warnings
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

warnings.filterwarnings('ignore')

# Project Root Resolution (Ensures script runs from backend root context)
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_ROOT)

def get_path(rel_path):
    # Try backend root first, then project root
    b_path = os.path.join(BACKEND_ROOT, rel_path)
    if os.path.exists(b_path) or not os.path.exists(os.path.join(PROJECT_ROOT, rel_path)):
        return b_path
    return os.path.join(PROJECT_ROOT, rel_path)

os.makedirs(get_path('models'), exist_ok=True)

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------

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

def map_categorical(val):
    """Unified ordinal mapping for survey strings used in clinical datasets."""
    v = str(val).strip().capitalize()
    mapping = {
        'Never': 0, 'No': 0, 
        'Light': 1, 'Rarely': 1, 
        'Moderate': 2, 'Occasionally': 2, 'Yes': 2, 
        'Heavy': 3, 'Frequently': 3
    }
    return mapping.get(v, 1) # Default to 1 (Low/Rarely) if unknown

def evaluate_model(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    print(f"--- {name} Evaluation ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}\n")
    return acc, prec, rec, f1

def train_and_select_best(X, y, models_param_grid):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    best_overall_model = None
    best_overall_score = -1
    best_model_name = ""
    
    for name, mp in models_param_grid.items():
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', mp['model'])
        ])
        
        # Prepend 'classifier__' to parameter grid keys
        param_grid = {f'classifier__{k}': v for k, v in mp['params'].items()}
        
        print(f"Running GridSearchCV for {name}...")
        grid = GridSearchCV(pipeline, param_grid, cv=cv, scoring='accuracy', n_jobs=-1)
        grid.fit(X_train, y_train)
        
        print(f"Best params for {name}: {grid.best_params_}")
        
        best_model = grid.best_estimator_
        y_pred = best_model.predict(X_test)
        
        acc, prec, rec, f1 = evaluate_model(name, y_test, y_pred)
        
        if acc > best_overall_score:
            best_overall_score = acc
            best_overall_model = best_model
            best_model_name = name
            
    print(f">>> Selected {best_model_name} as the best model with test accuracy {best_overall_score:.4f}\n")
    return best_overall_model

# ---------------------------------------------------------
# 1. DIABETES MODEL
# ---------------------------------------------------------
print("="*50)
print("1. TRAINING DIABETES MODEL")
print("="*50)
diabetes_path = get_path('datasets/diabetes_synthetic_dataset.csv')
if os.path.exists(diabetes_path):
    df_diabetes = pd.read_csv(diabetes_path)
    
    # Clinical headers: Age,BMI,FBS_mg_dL,PPBS_mg_dL,HbA1c_pct,SBP_mmHg,DBP_mmHg,Insulin_uU_mL,...
    # Generate binary target if needed (Diabetes_Risk_Pct > 50)
    if 'Diabetes_Risk_Pct' in df_diabetes.columns:
        # Clean percentile strings like '99.0%' or '99.0'
        risk_scores = df_diabetes['Diabetes_Risk_Pct'].astype(str).str.replace('%', '').str.strip()
        risk_scores = pd.to_numeric(risk_scores, errors='coerce').fillna(0)
        df_diabetes['target'] = (risk_scores > 50).astype(int)
    else:
        # Fallback to Outcome if present
        df_diabetes['target'] = pd.to_numeric(df_diabetes.get('Outcome', 0), errors='coerce').fillna(0)
        
    features_diabetes = ['FBS_mg_dL', 'BMI', 'Age', 'SBP_mmHg', 'Insulin_uU_mL', 'HbA1c_pct', 'PPBS_mg_dL']
    X_diabetes = df_diabetes[features_diabetes]
    y_diabetes = df_diabetes['target']
    
    models_grid = {
        "RandomForest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [100],
                "max_depth": [5, 10, None]
            }
        }
    }
    
    best_diabetes = train_and_select_best(X_diabetes, y_diabetes, models_grid)
    
    with open(get_path('models/diabetes_model.pkl'), 'wb') as f:
        pickle.dump(best_diabetes, f)
    print(f"Saved {get_path('models/diabetes_model.pkl')}")

# ---------------------------------------------------------
# 2. HYPERTENSION MODEL
# ---------------------------------------------------------
print("\n" + "="*50)
print("2. TRAINING HYPERTENSION MODEL")
print("="*50)
hyper_path = 'datasets/hypertension_dataset.csv'
if os.path.exists(hyper_path):
    df_hyper = pd.read_csv(hyper_path)
    
    # Clinical headers: Age,Gender,SBP,DBP,BMI,Physical_Activity,Diet_PackagedFood,Smoking,Alcohol,Stress_Level,Sleep_Duration_hrs,Family_History_Hypertension,Diabetes_Status,LDL_Cholesterol,HDL_Cholesterol,Triglycerides,Hypertension_Risk
    if 'Hypertension_Risk' in df_hyper.columns:
        risk_scores = df_hyper['Hypertension_Risk'].astype(str).str.replace('%', '').str.strip()
        risk_scores = pd.to_numeric(risk_scores, errors='coerce').fillna(0)
        df_hyper['target'] = (risk_scores > 50).astype(int)
    else:
        df_hyper['target'] = pd.to_numeric(df_hyper.get('hypertension_target', 0), errors='coerce').fillna(0)
    
    features_hyper = ['SBP', 'DBP', 'BMI', 'Age', 'LDL_Cholesterol', 'HDL_Cholesterol', 'Triglycerides']
    X_hyper = df_hyper[features_hyper]
    y_hyper = df_hyper['target']
    
    models_grid = {
        "RandomForest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [100],
                "max_depth": [5, 10, 15]
            }
        }
    }
    
    best_hyper = train_and_select_best(X_hyper, y_hyper, models_grid)
    
    with open(get_path('models/hypertension_model.pkl'), 'wb') as f:
        pickle.dump(best_hyper, f)
    print(f"Saved {get_path('models/hypertension_model.pkl')}")

# ---------------------------------------------------------
# 3. HEART DISEASE MODEL
# ---------------------------------------------------------
print("\n" + "="*50)
print("3. TRAINING HEART DISEASE MODEL")
print("="*50)
heart_path = get_path('datasets/heart.csv')
if os.path.exists(heart_path):
    df_heart = pd.read_csv(heart_path)
    
    # Synthesize proxy target variables based on logic
    df_heart['diabetes_result'] = df_heart['fbs']
    df_heart['hypertension_result'] = np.where(df_heart['trestbps'] >= 140, 1, 0)
    
    # Feature Engineering
    df_heart['BP_category'] = df_heart.apply(lambda row: get_bp_category(row['trestbps'], 80), axis=1) # using 80 as arbitrary dia for scaling
    
    features_heart = [
        'age', 'cp', 'trestbps', 'chol', 'thalach', 'oldpeak', 'exang',
        'diabetes_result', 'hypertension_result', 'BP_category'
    ]
    X_heart = df_heart[features_heart]
    y_heart = df_heart['target']
    
    models_grid = {
        "RandomForest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [50, 100],
                "max_depth": [5, 10]
            }
        },
        "GradientBoosting": {
            "model": GradientBoostingClassifier(random_state=42),
            "params": {
                "n_estimators": [50, 100],
                "learning_rate": [0.05, 0.1, 0.2]
            }
        }
    }
    
    best_heart = train_and_select_best(X_heart, y_heart, models_grid)
    
    with open(get_path('models/heart_model.pkl'), 'wb') as f:
        pickle.dump(best_heart, f)
    print(f"Saved {get_path('models/heart_model.pkl')}")

# ---------------------------------------------------------
# 4. BREAST CANCER MODEL
# ---------------------------------------------------------
print("\n" + "="*50)
print("4. TRAINING BREAST CANCER MODEL")
print("="*50)
breast_path = get_path('datasets/data.csv')
if os.path.exists(breast_path):
    df_bc = pd.read_csv(breast_path)
    
    # Target Encoding: Malignant (M) -> 1, Benign (B) -> 0
    df_bc['target'] = np.where(df_bc['diagnosis'] == 'M', 1, 0)
    
    # Selected Features matching user requirements
    features_bc = [
        'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
        'smoothness_mean', 'compactness_mean', 'concavity_mean', 
        'symmetry_mean', 'fractal_dimension_mean'
    ]
    
    X_bc = df_bc[features_bc]
    y_bc = df_bc['target']
    
    models_grid_bc = {
        "RandomForest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [50, 100],
                "max_depth": [5, 10, None]
            }
        },
        "LogisticRegression": {
            "model": LogisticRegression(max_iter=1000),
            "params": {
                "C": [0.1, 1, 10]
            }
        }
    }
    
    best_bc = train_and_select_best(X_bc, y_bc, models_grid_bc)
    
    with open(get_path('models/breast_cancer_model.pkl'), 'wb') as f:
        pickle.dump(best_bc, f)
    print(f"Saved {get_path('models/breast_cancer_model.pkl')}")

# ---------------------------------------------------------
# 5. LUNG CANCER MODEL
# ---------------------------------------------------------
print("\n" + "="*50)
print("5. TRAINING LUNG CANCER MODEL")
print("="*50)
lung_path = get_path('datasets/lung_cancer_dataset.csv')
if os.path.exists(lung_path):
    df_lung = pd.read_csv(lung_path)
    
    # Headers: Gender,Age,Smoking,Yellow_Fingers,CEA_ng_mL,Hemoglobin_g_dL,WBC_Count_10e3_uL,Family_History_Cancer,Chronic_Disease,Fatigue,Allergy,Wheezing,Alcohol_Consumption,Coughing,Shortness_of_Breath,Swallowing_Difficulty,Chest_Pain,Occupational_Exposure_Risk,LUNG_CANCER_RISK
    if 'LUNG_CANCER_RISK' in df_lung.columns:
        risk_scores = df_lung['LUNG_CANCER_RISK'].astype(str).str.replace('%', '').str.strip()
        risk_scores = pd.to_numeric(risk_scores, errors='coerce').fillna(0)
        df_lung['target'] = (risk_scores > 50).astype(int)
    else:
        df_lung['target'] = pd.to_numeric(df_lung.get('LUNG_CANCER', 0), errors='coerce').fillna(0)
    
    # Use headers matching actual dataset
    features_lung = ['Age', 'Smoking', 'Alcohol_Consumption', 'Coughing', 'Chest_Pain', 'Fatigue', 'Shortness_of_Breath']
    
    # Encode categorical strings to numeric
    for col in features_lung:
        if df_lung[col].dtype == 'object':
            df_lung[col] = df_lung[col].apply(map_categorical)
    
    X_lung = df_lung[features_lung]
    y_lung = df_lung['target']
    
    models_grid_lung = {
        "RandomForest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [100],
                "max_depth": [5, 10]
            }
        }
    }
    
    best_lung = train_and_select_best(X_lung, y_lung, models_grid_lung)
    
    with open('models/lung_cancer_model.pkl', 'wb') as f:
        pickle.dump(best_lung, f)
    print("Saved lung_cancer_model.pkl")

print("\nModel upgrade and tuning sequence strictly completed.")
