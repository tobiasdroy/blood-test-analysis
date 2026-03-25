# interpreter.py

# A dictionary holding the metric data:
# Key: Metric Name (standardized)
# Value: Dictionary of reference data (range, units, explanation, advice)
CONSULTATION_RESULTS = {
    "blood_pressure": {
        "name": "Blood Pressure",
        "type": "compound",
        "gender_specific": False,
        "range": (90, 140, 60, 90),  # Normal systolic range in mmHg
        "unit": "mmHg",
        "explanation": "Measures the force of blood pushing against your artery walls. The first (higher) number is the pressure when your heart pumps; the lower number is the pressure when it rests between beats.",
        "advice_high": "Reduce salt intake, exercise regularly, and manage stress.",
        "advice_low": "Ensure adequate hydration and consider increasing salt intake if advised by a healthcare professional."
    },
    "pulse_rate": {
        "name": "Pulse Rate",
        "type": "hilo",
        "gender_specific": False,
        "range": (60, 100),  # Normal resting heart rate in bpm
        "unit": "bpm",
        "explanation": "How many times your heart beats per minute. A consistently very high or low pulse rate can indicate an underlying health issue.",
        "advice_high": "Incorporate regular cardiovascular exercise and practice relaxation techniques.",
        "advice_low": "Consult a healthcare professional to rule out any underlying conditions."
    },
    "bmi": {
        "name": "Body Mass Index (BMI)",
        "type": "hilo",
        "gender_specific": False,
        "range": (18.5, 24.9),  # Normal BMI range
        "unit": "kg/m²",
        "explanation": "Compares your weight to your height as an indicator of whether you are underweight, a healthy weight, overweight, or obese.",
        "advice_high": "Adopt a balanced diet and increase physical activity.",
        "advice_low": "Increase calorie intake with nutritious foods and consider strength training exercises."
    },
    "muscle_mass": {
        "name": "Muscle Mass",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (30, 100),  # Example range in %
        "unit": "%",
        "explanation": "How much of your body weight comes from muscle. Higher muscle mass is generally associated with better metabolic health and physical function.",
        "advice_high": "Maintain your current exercise routine and balanced diet.",
        "advice_low": "Incorporate strength training and ensure adequate protein intake."
    },
    "average_peak_flow": {
        "name": "Average Peak Flow",
        "type": "lower_bound",
        "range": (300, 700),  # Example range in L/min
        "unit": "L/min",
        "explanation": "How fast you can blow air out of your lungs. Used to check breathing capacity and monitor respiratory conditions such as asthma.",
        "advice_high": "Maintain good respiratory health through regular exercise and avoiding pollutants.",
        "advice_low": "Consult a healthcare professional for assessment and possible treatment."
    },
    "body_fat_percentage": {
        "name": "Body Fat Percentage",
        "type": "hilo",
        "gender_specific": True,
        "range": (10, 32, 10, 25),  # Example range in %
        "unit": "%",
        "explanation": "How much of your body weight is made up of fat. Both too little and too much body fat can affect your health.",
        "advice_high": "Incorporate regular exercise and a balanced diet to reduce body fat.",
        "advice_low": "Ensure adequate calorie intake and consider strength training exercises."
    },
    "blood_oxygen_saturation": {
        "name": "Blood Oxygen Saturation",
        "type": "lower_bound",
        "range": (92, 100),  # Normal SpO2 range in %
        "unit": "%",
        "explanation": "How much oxygen your blood is carrying, expressed as a percentage. Low levels can indicate a respiratory or circulatory problem.",
        "advice_high": "Maintain good respiratory health through regular exercise and avoiding pollutants.",
        "advice_low": "Consult a healthcare professional for assessment and possible treatment."
    },
    "qrisk_score": {
        "name": "QRISK Score",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 20),  # Example range in %
        "unit": "%",
        "explanation": "Estimates your chance of having a heart attack or stroke in the next 10 years, calculated from a combination of health and lifestyle factors.",
        "advice_high": "Adopt a heart-healthy lifestyle, including diet, exercise, and smoking cessation.",
        "advice_low": "Maintain your healthy lifestyle to keep your risk low."
    }
}

