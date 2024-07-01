from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# In-memory storage for simplicity
patients_data = {}
questionnaire_data = {}

@app.route('/presentation', methods=['GET'])
def get_presentation():
    return "Welcome to the hospital. Please proceed to fill in your personal data."

@app.route('/personal-data', methods=['GET'])
def get_personal_data_form():
    return {
        "fields": ["firstName", "lastName", "age", "gender", "medicalHistory", "currentMedications", "allergies", "emergencyContact", "address"]
    }

@app.route('/personal-data', methods=['POST'])
def submit_personal_data():
    data = request.json
    # Generate a unique patient ID (for example purposes, you might use a database ID generator)
    patient_id = len(patients_data) + 1
    data['patientId'] = patient_id  # Assign a new patientId
    patients_data[patient_id] = data
    return "Personal data submitted successfully."

@app.route('/questionnaire', methods=['GET'])
def get_questionnaire():
    return {
        "questions": ["Have you consumed alcohol in the last 24 hours?", "Do you smoke cigarettes or use tobacco products?", "Have you engaged in vigorous physical activity in the past week?", "Have you experienced unusual fatigue or tiredness recently?", "Do you experience chronic stress or anxiety?", "Have you had fever or high temperature recently?", "Have you been diagnosed with typhoid or similar infections?", "Are you allergic to any medications or substances?", "Do you have a history of chronic conditions or illnesses?"]
    }

@app.route('/questionnaire', methods=['POST'])
def submit_questionnaire():
    data = request.json
    # For example purposes, generate a unique identifier (e.g., using length of existing data)
    patient_id = len(questionnaire_data) + 1
    data['patientId'] = patient_id
    questionnaire_data[patient_id] = data
    
    return "Questionnaire submitted successfully."

@app.route('/risk-assessment', methods=['POST'])
def risk_assessment():

    patient = patients_data[1]
    questionnaire = questionnaire_data[1]

    # Initial threshold based on age and gender
    age = int(patient.get('age', 0))
    gender = patient.get('gender', '').lower()
    threshold = 0
    
    if age < 6:
        threshold += 3
    elif age >= 6 and age <= 14:
        threshold += 2
    elif age > 14 and age <= 25:
        threshold += 1
    elif age >= 35 and age <= 45:
        threshold += 2
    elif age > 45 and age <= 60:
        threshold += 3
    elif age > 60:
        threshold += 4
    
    if gender == 'female':
        threshold += 2

    # Keywords indicating high risk in personal data
    high_risk_keywords = ["fever", "typhoid", "allergic reaction", "chronic condition"]

    # Check medical history, current medications, and allergies for high-risk keywords
    for field in ['medicalHistory', 'currentMedications', 'allergies']:
        text = patient.get(field, '').lower()
        for keyword in high_risk_keywords:
            if keyword in text:
                threshold += 1

    questionnaire.pop('patientId', None)

    # Evaluate questionnaire responses
    threshold += sum(1 for answer in questionnaire.values() if answer.lower() == 'yes')

    # Prepare response based on assessment
    if threshold > 50:
        message = "You will be called back by phone for additional analysis."
        file_path = 'at_risk_patients.xlsx'
        new_data = pd.DataFrame([patient])
        if os.path.exists(file_path):
            # If the file exists, append the new data
            existing_data = pd.read_excel(file_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            updated_data.to_excel(file_path, index=False)
        else:
            # If the file doesn't exist, create a new one
            new_data.to_excel(file_path, index=False)
        # Optionally, perform additional actions based on risk assessment
    else:
        message = "You are ok!"

    return jsonify({
        "message": message
    })

if __name__ == '__main__':
    app.run(debug=True)
