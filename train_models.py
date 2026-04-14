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

os.makedirs('models', exist_ok=True)

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
diabetes_path = 'datasets/diabetes.csv'
if os.path.exists(diabetes_path):
    df_diabetes = pd.read_csv(diabetes_path)
    
    cols_with_zeros = ['Glucose', 'BloodPressure', 'BMI', 'Insulin']
    for col in cols_with_zeros:
        df_diabetes[col] = df_diabetes[col].replace(0, np.nan)
        df_diabetes[col] = df_diabetes[col].fillna(df_diabetes[col].median())
        
    # Feature Engineering
    df_diabetes['BP_category'] = df_diabetes.apply(lambda row: get_bp_category(row['BloodPressure'], 80), axis=1) # assuming dia roughly 80 if sys is row bp
    df_diabetes['BMI_category'] = df_diabetes['BMI'].apply(get_bmi_category)
    df_diabetes['Glucose_category'] = df_diabetes['Glucose'].apply(get_glucose_category)
    
    features_diabetes = ['Glucose', 'BMI', 'Age', 'BloodPressure', 'Insulin', 'BP_category', 'BMI_category', 'Glucose_category']
    X_diabetes = df_diabetes[features_diabetes]
    y_diabetes = df_diabetes['Outcome']
    
    models_grid = {
        "LogisticRegression": {
            "model": LogisticRegression(max_iter=1000),
            "params": {
                "C": [0.1, 1, 10]
            }
        },
        "RandomForest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [50, 100],
                "max_depth": [5, 10, None]
            }
        }
    }
    
    best_diabetes = train_and_select_best(X_diabetes, y_diabetes, models_grid)
    
    with open('models/diabetes_model.pkl', 'wb') as f:
        pickle.dump(best_diabetes, f)
    print("Saved diabetes_model.pkl")

# ---------------------------------------------------------
# 2. HYPERTENSION MODEL
# ---------------------------------------------------------
print("\n" + "="*50)
print("2. TRAINING HYPERTENSION MODEL")
print("="*50)
hyper_path = 'datasets/clean_hypertension.csv'
if os.path.exists(hyper_path):
    df_hyper = pd.read_csv(hyper_path)
    
    # Remove unrealistic BP
    df_hyper = df_hyper[(df_hyper['ap_hi'] < 300) & (df_hyper['ap_hi'] > 40)]
    df_hyper = df_hyper[(df_hyper['ap_lo'] < 200) & (df_hyper['ap_lo'] > 20)]
    
    # Feature Engineering
    df_hyper['BP_category'] = df_hyper.apply(lambda row: get_bp_category(row['ap_hi'], row['ap_lo']), axis=1)
    df_hyper['BMI_category'] = df_hyper['BMI'].apply(get_bmi_category)
    df_hyper['hypertension_target'] = np.where((df_hyper['ap_hi'] >= 140) | (df_hyper['ap_lo'] >= 90), 1, 0)
    
    # To speed up GridSearchCV on a potentially huge dataset (68k rows), take a sample if needed,
    # but we will try running on full. If slow, we'd sample.
    # Take a 10k random sample for faster hyperparameter searching (optional but practical)
    df_hyper = df_hyper.sample(n=min(15000, len(df_hyper)), random_state=42)
    
    features_hyper = ['ap_hi', 'ap_lo', 'BMI', 'age', 'cholesterol', 'BP_category', 'BMI_category']
    X_hyper = df_hyper[features_hyper]
    y_hyper = df_hyper['hypertension_target']
    
    models_grid = {
        "RandomForest": {
            "model": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [50, 100],
                "max_depth": [5, 10, 15]
            }
        },
        "GradientBoosting": {
            "model": GradientBoostingClassifier(random_state=42),
            "params": {
                "n_estimators": [50, 100],
                "learning_rate": [0.05, 0.1]
            }
        }
    }
    
    best_hyper = train_and_select_best(X_hyper, y_hyper, models_grid)
    
    with open('models/hypertension_model.pkl', 'wb') as f:
        pickle.dump(best_hyper, f)
    print("Saved hypertension_model.pkl")

# ---------------------------------------------------------
# 3. HEART DISEASE MODEL
# ---------------------------------------------------------
print("\n" + "="*50)
print("3. TRAINING HEART DISEASE MODEL")
print("="*50)
heart_path = 'datasets/heart.csv'
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
    
    with open('models/heart_model.pkl', 'wb') as f:
        pickle.dump(best_heart, f)
    print("Saved heart_model.pkl")

print("\nModel upgrade and tuning sequence strictly completed.")