FULL_BLOOD_COUNT = {
    "haemoglobin": {
        "name": "Haemoglobin",
        "type": "hilo",
        "gender_specific": True,
        "range": (120, 150, 130, 170),  #
        "unit": "g/L",
        "explanation": "Haemoglobin is a protein in red blood cells that carries oxygen. Low levels can indicate anemia.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase iron-rich foods in your diet and consider supplements if advised."
    },
    "red_blood_cell_count": {
        "name": "Red Blood Cell Count",
        "type": "hilo",
        "gender_specific": True,
        "range": (3.8, 4.8, 4.7, 6.1),
        "unit": "x10¹²/L",
        "explanation": "Red blood cell count measures the number of red blood cells in your blood. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "hct": {
        "name": "Haematocrit (HCT)",
        "type": "hilo",
        "gender_specific": True,
        "range": (36, 46, 40, 54),
        "unit": "%",
        "explanation": "Hematocrit (HCT) measures the proportion of red blood cells in your blood. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "mcv": {
        "name": "Mean Corpuscular Volume",
        "type": "hilo",
        "gender_specific": False,
        "range": (83, 101),
        "unit": "fL",
        "explanation": "Mean Corpuscular Volume (MCV) measures the average size of your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "mch": {
        "name": "Mean Corpuscular Haemoglobin",
        "type": "hilo",
        "gender_specific": False,
        "range": (27, 32),
        "unit": "pg",
        "explanation": "Mean Corpuscular Hemoglobin (MCH) measures the average amount of hemoglobin in your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "mchc": {
        "name": "Mean Corpuscular Haemoglobin Concentration (MCHC)",
        "type": "hilo",
        "gender_specific": False,
        "range": (315, 345),
        "unit": "g/L",
        "explanation": "Mean Corpuscular Hemoglobin Concentration (MCHC) measures the average concentration of hemoglobin in your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "rdw": {
        "name": "Red Cell Distribution Width (RDW)",
        "type": "hilo", 
        "gender_specific": False,
        "range": (11.6, 14),
        "unit": "%",
        "explanation": "Red Cell Distribution Width (RDW) measures the variation in size of your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "platelets": {
        "name": "Platelet Count",
        "type": "hilo",
        "gender_specific": False,
        "range": (150, 410),
        "unit": "x10⁹/L",
        "explanation": "Platelets are small blood cells that help with clotting. Abnormal levels can indicate bleeding disorders or bone marrow issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid injury and consult a healthcare professional."
    },
    "mpv": {
        "name": "Mean Platelet Volume (MPV)",
        "type": "hilo",
        "gender_specific": False,
        "range": (7.1, 10.1),
        "unit": "fL",
        "explanation": "Mean Platelet Volume (MPV) measures the average size of your platelets. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "white_blood_cell_count": {
        "name": "White Blood Cell Count",
        "type": "hilo",
        "gender_specific": False,
        "range": (4.0, 10.0),
        "unit": "x10⁹/L",
        "explanation": "White blood cell count measures the number of white blood cells in your blood. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional." 
    },
    "neutrophils": {
        "name": "Neutrophils",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.0, 7.0),
        "unit": "x10⁹/L",
        "explanation": "Neutrophils are a type of white blood cell that helps fight infections. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional." 
    },
    "lymphocytes": {
        "name": "Lymphocytes",
        "type": "hilo",
        "gender_specific": False,
        "range": (1.0, 3.0),
        "unit": "x10⁹/L",
        "explanation": "Lymphocytes are a type of white blood cell that helps fight infections. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional."
    },
    "monocytes": {
        "name": "Monocytes",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.2, 1.0),
        "unit": "x10⁹/L",
        "explanation": "Monocytes are a type of white blood cell that helps fight infections. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional."
    },
    "eosinophils": {
        "name": "Eosinophils",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.02, 0.5),
        "unit": "x10⁹/L",
        "explanation": "Eosinophils are a type of white blood cell involved in allergic reactions and fighting parasites. High levels can indicate allergies or infections.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern." 
    },
    "basophils": {
        "name": "Basophils",    
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.02, 0.1),
        "unit": "x10⁹/L",
        "explanation": "Basophils are a type of white blood cell involved in allergic reactions. High levels can indicate allergies or infections.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern." 
    },
}

