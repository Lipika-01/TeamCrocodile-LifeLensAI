from fastapi import APIRouter, File, UploadFile, Depends
from pydantic import BaseModel
import os
import shutil

from services.predictor import predictor
from services.pdf_parser import parse_medical_pdf
from services.recommendations import analyze_values, generate_reasoning, generate_recommendations, generate_combined_analysis, generate_doctor_report
from core.database import records_collection
from routes.auth import get_current_user

router = APIRouter()

class DiabetesInput(BaseModel):
    Age: int
    BMI: float
    FBS_mg_dL: float
    PPBS_mg_dL: float
    HbA1c_pct: float
    SBP_mmHg: int
    DBP_mmHg: int
    Insulin_uU_mL: float
    Physical_Activity_Score: int
    Family_History: int
    LDL_mg_dL: float
    HDL_mg_dL: float
    Triglycerides_mg_dL: float
    Smoking: int
    Alcohol: int

class HypertensionInput(BaseModel):
    Age: int
    Gender: str
    SBP: int
    DBP: int
    BMI: float
    Physical_Activity: str
    Diet_PackagedFood: str
    Smoking: str
    Alcohol: str
    Stress_Level: str
    Sleep_Duration_hrs: float
    Family_History_Hypertension: str
    Diabetes_Status: str
    LDL_Cholesterol: float
    HDL_Cholesterol: float
    Triglycerides: float

class LungCancerInput(BaseModel):
    Gender: str
    Age: int
    Smoking: str
    Yellow_Fingers: str
    CEA_ng_mL: float
    Hemoglobin_g_dL: float
    WBC_Count_10e3_uL: float
    Family_History_Cancer: str
    Chronic_Disease: str
    Fatigue: str
    Allergy: str
    Wheezing: str
    Alcohol_Consumption: str
    Coughing: str
    Shortness_of_Breath: str
    Swallowing_Difficulty: str
    Chest_Pain: str
    Occupational_Exposure_Risk: str


class BreastCancerInput(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float

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

@router.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    extracted_data = parse_medical_pdf(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return {"status": "success", "data": extracted_data}

@router.get("/user/records")
async def get_user_records(current_user: dict = Depends(get_current_user)):
    # Retrieve all previous module predictions to enable Auto-Fill
    record = records_collection.find_one({"user_id": current_user["_id"]}, {"_id": 0})
    if not record:
        return {"status": "success", "data": {}}
    return {"status": "success", "data": record}

def compile_doctor_report(predict_results, data):
    analysis = analyze_values(data)
    reasoning = generate_reasoning(predict_results, data)
    combined_warnings = generate_combined_analysis(predict_results)
    recs = generate_recommendations(predict_results, data)
    doc_report = generate_doctor_report(predict_results, data)

    return {
        "predictions": predict_results,
        "analysis": analysis,
        "reasoning": reasoning,
        "recommendations": recs,
        "combined_warnings": combined_warnings,
        "doctor_report": doc_report
    }

import pandas as pd

@router.post("/predict/diabetes")
async def predict_diabetes(data: DiabetesInput, current_user: dict = Depends(get_current_user)):
    input_data = data.dict()
    result = predictor.predict_diabetes(input_data)
    if "error" in result: return {"status": "error", "message": result["error"]}
    
    predict_results = {"diabetes": result}
    input_data = data.dict()
    report = compile_doctor_report(predict_results, input_data)
    report["ml_metadata"] = result
    
    records_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"diabetes": {"inputs": input_data, "result": result}}},
        upsert=True
    )
    
    return {"status": "success", "report": report}

@router.post("/predict/hypertension")
async def predict_hypertension(data: HypertensionInput, current_user: dict = Depends(get_current_user)):
    input_data = data.dict()
    result = predictor.predict_hypertension(input_data)
    if "error" in result: return {"status": "error", "message": result["error"]}
    
    predict_results = {"hypertension": result}
    input_data = data.dict()
    report = compile_doctor_report(predict_results, input_data)
    report["ml_metadata"] = result
    
    records_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"hypertension": {"inputs": input_data, "result": result}}},
        upsert=True
    )
    
    return {"status": "success", "report": report}

@router.post("/predict/heart")
async def predict_heart(data: HeartDiseaseInput, current_user: dict = Depends(get_current_user)):
    result = predictor.predict_heart_disease(
        data.age, data.cp, data.trestbps, data.chol, data.thalach,
        data.oldpeak, data.exang, data.diabetes_result, data.hypertension_result
    )
    
    predict_results = {"heart": result}
    input_data = data.dict()
    report = compile_doctor_report(predict_results, input_data)
    
    records_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"heart_disease": {"inputs": input_data, "result": result}}},
        upsert=True
    )
    
    return {"status": "success", "report": report}

@router.post("/predict/breast-cancer")
async def predict_breast_cancer(data: BreastCancerInput, current_user: dict = Depends(get_current_user)):
    result = predictor.predict_breast_cancer(
        data.radius_mean, data.texture_mean, data.perimeter_mean, data.area_mean, 
        data.smoothness_mean, data.compactness_mean, data.concavity_mean, 
        data.symmetry_mean, data.fractal_dimension_mean
    )
    
    predict_results = {"breast_cancer": result}
    input_data = data.dict()
    report = compile_doctor_report(predict_results, input_data)
    
    records_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"breast_cancer": {"inputs": input_data, "result": result}}},
        upsert=True
    )
    
    return {"status": "success", "report": report}

@router.post("/predict/lung-cancer")
async def predict_lung_cancer(data: LungCancerInput, current_user: dict = Depends(get_current_user)):
    input_data = data.dict()
    result = predictor.predict_lung_cancer(input_data)
    if "error" in result: return {"status": "error", "message": result["error"]}
    
    predict_results = {"lung_cancer": result}
    input_data = data.dict()
    report = compile_doctor_report(predict_results, input_data)
    report["ml_metadata"] = result
    
    records_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"lung_cancer": {"inputs": input_data, "result": result}}},
        upsert=True
    )
    
    return {"status": "success", "report": report}
