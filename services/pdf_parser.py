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
        print(f"Failed to read PDF: {e}")
        return {}

    extracted_data = {}
    
    # Simple regex patterns tailored for basic medical reports
    # Age pattern (e.g., Age: 45 or Age 45)
    age_match = re.search(r'(?i)age\s*[:\-]?\s*(\d{1,3})', text)
    if age_match:
        extracted_data['age'] = int(age_match.group(1))

    # BMI pattern
    bmi_match = re.search(r'(?i)bmi\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)', text)
    if bmi_match:
        extracted_data['bmi'] = float(bmi_match.group(1))

    # Glucose pattern
    glucose_match = re.search(r'(?i)glucose\s*[:\-]?\s*(\d{2,3}(?:\.\d+)?)', text)
    if glucose_match:
        extracted_data['glucose'] = float(glucose_match.group(1))

    # Blood Pressure pattern (e.g., 120/80 or 120 / 80 or BP: 120/80)
    bp_match = re.search(r'(?i)(?:bp|blood pressure)\s*[:\-]?\s*(\d{2,3})\s*/\s*(\d{2,3})', text)
    if not bp_match:
        # Fallback to just finding X/Y format assuming it's BP
        bp_match = re.search(r'\b(\d{2,3})\s*/\s*(\d{2,3})\b', text)
        
    if bp_match:
        extracted_data['ap_hi'] = int(bp_match.group(1))
        extracted_data['ap_lo'] = int(bp_match.group(2))

    return extracted_data