KIDNEY_FUNCTION = {
    "sodium": {
        "name": "Sodium",
        "type": "hilo",
        "gender_specific": False,
        "range": (133, 146),
        "unit": "mmol/L",
        "explanation": "Sodium is an essential electrolyte that helps maintain fluid balance and nerve function. Abnormal levels can indicate dehydration or kidney issues.",
        "advice_high": "Reduce salt intake and ensure adequate hydration.", 
        "advice_low": "Increase salt intake and ensure adequate hydration." 
    },
    "potassium": {
        "name": "Potassium",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.5, 5.3),
        "unit": "mmol/L",
        "explanation": "Potassium is an essential electrolyte that helps maintain heart and muscle function. Abnormal levels can indicate kidney issues or dehydration.",
        "advice_high": "Limit high-potassium foods and consult a healthcare professional.", 
        "advice_low": "Increase intake of potassium-rich foods like bananas and oranges." 
    },
    "urea": {
        "name": "Urea",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.2, 8.2),
        "unit": "mmol/L",
        "explanation": "Urea is a waste product formed in the liver and excreted by the kidneys. Abnormal levels can indicate kidney function issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Ensure adequate protein intake and hydration." 
    },
    "creatinine": {
        "name": "Creatinine",
        "type": "hilo",
        "gender_specific": True,
        "range": (49, 90, 62, 115),
        "unit": "µmol/L",
        "explanation": "Creatinine is a waste product produced by muscle metabolism and excreted by the kidneys. Abnormal levels can indicate kidney function issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Ensure adequate nutrition and hydration."    
    }
}

HEART_HEALTH = {
    "cholesterol": {
        "name": "Cholesterol",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.5, 5.18),
        "unit": "mmol/L",
        "explanation": "Cholesterol is a fatty substance in your blood. High levels can increase the risk of heart disease.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate cholesterol levels."
    },
    "triglycerides": {
        "name": "Triglycerides",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.4, 1.7),
        "unit": "mmol/L",
        "explanation": "Triglycerides are a type of fat in your blood. High levels can increase the risk of heart disease.",
        "advice_high": "Reduce intake of sugary and fatty foods, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate triglyceride levels."
    },
    "hdl_cholesterol": {
        "name": "HDL Cholesterol",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (1.04, 100),
        "unit": "mmol/L",
        "explanation": "HDL cholesterol is known as 'good' cholesterol. Higher levels are better for heart health.",
        "advice_high": "Maintain your healthy lifestyle to keep your HDL levels high.",
        "advice_low": "Incorporate healthy fats into your diet and exercise regularly."
    },
    "ldl_cholesterol": {
        "name": "LDL Cholesterol",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.5, 3.0),
        "unit": "mmol/L",
        "explanation": "LDL cholesterol is known as 'bad' cholesterol. High levels can increase the risk of heart disease.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate LDL levels."
    },
    "tc_hdl_ratio": {
        "name": "Total Cholesterol to HDL Ratio",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 4.5),
        "unit": "",
        "explanation": "The total cholesterol to HDL ratio is used to assess heart disease risk. Lower ratios are better for heart health.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure an adequate cholesterol ratio."   
    },
    "hdl_percentage_of_total_cholesterol": {
        "name": "HDL Percentage of Total Cholesterol",
        "type": "hilo",
        "gender_specific": False,
        "range": (20, 50),
        "unit": "%",
        "explanation": "The percentage of HDL cholesterol in total cholesterol is used to assess heart disease risk. Higher percentages are better for heart health.",
        "advice_high": "Maintain your healthy lifestyle to keep your HDL percentage high.",
        "advice_low": "Incorporate healthy fats into your diet and exercise regularly."
    },
    "hs_crp": {
        "name": "High-sensitivity C-reactive Protein (hs-CRP)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 5.0),
        "unit": "mg/L",
        "explanation": "High-sensitivity C-reactive protein (hs-CRP) is a marker of inflammation in the body. High levels can indicate an increased risk of heart disease.",   
        "advice_high": "Adopt a heart-healthy lifestyle, including diet, exercise, and smoking cessation.",
        "advice_low": "Maintain your healthy lifestyle to keep inflammation low."
    },
    "apolipoprotein_a1": {
        "name": "Apolipoprotein A1",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.76, 2.14),
        "unit": "g/L",
        "explanation": "Apolipoprotein A1 is a component of HDL cholesterol. Higher levels are better for heart health.",
        "advice_high": "Maintain your healthy lifestyle to keep your ApoA1 levels high.",
        "advice_low": "Incorporate healthy fats into your diet and exercise regularly."
    },
    "apolipoprotein_b": {
        "name": "Apolipoprotein B",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.46, 1.42),
        "unit": "g/L",
        "explanation": "Apolipoprotein B is a component of LDL cholesterol. High levels can increase the risk of heart disease.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate ApoB levels."
    },
    "lipoprotein_a": {
        "name": "Lipoprotein(a)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 0.3),
        "unit": "g/L",
        "explanation": "Lipoprotein(a) is a type of lipoprotein that can increase the risk of heart disease. High levels are a concern.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Maintain a healthy lifestyle to keep Lipoprotein(a) levels low."
    }
}

