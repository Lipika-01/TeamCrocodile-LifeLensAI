import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY and "PASTE_YOUR_GEMINI" not in GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    GEMINI_ENABLED = True
else:
    GEMINI_ENABLED = False

def analyze_values(data):
    analysis = []
    # Glucose Interpretation
    if 'glucose' in data:
        gl = data['glucose']
        if gl < 70:
            analysis.append({"name": "Glucose", "status": "Low (Hypoglycemic)", "value": gl, "warning": True})
        elif gl <= 125:
            analysis.append({"name": "Glucose", "status": "Normal", "value": gl, "warning": False})
        elif gl < 140:
            analysis.append({"name": "Glucose", "status": "Elevated (Pre-Diabetic)", "value": gl, "warning": True})
        else:
            analysis.append({"name": "Glucose", "status": "High (Diabetic Range)", "value": gl, "warning": True})
            
    # BMI Interpretation
    if 'bmi' in data:
        bmi = data['bmi']
        if bmi < 18.5:
            analysis.append({"name": "BMI", "status": "Underweight", "value": bmi, "warning": True})
        elif bmi <= 25:
            analysis.append({"name": "BMI", "status": "Normal", "value": bmi, "warning": False})
        elif bmi <= 30:
            analysis.append({"name": "BMI", "status": "Overweight", "value": bmi, "warning": True})
        else:
            analysis.append({"name": "BMI", "status": "Obese", "value": bmi, "warning": True})
            
    # BP Interpretation
    if 'ap_hi' in data and 'ap_lo' in data:
        sys = data['ap_hi']
        dia = data['ap_lo']
        if sys < 120 and dia < 80:
            analysis.append({"name": "Blood Pressure", "status": "Normal", "value": f"{sys}/{dia}", "warning": False})
        elif sys < 130 and dia < 80:
            analysis.append({"name": "Blood Pressure", "status": "Elevated", "value": f"{sys}/{dia}", "warning": True})
        elif sys >= 140 or dia >= 90:
            analysis.append({"name": "Blood Pressure", "status": "High (Stage 2)", "value": f"{sys}/{dia}", "warning": True})
        else:
            analysis.append({"name": "Blood Pressure", "status": "High (Stage 1)", "value": f"{sys}/{dia}", "warning": True})
            
    return analysis

