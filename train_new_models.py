import pandas as pd
import numpy as np
import pickle
import os
import warnings
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

warnings.filterwarnings('ignore')
os.makedirs('models', exist_ok=True)

def evaluate_model(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    print(f"--- {name} Evaluation ---")
    print(f"Accuracy:  {acc:.4f}\nPrecision: {prec:.4f}\nRecall:    {rec:.4f}\nF1 Score:  {f1:.4f}\n")
    return acc

def convert_risk_target(risk_series, threshold=50.0):
    """Converts a continuous risk target (e.g. '85%' or 85.0) to a binary classification target."""
    if risk_series.dtype == 'object':
        risk_series = risk_series.str.replace('%', '').astype(float)
    return np.where(risk_series >= threshold, 1, 0)

# =========================================================
# 1. DIABETES MODEL PIPELINE
# =========================================================
print("="*50 + "\n1. TRAINING DIABETES MODEL\n" + "="*50)
if os.path.exists('datasets/diabetes_synthetic_dataset.csv'):
    df_diabetes = pd.read_csv('datasets/diabetes_synthetic_dataset.csv')
    
    # Preprocessing
    target_col = 'Diabetes_Risk_Pct'
    y_diab = convert_risk_target(df_diabetes[target_col], 50.0)
    X_diab = df_diabetes.drop(columns=[target_col])
    
    # Impute missing numeric values natively if present
    imputer_diab = SimpleImputer(strategy='median')
    X_diab_imputed = imputer_diab.fit_transform(X_diab)
    
    scaler_diab = StandardScaler()
    X_diab_scaled = scaler_diab.fit_transform(X_diab_imputed)
    
    X_train, X_test, y_train, y_test = train_test_split(X_diab_scaled, y_diab, test_size=0.2, random_state=42, stratify=y_diab)
    
    # Model Tuning
    rf_diab = RandomForestClassifier(random_state=42)
    grid_diab = GridSearchCV(rf_diab, {'n_estimators': [50, 100], 'max_depth': [5, 10, None]}, cv=5, scoring='accuracy', n_jobs=-1)
    grid_diab.fit(X_train, y_train)
    
    best_diab = grid_diab.best_estimator_
    print(f"Best Diabetes Params: {grid_diab.best_params_}")
    
    test_acc = evaluate_model("RandomForest (Diabetes)", y_test, best_diab.predict(X_test))
    best_diab.model_accuracy = round(test_acc * 100, 2)
    
    with open('models/diabetes_model.pkl', 'wb') as f: pickle.dump(best_diab, f)
    with open('models/diabetes_scaler.pkl', 'wb') as f: pickle.dump(scaler_diab, f)
    with open('models/diabetes_imputer.pkl', 'wb') as f: pickle.dump(imputer_diab, f)
    print("-> Saved Diabetes assets.\n")


# =========================================================
# 2. HYPERTENSION MODEL PIPELINE
# =========================================================
print("="*50 + "\n2. TRAINING HYPERTENSION MODEL\n" + "="*50)
if os.path.exists('datasets/hypertension_dataset.csv'):
    df_hyper = pd.read_csv('datasets/hypertension_dataset.csv')
    
    target_col = 'Hypertension_Risk'
    y_hyper = convert_risk_target(df_hyper[target_col], 50.0)
    X_hyper = df_hyper.drop(columns=[target_col])
    
    # Encode categoricals dynamically
    cat_cols = X_hyper.select_dtypes(include=['object']).columns
    encoders_hyper = {}
    
    for col in cat_cols:
        le = LabelEncoder()
        # Impute missing categorical with mode before encoding
        mode_val = X_hyper[col].mode()[0]
        X_hyper[col] = X_hyper[col].fillna(mode_val)
        X_hyper[col] = le.fit_transform(X_hyper[col])
        encoders_hyper[col] = le
        
    num_cols = X_hyper.select_dtypes(exclude=['object']).columns
    imputer_hyper = SimpleImputer(strategy='median')
    X_hyper[num_cols] = imputer_hyper.fit_transform(X_hyper[num_cols])
    
    scaler_hyper = StandardScaler()
    X_hyper_scaled = scaler_hyper.fit_transform(X_hyper)
    
    X_train, X_test, y_train, y_test = train_test_split(X_hyper_scaled, y_hyper, test_size=0.2, random_state=42, stratify=y_hyper)

    rf_hyper = RandomForestClassifier(random_state=42)
    grid_hyper = GridSearchCV(rf_hyper, {'n_estimators': [50, 100, 150], 'max_depth': [5, 10, 15]}, cv=5, scoring='accuracy', n_jobs=-1)
    grid_hyper.fit(X_train, y_train)
    
    best_hyper = grid_hyper.best_estimator_
    print(f"Best Hypertension Params: {grid_hyper.best_params_}")
    
    test_acc = evaluate_model("RandomForest (Hypertension)", y_test, best_hyper.predict(X_test))
    best_hyper.model_accuracy = round(test_acc * 100, 2)
    
    with open('models/hypertension_model.pkl', 'wb') as f: pickle.dump(best_hyper, f)
    with open('models/hypertension_scaler.pkl', 'wb') as f: pickle.dump(scaler_hyper, f)
    with open('models/hypertension_imputer.pkl', 'wb') as f: pickle.dump(imputer_hyper, f)
    with open('models/hypertension_encoders.pkl', 'wb') as f: pickle.dump(encoders_hyper, f)
    print("-> Saved Hypertension assets.\n")


# =========================================================
# 3. LUNG CANCER MODEL PIPELINE
# =========================================================
print("="*50 + "\n3. TRAINING LUNG CANCER MODEL\n" + "="*50)
if os.path.exists('datasets/lung_cancer_dataset.csv'):
    df_lung = pd.read_csv('datasets/lung_cancer_dataset.csv')
    
    target_col = 'LUNG_CANCER_RISK'
    y_lung = convert_risk_target(df_lung[target_col], 50.0)
    X_lung = df_lung.drop(columns=[target_col])
    
    cat_cols = X_lung.select_dtypes(include=['object']).columns
    encoders_lung = {}
    
    for col in cat_cols:
        le = LabelEncoder()
        mode_val = X_lung[col].mode()[0]
        X_lung[col] = X_lung[col].fillna(mode_val)
        X_lung[col] = le.fit_transform(X_lung[col])
        encoders_lung[col] = le
        
    num_cols = X_lung.select_dtypes(exclude=['object']).columns
    imputer_lung = SimpleImputer(strategy='median')
    X_lung[num_cols] = imputer_lung.fit_transform(X_lung[num_cols])
    
    scaler_lung = StandardScaler()
    X_lung_scaled = scaler_lung.fit_transform(X_lung)
    
    X_train, X_test, y_train, y_test = train_test_split(X_lung_scaled, y_lung, test_size=0.2, random_state=42, stratify=y_lung)

    rf_lung = RandomForestClassifier(random_state=42)
    grid_lung = GridSearchCV(rf_lung, {'n_estimators': [50, 100], 'max_depth': [5, 10, None]}, cv=5, scoring='accuracy', n_jobs=-1)
    grid_lung.fit(X_train, y_train)
    
    best_lung = grid_lung.best_estimator_
    print(f"Best Lung Cancer Params: {grid_lung.best_params_}")
    
    test_acc = evaluate_model("RandomForest (Lung Cancer)", y_test, best_lung.predict(X_test))
    best_lung.model_accuracy = round(test_acc * 100, 2)
    
    with open('models/lung_cancer_model.pkl', 'wb') as f: pickle.dump(best_lung, f)
    with open('models/lung_cancer_scaler.pkl', 'wb') as f: pickle.dump(scaler_lung, f)
    with open('models/lung_cancer_imputer.pkl', 'wb') as f: pickle.dump(imputer_lung, f)
    with open('models/lung_cancer_encoders.pkl', 'wb') as f: pickle.dump(encoders_lung, f)
    print("-> Saved Lung Cancer assets.\n")

print(">>> ALL PIPELINES REBUILT STRONGLY. SUMMARY METRICS COMPLETED.")