DIABETES_MARKERS = {
    "hba1c": {
        "name": "HbA1c",
        "type": "hilo", 
        "gender_specific": False,
        "range": (20, 42),
        "unit": "mmol/mol",
        "explanation": "HbA1c reflects your average blood glucose levels over the past 2-3 months. High levels can indicate diabetes or prediabetes.",    
        "advice_high": "Adopt a healthy diet, exercise regularly, and monitor your blood sugar levels.",    
        "advice_low": "Maintain a balanced diet to ensure adequate blood sugar levels."    
    },
    "glucose": {
        "name": "Glucose",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.9, 6.9),
        "unit": "mmol/L",
        "explanation": "Glucose is the main sugar found in your blood. High levels can indicate diabetes or prediabetes.",
        "advice_high": "Adopt a healthy diet, exercise regularly, and monitor your blood sugar levels.",
        "advice_low": "Maintain a balanced diet to ensure adequate blood sugar levels."
    }
}

IRON_STATUS = {
    "serum_iron": {
        "name": "Serum Iron",
        "type": "hilo",
        "gender_specific": False,
        "range": (9, 30.4),
        "unit": "µmol/L",
        "explanation": "Serum iron measures the amount of iron in your blood. Abnormal levels can indicate iron deficiency or overload.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase intake of iron-rich foods and consider supplements if advised."
    },
    "transferrin": {
        "name": "Transferrin",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.5, 3.8),
        "unit": "g/L",
        "explanation": "Transferrin is a protein that transports iron in your blood. Abnormal levels can indicate iron deficiency or overload.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase intake of iron-rich foods and consider supplements if advised."
    },
    "ferritin": {
        "name": "Ferritin",
        "type": "hilo",
        "gender_specific": True,
        "range": (10, 291, 30, 400),
        "unit": "ng/mL",
        "explanation": "Ferritin is a protein that stores iron in your body. Abnormal levels can indicate iron deficiency or overload.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase intake of iron-rich foods and consider supplements if advised."
    },
    "uric_acid": {
        "name": "Uric Acid",
        "type": "hilo",
        "gender_specific": False,
        "range": (184, 464),
        "unit": "µmol/L",
        "explanation": "Uric acid is a waste product formed from the breakdown of purines. High levels can indicate gout or kidney issues.",
        "advice_high": "Reduce intake of purine-rich foods and ensure adequate hydration.",
        "advice_low": "Maintain a balanced diet and ensure adequate hydration."
    }
}

BONE_PROFILE = {
    "vitamin_d": {
        "name": "Vitamin D",
        "type": "hilo",
        "gender_specific": False,
        "range": (50, 125),
        "unit": "nmol/L",
        "explanation": "Vitamin D is essential for bone health and calcium absorption. Low levels can lead to bone disorders.",
        "advice_high": "Avoid excessive vitamin D supplementation and consult a healthcare professional.",
        "advice_low": "Increase sun exposure and consider vitamin D supplements if advised."
    },
}

MUSCLE_HEALTH = {
    "ck": {
        "name": "Creatine Kinase (CK)",
        "type": "hilo",
        "gender_specific": False,
        "range": (25, 200),
        "unit": "U/L",
        "explanation": "Creatine kinase (CK) is an enzyme found in the heart, brain, and skeletal muscle. High levels can indicate muscle damage.",
        "advice_high": "Avoid strenuous exercise and consult a healthcare professional for further evaluation.",
        "advice_low": "Maintain a balanced diet and regular exercise routine."
    }
}

