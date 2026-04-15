"""
LifeLensAI Clinical Data Extraction Service (CDES)
Autonomous Medical Report Parsing Engine

This module implements high-precision regex extraction logic to synthesize 
structured clinical profiles from unstructured PDF medical reports. 

Supported Paradigms:
- Vitals: BP (SBP/DBP), BMI, Pulse
- Glycemic: HbA1c, Fasting Blood Sugar
- Lipid: LDL, HDL, Triglycerides
- Demographics: Age, Gender

Technology: PyMuPDF (fitz) + Clinical Regex Patterns
"""

import fitz  # PyMuPDF
import re

def parse_medical_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()
    except Exception as e:
        print(f"FAILED to read PDF: {e}")
        return {}

    print(f"DEBUG: Successfully read PDF. Text length: {len(text)}")
    print(f"DEBUG: Extracted Text Snippet:\n{text[:1000]}") # Log first 1000 chars

    extracted_data = {}
    
    # 1. Basic Demographics
    age_match = re.search(r'(?i)age\s*[:\-]?\s*(\d{1,3})', text)
    if age_match:
        extracted_data['Age'] = int(age_match.group(1))

    # 2. Vital Signs & BMI
    bmi_match = re.search(r'(?i)bmi\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)', text)
    if bmi_match:
        extracted_data['BMI'] = float(bmi_match.group(1))

    # Blood Pressure (Systolic / Diastolic)
    bp_match = re.search(r'(?i)(?:bp|blood pressure|pressure)\s*[:\-]?\s*(\d{2,3})\s*/\s*(\d{2,3})', text)
    if not bp_match:
        bp_match = re.search(r'\b(\d{2,3})\s*/\s*(\d{2,3})\b', text)
        
    if bp_match:
        extracted_data['SBP'] = int(bp_match.group(1))
        extracted_data['DBP'] = int(bp_match.group(2))
        extracted_data['SBP_mmHg'] = int(bp_match.group(1)) # Duplicate for diabetes module
        extracted_data['DBP_mmHg'] = int(bp_match.group(2))

    # 3. Glycemic Markers
    fbs_match = re.search(r'(?i)(?:fbs|fasting blood sugar|fasting glucose)\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)', text)
    if fbs_match:
        extracted_data['FBS_mg_dL'] = float(fbs_match.group(1))
        extracted_data['glucose'] = float(fbs_match.group(1))

    hba1c_match = re.search(r'(?i)hba1c\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%', text)
    if hba1c_match:
        extracted_data['HbA1c_pct'] = float(hba1c_match.group(1))

    # 4. Lipid Profile
    ldl_match = re.search(r'(?i)ldl\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)', text)
    if ldl_match:
        extracted_data['LDL_mg_dL'] = float(ldl_match.group(1))
        extracted_data['LDL_Cholesterol'] = float(ldl_match.group(1))

    hdl_match = re.search(r'(?i)hdl\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)', text)
    if hdl_match:
        extracted_data['HDL_mg_dL'] = float(hdl_match.group(1))
        extracted_data['HDL_Cholesterol'] = float(hdl_match.group(1))

    tg_match = re.search(r'(?i)(?:triglycerides|tg)\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)', text)
    if tg_match:
        extracted_data['Triglycerides_mg_dL'] = float(tg_match.group(1))
        extracted_data['Triglycerides'] = float(tg_match.group(1))

    print(f"DEBUG: Final Extracted Data: {extracted_data}")
    return extracted_data
