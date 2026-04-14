import requests
import json
from passlib.context import CryptContext
from core.database import users_collection

# Reset testuser password to a known value
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("Test123!")
users_collection.update_one({"username": "testuser"}, {"$set": {"password": hashed}})
print("Password reset for testuser to: Test123!")

# Login
login = requests.post("http://localhost:8000/api/auth/login", data={"username": "testuser", "password": "Test123!"})
print("Login:", login.status_code)
token = login.json().get("access_token")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Test Diabetes
payload = {
    "Age": 45, "BMI": 27.5, "FBS_mg_dL": 130.0, "PPBS_mg_dL": 175.0,
    "HbA1c_pct": 7.2, "SBP_mmHg": 135, "DBP_mmHg": 88, "Insulin_uU_mL": 18.5,
    "Physical_Activity_Score": 40, "Family_History": 1, "LDL_mg_dL": 145.0,
    "HDL_mg_dL": 42.0, "Triglycerides_mg_dL": 180.0, "Smoking": 0, "Alcohol": 0
}
r = requests.post("http://localhost:8000/api/predict/diabetes", json=payload, headers=headers)
print("Predict status:", r.status_code)
data = r.json()

if "report" in data:
    report = data["report"]
    print("\nReport keys:", list(report.keys()))
    print("Predictions:", json.dumps(report.get("predictions", {}), indent=2)[:500])
    print("Doctor report keys:", list(report.get("doctor_report", {}).keys()))
    print("Analysis items:", len(report.get("analysis", [])))
else:
    print("No report in response!")
    print(json.dumps(data, indent=2)[:600])
