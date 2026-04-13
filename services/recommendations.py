def analyze_values(data):
    analysis = []
    
    # Glucose Analysis
    if 'glucose' in data:
        gl = data['glucose']
        if gl < 70:
            analysis.append({"name": "Glucose", "status": "Low", "value": gl, "warning": True})
        elif gl <= 140:
            analysis.append({"name": "Glucose", "status": "Normal", "value": gl, "warning": False})
        else:
            analysis.append({"name": "Glucose", "status": "High", "value": gl, "warning": True})
            
    # BMI Analysis
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
            
    # BP Analysis
    if 'ap_hi' in data and 'ap_lo' in data:
        sys = data['ap_hi']
        dia = data['ap_lo']
        if sys > 130 or dia > 85:
            analysis.append({"name": "Blood Pressure", "status": f"Elevated ({sys}/{dia})", "value": f"{sys}/{dia}", "warning": True})
        else:
            analysis.append({"name": "Blood Pressure", "status": "Normal", "value": f"{sys}/{dia}", "warning": False})
            
    return analysis

def generate_insights(predict_results, data):
    insights = []
    
    if predict_results.get('diabetes', {}).get('prediction') == 1:
        insights.append("Your profile indicates a risk of Diabetes. Elevated glucose levels could be placing strain on your systemic health, which over time can affect your nerves and blood vessels.")
        
    if predict_results.get('hypertension', {}).get('prediction') == 1:
        insights.append("There are signs of Hypertension. High blood pressure means your heart is working harder to pump blood, increasing the risk of cardiovascular events.")
        
    if predict_results.get('heart', {}).get('prediction') == 1:
        insights.append("Your metrics show a high predictive risk for Heart Disease. This indicates that factors like your cholesterol, BP, or age profile require cardiovascular attention.")
        
    if not insights:
        insights.append("Your predict metrics are within expected ranges. Maintaining a healthy lifestyle will help keep your risks low.")
        
    return insights

def generate_recommendations(predict_results):
    has_diabetes = predict_results.get('diabetes', {}).get('prediction') == 1
    has_hyper = predict_results.get('hypertension', {}).get('prediction') == 1
    has_heart = predict_results.get('heart', {}).get('prediction') == 1
    
    # Defaults
    recs = {
        "diet": ["Maintain a balanced diet rich in leafy greens, lean proteins, and whole grains."],
        "exercise": ["Aim for 150 minutes of moderate aerobic activity every week."],
        "medicine": ["Always consult a doctor before taking any long-term medication."],
        "vitamins": ["Vitamin D (1000-2000 IU/day)", "Vitamin B12", "Omega-3 Fatty Acids (Fish Oil)"],
        "preventive": ["Annual comprehensive health checkup", "Maintain a healthy sleep schedule of 7-8 hours"]
    }
    
    if has_diabetes:
        recs["diet"].extend(["Strictly avoid refined sugars and high-glycemic foods.", "Incorporate complex carbohydrates like oats and quinoa."])
        recs["preventive"].append("Monitor your fasting blood sugar weekly.")
        recs["medicine"].append("Metformin is a common prescription (Consult physician).")
        
    if has_hyper:
        recs["diet"].append("Follow the DASH diet. Reduce sodium intake to less than 1,500mg per day.")
        recs["exercise"].append("Engage in daily brisk walking or light jogging to improve vascular health.")
        recs["medicine"].append("ACE inhibitors or ARBs are common for BP control (Consult physician).")
        
    if has_heart:
        recs["diet"].append("Avoid saturated and trans fats to manage cholesterol.")
        recs["exercise"].append("Perform light to moderate stationary cycling or swimming under medical supervision.")
        recs["vitamins"].append("CoQ10 supplements might be beneficial for heart health.")
        recs["medicine"].append("Statins or beta-blockers might be prescribed by your cardiologist.")
        
    return recs

def generate_combined_analysis(predict_results):
    has_diabetes = predict_results.get('diabetes', {}).get('prediction') == 1
    has_hyper = predict_results.get('hypertension', {}).get('prediction') == 1
    has_heart = predict_results.get('heart', {}).get('prediction') == 1
    
    warnings = []
    if has_diabetes and has_hyper:
        warnings.append("⚠️ **CRITICAL: Diabetes + Hypertension detected.** This combination exponentially increases the risk of severe cardiovascular complications. Immediate dietary adjustment and physician consultation required.")
    
    if has_heart and (has_diabetes or has_hyper):
        warnings.append("🚨 **HIGH ALERT: Pre-existing conditions amplifying Heart Disease Risk.** Ensure strict adherence to medical advice, as combined markers accelerate arterial aging.")
        
    return warnings