LIVER_FUNCTION = {
    "albumin": {
        "name": "Albumin",
        "type": "hilo",
        "gender_specific": False,
        "range": (34, 50),
        "unit": "g/L",
        "explanation": "Albumin is a protein made by the liver. Low levels can indicate liver disease or malnutrition.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Ensure adequate protein intake and consult a healthcare professional."
    },
    "total_bilirubin": {
        "name": "Total Bilirubin",
        "type": "hilo",
        "gender_specific": False,
        "range": (5, 21),
        "unit": "µmol/L",
        "explanation": "Bilirubin is a yellow compound that occurs in the normal catabolism of red blood cells. High levels can indicate liver or bile duct issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "alkaline_phosphatase": {
        "name": "Alkaline Phosphatase",
        "type": "hilo",
        "gender_specific": False,
        "range": (46, 116),
        "unit": "IU/L",
        "explanation": "Alkaline phosphatase is an enzyme related to the bile ducts; high levels can indicate liver disease or bone disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "alt/gpt": {
        "name": "Alanine Aminotransferase (ALT/GPT)",
        "type": "hilo",
        "gender_specific": False,
        "range": (5, 56),
        "unit": "IU/L",
        "explanation": "Alanine aminotransferase (ALT) is an enzyme found in the liver. High levels can indicate liver damage.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "ast/got": {
        "name": "Aspartate Aminotransferase (AST/GOT)",
        "type": "hilo",
        "gender_specific": False,
        "range": (13, 45),
        "unit": "IU/L",
        "explanation": "Aspartate aminotransferase (AST) is an enzyme found in the liver and heart. High levels can indicate liver or heart damage.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "gamma_gt": {
        "name": "Gamma-Glutamyl Transferase (GGT)",
        "type": "hilo",
        "gender_specific": False,
        "range": (4, 38),
        "unit": "IU/L",
        "explanation": "Gamma-glutamyl transferase (GGT) is an enzyme found in the liver. High levels can indicate liver or bile duct issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    }
}

URINE_ANALYSIS = {
    "ph": {
        "name": "pH",
        "type": "hilo",
        "gender_specific": False,
        "range": (4.5, 8.0),
        "unit": "",
        "explanation": "Urine pH indicates the acidity or alkalinity of your urine. Abnormal levels can indicate kidney issues or urinary tract infections.",   
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."    
    },
    "urine_protein": {
        "name": "Urine Protein",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Protein in urine can indicate kidney damage or disease. Presence of protein should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of protein is generally not a concern."    
    },
    "urine_glucose": {
        "name": "Urine Glucose",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Glucose in urine can indicate high blood sugar levels, often associated with diabetes. Presence of glucose should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of glucose is generally not a concern."    
    },
    "ketones": {
        "name": "Ketones",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Ketones in urine can indicate that the body is using fat for energy instead of glucose. Presence of ketones should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of ketones is generally not a concern."    
    },
    "wbcs": {
        "name": "White Blood Cells",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "White blood cells (WBCs) in urine can indicate a urinary tract infection. Presence of WBCs should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of WBCs is generally not a concern." 
    },
    "rbcs": {
        "name": "Red Blood Cells",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "Red blood cells (RBCs) in urine can indicate bleeding in the urinary tract. Presence of RBCs should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of RBCs is generally not a concern." 
    },
    "casts": {
        "name": "Casts",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "casts/µL",
        "explanation": "Casts in urine can indicate kidney issues. Presence of casts should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of casts is generally not a concern." 
    },
    "bacterial_count": {
        "name": "Bacterial Count",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cfu/mL",
        "explanation": "Bacterial count in urine can indicate a urinary tract infection. Presence of bacteria should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of bacteria is generally not a concern." 
    }
}

THYROID_FUNCTION = {
    "free_thyroxine": {
        "name": "Free Thyroxine (FT4)",
        "type": "hilo",
        "gender_specific": False,
        "range": (10.4, 19.4),
        "unit": "pmol/L",
        "explanation": "Free thyroxine (FT4) is a hormone produced by the thyroid gland. Abnormal levels can indicate thyroid dysfunction.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."    
    },
    "tsh": {
        "name": "Thyroid-Stimulating Hormone (TSH)",
        "type": "hilo", 
        "gender_specific": False,
        "range": (0.55, 4.78),
        "unit": "mIU/L",
        "explanation": "Thyroid-stimulating hormone (TSH) regulates thyroid function. Abnormal levels can indicate thyroid dysfunction.",   
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."
    },
    "ft3": {
        "name": "Free Triiodothyronine (FT3)",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.6, 7.1),
        "unit": "pmol/L",
        "explanation": "Free triiodothyronine (FT3) is a hormone produced by the thyroid gland. Abnormal levels can indicate thyroid dysfunction.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."    
    }
}