def get_recommendations_from_gemini(predict_results, data):
    """Attempt to get dynamic medical insights from Gemini."""
    prompt = f"""
    You are a world-class AI Healthcare Assistant UI content generator.
    Based on the following patient data and AI predictions, generate a structured, professional, and non-prescriptive health intelligence report.
    
    PATIENT DATA:
    {json.dumps(data, indent=2)}
    
    AI PREDICTIONS (Probability and Risk Level):
    {json.dumps(predict_results, indent=2)}
    
    OUTPUT FORMAT (Strict JSON):
    {{
      "medical_summary": "Intelligent overview of condition and primary risk drivers.",
      "daily_routine": ["Step-by-step morning-to-evening schedule"],
      "monitoring_plan": ["Specific metrics to track and thresholds"],
      "physical_activity": ["Recommended exercises based on risk level"],
      "diet_configuration": ["Breakfast/Lunch/Dinner breakdown, foods to avoid"],
      "supplements": ["Safe, non-prescriptive vitamin/supplement suggestions"],
      "medicinal_guidance": ["NON-PRESCRIPTIVE informational guidance only"]
    }}
    
    RULES:
    1. Professional, empathetic tone.
    2. NO direct drug dosages. Always say "Consult physician".
    3. Ensure routine includes hydration and sleep.
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean potential markdown from response
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

def generate_reasoning(predict_results, data):
    # Keep the logic for reasoning as it's useful for the summary card
    reasoning = {}
    for module, result in predict_results.items():
        if result and result.get('risk_level') in ['Medium', 'High']:
            reasoning[module] = f"Risk triggered by abnormal physiological patterns detected in {module} parameters."
        else:
            reasoning[module] = "Metrics remain within clinical safety thresholds for this module."
    return reasoning

def get_fallback_recommendations(predict_results, data):
    """Robust rule-based fallback if Gemini is disabled or fails."""
    max_risk = 'Low'
    for v in predict_results.values():
        if v and v.get('risk_level') == 'High': max_risk = 'High'; break
        elif v and v.get('risk_level') == 'Medium': max_risk = 'Medium'

    # Baseline logic
    if max_risk == 'High':
        return {
            "medical_summary": "Clinical indicators suggest significant metabolic or cardiovascular strain requiring immediate professional review.",
            "daily_routine": ["07:00 AM - Fasting vitals check", "08:00 AM - High-fiber breakfast", "01:00 PM - Lean protein lunch", "06:00 PM - Supervised light walking", "10:00 PM - Optimized rest"],
            "monitoring_plan": ["Daily Blood Pressure (Target: <130/80)", "Daily Fasting Glucose (Target: <100 mg/dL)", "Bi-weekly weights"],
            "physical_activity": ["Monitored light walking (15 min)", "Postural yoga", "Avoid high-intensity cardio"],
            "diet_configuration": ["Zero refined sugar", "Restrict sodium to <1500mg/day", "Focus on leafy greens and omega-rich nuts"],
            "supplements": ["Vitamin D (1000-2000 IU)", "Omega-3 Fatty Acids", "CoQ10 (Consult doctor)"],
            "medicinal_guidance": ["Consult cardiologist regarding lipid-lowering therapies (Statins)", "Do not alter existing medication without professional advice"]
        }
    elif max_risk == 'Medium':
        return {
            "medical_summary": "Your profile shows elevated markers that indicate a transition towards metabolic instability.",
            "daily_routine": ["07:30 AM - Hydration & Light Stretching", "08:30 AM - Whole grain breakfast", "07:00 PM - 30 min brisk walking", "10:30 PM - Consistent sleep cycle"],
            "monitoring_plan": ["Weekly Blood Pressure checks", "Monthly Fasting Glucose screening", "Monitor BMI weekly"],
            "physical_activity": ["Brisk walking (30 min, 4x weekly)", "Bodyweight resistance training", "Swimming"],
            "diet_configuration": ["Increase fiber intake", "Limit processed carbohydrates", "Portion control focused"],
            "supplements": ["Daily Multivitamin", "Vitamin B12 if vegetarian", "Standard Omega-3"],
            "medicinal_guidance": ["General wellness check mandatory", "Inform doctor of elevated indicators during next visit"]
        }
    else:
        return {
            "medical_summary": "Your physiological parameters currently align with optimal health maintenance ranges.",
            "daily_routine": ["Standard daily schedule", "Maintain consistent hydration (2L+)", "Prioritize 150 min activity/week"],
            "monitoring_plan": ["Annual comprehensive checkup", "Maintain BMI <25", "Standard preventive screening"],
            "physical_activity": ["Standard strength training", "Aerobic activity (150 min/week)", "Flexible mobility work"],
            "diet_configuration": ["Balanced Mediterranean-style diet", "Moderate sodium/sugar", "Whole-food focused"],
            "supplements": ["Maintenance Multivitamin", "Probiotics for gut health"],
            "medicinal_guidance": ["Maintain existing preventive protocols", "No immediate medicinal intervention indicated"]
        }

def generate_doctor_report(predict_results, data):
    """Main entry point to get the full report."""
    if GEMINI_ENABLED:
        ai_advice = get_recommendations_from_gemini(predict_results, data)
        if ai_advice:
            return ai_advice
            
    return get_fallback_recommendations(predict_results, data)

def generate_combined_analysis(predict_results):
    has_diabetes_high = predict_results.get('diabetes', {}).get('risk_level') == 'High'
    has_hyper_high = predict_results.get('hypertension', {}).get('risk_level') == 'High'
    has_heart_high = predict_results.get('heart', {}).get('risk_level') == 'High'
    
    warnings = []
    if has_diabetes_high and has_hyper_high:
        warnings.append("⚠️ **CRITICAL METABOLIC ALERT**: The simultaneous high risk of Diabetes and Hypertension exponentially scales cardiovascular mortality.")
    if has_heart_high and (has_diabetes_high or has_hyper_high):
        warnings.append("🚨 **HEART STRAIN ALERT**: Underlying conditions are aggressively amplifying your Heart Disease risk profile.")
        
    return warnings

def generate_recommendations(predict_results, data):
    # This is kept for backward compatibility if needed, but the main logic is now in generate_doctor_report
    return get_fallback_recommendations(predict_results, data)
