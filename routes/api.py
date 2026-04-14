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

@router.post("/predict/diabetes")
async def predict_diabetes(data: DiabetesInput, current_user: dict = Depends(get_current_user)):
    result = predictor.predict_diabetes(
        data.glucose, data.bmi, data.age, data.blood_pressure, data.insulin
    )
    
    predict_results = {"diabetes": result}
    input_data = data.dict()
    report = compile_doctor_report(predict_results, input_data)
    
    # Save to MongoDB
    records_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"diabetes": {"inputs": input_data, "result": result}}},
        upsert=True
    )
    
    return {"status": "success", "report": report}

@router.post("/predict/hypertension")
async def predict_hypertension(data: HypertensionInput, current_user: dict = Depends(get_current_user)):
    result = predictor.predict_hypertension(
        data.ap_hi, data.ap_lo, data.bmi, data.age, data.cholesterol
    )
    
    predict_results = {"hypertension": result}
    input_data = data.dict()
    report = compile_doctor_report(predict_results, input_data)
    
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