CANCER_MARKERS = {
    "ca_125": {
        "name": "CA 125",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 35),
        "unit": "U/mL",
        "explanation": "A protein linked to ovarian cancer risk. Elevated levels may indicate ovarian cancer or other conditions. Note that this marker is not applicable to those without ovaries.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; normal levels are generally not a concern." 
    },
    "psa": {
        "name": "Prostate-Specific Antigen (PSA)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 4),
        "unit": "ng/mL",
        "explanation": "A protein produced by the prostate gland. Elevated levels can indicate prostate problems including cancer. Note that this marker is not applicable to those without a prostate.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; low levels are generally not a concern."
    }
}

VITAMINS = {
    "ab12": {
        "name": "Vitamin B12 (cobalamin)",
        "type": "hilo",
        "gender_specific": False,
        "range": (25.1, 165),
        "unit": "pmol/L",
        "explanation": "Essential for nerve health and blood cell production. Low levels can cause anaemia and neurological problems; very high levels may warrant further investigation.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."
    },
    "folate": {
        "name": "Folate (vitamin B9)",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (3, 17),
        "unit": "ng/mL",
        "explanation": "Essential for nerve health, blood cell production, and DNA synthesis. Low levels can cause anaemia and are particularly important to address during pregnancy.",    
        "advice_high": "No specific advice; high levels are generally not a concern.", 
        "advice_low": "Consult a healthcare professional for further evaluation."
    }
}

BLOOD_METRIC_DATA = {}
BLOOD_METRIC_DATA.update(FULL_BLOOD_COUNT)
BLOOD_METRIC_DATA.update(KIDNEY_FUNCTION)
BLOOD_METRIC_DATA.update(HEART_HEALTH)
BLOOD_METRIC_DATA.update(DIABETES_MARKERS)
BLOOD_METRIC_DATA.update(IRON_STATUS)
BLOOD_METRIC_DATA.update(BONE_PROFILE)
BLOOD_METRIC_DATA.update(MUSCLE_HEALTH)
BLOOD_METRIC_DATA.update(LIVER_FUNCTION)
BLOOD_METRIC_DATA.update(URINE_ANALYSIS)
BLOOD_METRIC_DATA.update(THYROID_FUNCTION)
BLOOD_METRIC_DATA.update(CANCER_MARKERS)
BLOOD_METRIC_DATA.update(VITAMINS)

def interpret_result(metric, data, gender):
    """
    Interprets a single blood test result based on the defined data.
    Returns a tuple: (status, explanation, advice)
    """
    
    # 2. Check if the metric is known
    if metric not in BLOOD_METRIC_DATA:
        return ("Unknown", "This metric is not yet in our database.", "Consult your doctor for interpretation.")


    if data["gender_specific"]:
        if gender == "Female":
            low_end, high_end = data["range"][0:2]
        elif gender == "Male":
            low_end, high_end = data["range"][2:4]
        else:
            return ("Unknown", "Gender not specified correctly for this metric.", "Consult your doctor for interpretation.")
    else:
        low_end, high_end = data["range"]
    
    # 3. Simple interpretation logic
    if data["value"] < low_end:
        status = "Low"
        advice = data.get("advice_low", "See a healthcare professional for specific advice.")
    elif data["value"] > high_end:
        status = "High"
        advice = data.get("advice_high", "See a healthcare professional for specific advice.")
    else:
        status = "Normal"
        advice = "Maintain your current healthy lifestyle."

    explanation = data["explanation"]
    
    return status, explanation, advice