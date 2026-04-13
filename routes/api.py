from fastapi import APIRouter, File, UploadFile, Request
from pydantic import BaseModel
import os
import shutil
from services.predictor import predictor
from services.pdf_parser import parse_medical_pdf
from services.recommendations import analyze_values, generate_insights, generate_recommendations, generate_combined_analysis

router = APIRouter()

# Schema definitions
class DiabetesInput(BaseModel):
    glucose: float
    bmi: float
    age: int
    blood_pressure: float
    insulin: float

class HypertensionInput(BaseModel):
    ap_hi: float
    ap_lo: float
    bmi: float
    age: int
    cholesterol: float

class HeartDiseaseInput(BaseModel):
    age: int
    cp: int
    trestbps: float
    chol: float
    thalach: float
    oldpeak: float
    exang: int
    diabetes_result: int
    hypertension_result: int

class AllPredictInput(BaseModel):
    # Shared Features
    age: int
    bmi: float
    glucose: float
    insulin: float
    ap_hi: float
    ap_lo: float
    cholesterol: float
    cp: int
    thalach: float
    oldpeak: float
    exang: int

@router.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    # Save the file temporarily
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    extracted_data = parse_medical_pdf(file_path)
    
    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return {"status": "success", "data": extracted_data}

@router.post("/predict/diabetes")
async def predict_diabetes(data: DiabetesInput):
    result = predictor.predict_diabetes(
        data.glucose, data.bmi, data.age, data.blood_pressure, data.insulin
    )
    return {"status": "success", "result": result}

@router.post("/predict/hypertension")
async def predict_hypertension(data: HypertensionInput):
    result = predictor.predict_hypertension(
        data.ap_hi, data.ap_lo, data.bmi, data.age, data.cholesterol
    )
    return {"status": "success", "result": result}

@router.post("/predict/heart")
async def predict_heart(data: HeartDiseaseInput):
    result = predictor.predict_heart_disease(
        data.age, data.cp, data.trestbps, data.chol, data.thalach,
        data.oldpeak, data.exang, data.diabetes_result, data.hypertension_result
    )
    return {"status": "success", "result": result}

@router.post("/predict/all")
async def predict_all(data: AllPredictInput):
    # Predict Diabetes
    diab_res = predictor.predict_diabetes(
        data.glucose, data.bmi, data.age, data.ap_hi, data.insulin # Using ap_hi as BP for diabetes loosely
    )
    
    # Predict Hypertension
    hyper_res = predictor.predict_hypertension(
        data.ap_hi, data.ap_lo, data.bmi, data.age, data.cholesterol
    )
    
    # Predict Heart
    diab_val = diab_res['prediction'] if diab_res else 0
    hyper_val = hyper_res['prediction'] if hyper_res else 0

    heart_res = predictor.predict_heart_disease(
        data.age, data.cp, data.ap_hi, data.cholesterol, data.thalach,
        data.oldpeak, data.exang, diab_val, hyper_val
    )
    
    predict_results = {
        "diabetes": diab_res,
        "hypertension": hyper_res,
        "heart": heart_res
    }
    
    # Generate insights and recommendations
    input_data = data.dict()
    analysis = analyze_values(input_data)
    insights = generate_insights(predict_results, input_data)
    combined_warnings = generate_combined_analysis(predict_results)
    
    # Using generic function from recommendations.py directly here
    # (Assuming generate_recommendations might use it)
    has_diabetes = diab_val == 1
    has_hyper = hyper_val == 1
    has_heart = heart_res['prediction'] == 1 if heart_res else False
    
    # Simple direct builder
    recs = {
        "diet": ["Maintain a balanced diet rich in leafy greens, lean proteins, and whole grains."],
        "exercise": ["Aim for 150 minutes of moderate aerobic activity every week."],
        "medicine": ["Always consult a doctor before taking any long-term medication."],
        "vitamins": ["Vitamin D (1000-2000 IU/day)", "Vitamin B12", "Omega-3 Fatty Acids (Fish Oil)"],
        "preventive": ["Annual comprehensive health checkup", "Maintain a healthy sleep schedule of 7-8 hours"]
    }
    
    if has_diabetes:
        recs["diet"].extend(["Strictly avoid refined sugars and high-glycemic foods.", "Incorporate complex carbohydrates."])
        recs["preventive"].append("Monitor your fasting blood sugar weekly.")
        recs["medicine"].append("Metformin is a commonly prescribed drug (Consult physician).")
        
    if has_hyper:
        recs["diet"].append("Follow the DASH diet. Reduce sodium intake.")
        recs["exercise"].append("Engage in daily brisk walking to improve vascular health.")
        recs["medicine"].append("ACE inhibitors are common for BP control.")
        
    if has_heart:
        recs["diet"].append("Avoid saturated and trans fats to manage cholesterol.")
        recs["vitamins"].append("CoQ10 supplements might be beneficial for heart health.")
        recs["medicine"].append("Statins or beta-blockers might be prescribed.")

    return {
        "status": "success",
        "predictions": predict_results,
        "analysis": analysis,
        "insights": insights,
        "recommendations": recs,
        "combined_warnings": combined_warnings
    }
