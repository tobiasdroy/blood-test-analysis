# interpreter.py

# A dictionary holding the metric data:
# Key: Metric Name (standardized)
# Value: Dictionary of reference data (range, units, explanation, advice)
CONSULTATION_RESULTS = {
    "blood_pressure": {
        "type": "compound",
        "gender_specific": False,
        "range": (90, 140, 60, 90),  # Normal systolic range in mmHg
        "unit": "mmHg",
        "explanation": "Blood pressure indicates the force of blood against your artery walls. High blood pressure can lead to heart disease.",
        "advice_high": "Reduce salt intake, exercise regularly, and manage stress.",
        "advice_low": "Ensure adequate hydration and consider increasing salt intake if advised by a healthcare professional."
    },
    "pulse_rate": {
        "type": "hilo",
        "gender_specific": False,
        "range": (60, 100),  # Normal resting heart rate in bpm
        "unit": "bpm",
        "explanation": "Pulse rate indicates your heartbeats per minute. A very high or low pulse rate can indicate underlying health issues.",
        "advice_high": "Incorporate regular cardiovascular exercise and practice relaxation techniques.",
        "advice_low": "Consult a healthcare professional to rule out any underlying conditions."
    },
    "bmi": {
        "type": "hilo",
        "gender_specific": False,
        "range": (18.5, 24.9),  # Normal BMI range
        "unit": "kg/m²",
        "explanation": "Body Mass Index (BMI) is a measure of body fat based on height and weight.",
        "advice_high": "Adopt a balanced diet and increase physical activity.",
        "advice_low": "Increase calorie intake with nutritious foods and consider strength training exercises."
    },
    "muscle_mass": {
        "type": "lower_bound",
        "gender_specific": False,
        "range": (30, 100),  # Example range in %
        "unit": "%",
        "explanation": "Muscle mass percentage indicates the proportion of your body weight that is muscle.",
        "advice_high": "Maintain your current exercise routine and balanced diet.",
        "advice_low": "Incorporate strength training and ensure adequate protein intake."
    },
    "average_peak_flow": {
        "type": "lower_bound",
        "range": (300, 700),  # Example range in L/min
        "unit": "L/min",
        "explanation": "Peak flow measures how well air moves out of your lungs. It is important for monitoring respiratory conditions.",
        "advice_high": "Maintain good respiratory health through regular exercise and avoiding pollutants.",
        "advice_low": "Consult a healthcare professional for assessment and possible treatment."
    },
    "body_fat_percentage": {
        "type": "hilo",
        "gender_specific": True,
        "range": (10, 32, 10, 25),  # Example range in %
        "unit": "%",
        "explanation": "Body fat percentage indicates the proportion of your body weight that is fat.",
        "advice_high": "Incorporate regular exercise and a balanced diet to reduce body fat.",
        "advice_low": "Ensure adequate calorie intake and consider strength training exercises."
    },
    "blood_oxygen_saturation": {
        "type": "lower_bound",
        "range": (92, 100),  # Normal SpO2 range in %
        "unit": "%",
        "explanation": "Blood oxygen saturation indicates how much oxygen your blood is carrying. Low levels can indicate respiratory issues.",
        "advice_high": "Maintain good respiratory health through regular exercise and avoiding pollutants.",
        "advice_low": "Consult a healthcare professional for assessment and possible treatment."
    },
    "qrisk_score": {
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 20),  # Example range in %
        "unit": "%",
        "explanation": "QRISK score estimates your risk of developing cardiovascular disease over the next 10 years.",
        "advice_high": "Adopt a heart-healthy lifestyle, including diet, exercise, and smoking cessation.",
        "advice_low": "Maintain your healthy lifestyle to keep your risk low."
    }
}

FULL_BLOOD_COUNT = {
    "haemoglobin": {
        "type": "hilo",
        "gender_specific": True,
        "range": (120, 150, 130, 170),  #
        "unit": "g/L",
        "explanation": "Haemoglobin is a protein in red blood cells that carries oxygen. Low levels can indicate anemia.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase iron-rich foods in your diet and consider supplements if advised."
    },
    "red_blood_cell_count": {
        "type": "hilo",
        "gender_specific": True,
        "range": (4.2, 5.4, 4.7, 6.1),
        "unit": "million cells/µL",
        "explanation": "Red blood cell count measures the number of red blood cells in your blood. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "hct": {
        "type": "hilo",
        "gender_specific": True,
        "range": (37, 47, 40, 54),
        "unit": "%",
        "explanation": "Hematocrit (HCT) measures the proportion of red blood cells in your blood. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "mcv": {
        "type": "hilo",
        "gender_specific": False,
        "range": (80, 96),
        "unit": "fL",
        "explanation": "Mean Corpuscular Volume (MCV) measures the average size of your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "mch": {
        "type": "hilo",
        "gender_specific": False,
        "range": (27, 33),
        "unit": "pg",
        "explanation": "Mean Corpuscular Hemoglobin (MCH) measures the average amount of hemoglobin in your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "mchc": {
        "type": "hilo",
        "gender_specific": False,
        "range": (32, 36),
        "unit": "g/dL",
        "explanation": "Mean Corpuscular Hemoglobin Concentration (MCHC) measures the average concentration of hemoglobin in your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "rdw": {
        "type": "hilo", 
        "gender_specific": False,
        "range": (11.5, 14.5),
        "unit": "%",
        "explanation": "Red Cell Distribution Width (RDW) measures the variation in size of your red blood cells. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "platelets": {
        "type": "hilo",
        "gender_specific": False,
        "range": (150, 450),
        "unit": "billion cells/L",
        "explanation": "Platelets are small blood cells that help with clotting. Abnormal levels can indicate bleeding disorders or bone marrow issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid injury and consult a healthcare professional."
    },
    "mpv": {
        "type": "hilo",
        "gender_specific": False,
        "range": (7.5, 11.5),
        "unit": "fL",
        "explanation": "Mean Platelet Volume (MPV) measures the average size of your platelets. Abnormal levels can indicate various health issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Ensure adequate nutrition and consult a healthcare professional."
    },
    "white_blood_cell_count": {
        "type": "hilo",
        "gender_specific": False,
        "range": (4.0, 11.0),
        "unit": "billion cells/L",
        "explanation": "White blood cell count measures the number of white blood cells in your blood. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional." 
    },
    "neutrophils": {
        "type": "hilo",
        "gender_specific": False,
        "range": (2.0, 7.5),
        "unit": "billion cells/L",
        "explanation": "Neutrophils are a type of white blood cell that helps fight infections. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional." 
    },
    "lymphocytes": {
        "type": "hilo",
        "gender_specific": False,
        "range": (1.0, 4.0),
        "unit": "billion cells/L",
        "explanation": "Lymphocytes are a type of white blood cell that helps fight infections. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional."
    },
    "monocytes": {
        "type": "hilo",
        "gender_specific": False,
        "range": (0.2, 1.0),
        "unit": "billion cells/L",
        "explanation": "Monocytes are a type of white blood cell that helps fight infections. Abnormal levels can indicate infections or immune system disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Avoid exposure to infections and consult a healthcare professional."
    },
    "eosinophils": {
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 0.5),
        "unit": "billion cells/L",
        "explanation": "Eosinophils are a type of white blood cell involved in allergic reactions and fighting parasites. High levels can indicate allergies or infections.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern." 
    },
    "basophils": {
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 0.2),
        "unit": "billion cells/L",
        "explanation": "Basophils are a type of white blood cell involved in allergic reactions. High levels can indicate allergies or infections.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern." 
    },
}

KIDNEY_FUNCTION = {
    "sodium": {
        "type": "hilo",
        "gender_specific": False,
        "range": (135, 145),
        "unit": "mmol/L",
        "explanation": "Sodium is an essential electrolyte that helps maintain fluid balance and nerve function. Abnormal levels can indicate dehydration or kidney issues.",
        "advice_high": "Reduce salt intake and ensure adequate hydration.", 
        "advice_low": "Increase salt intake and ensure adequate hydration." 
    },
    "potassium": {
        "type": "hilo",
        "gender_specific": False,
        "range": (3.5, 5.0),
        "unit": "mmol/L",
        "explanation": "Potassium is an essential electrolyte that helps maintain heart and muscle function. Abnormal levels can indicate kidney issues or dehydration.",
        "advice_high": "Limit high-potassium foods and consult a healthcare professional.", 
        "advice_low": "Increase intake of potassium-rich foods like bananas and oranges." 
    },
    "urea": {
        "type": "hilo",
        "gender_specific": False,
        "range": (2.5, 7.8),
        "unit": "mmol/L",
        "explanation": "Urea is a waste product formed in the liver and excreted by the kidneys. Abnormal levels can indicate kidney function issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Ensure adequate protein intake and hydration." 
    },
    "creatinine": {
        "type": "hilo",
        "gender_specific": True,
        "range": (53, 97, 62, 115),
        "unit": "µmol/L",
        "explanation": "Creatinine is a waste product produced by muscle metabolism and excreted by the kidneys. Abnormal levels can indicate kidney function issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Ensure adequate nutrition and hydration."    
    }
}

HEART_HEALTH = {
    "cholesterol": {
        "type": "hilo",
        "gender_specific": False,
        "range": (3.5, 5),
        "unit": "mmol/L",
        "explanation": "Cholesterol is a fatty substance in your blood. High levels can increase the risk of heart disease.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate cholesterol levels."
    },
    "triglycerides": {
        "type": "hilo",
        "gender_specific": False,
        "range": (0.4, 1.7),
        "unit": "mmol/L",
        "explanation": "Triglycerides are a type of fat in your blood. High levels can increase the risk of heart disease.",
        "advice_high": "Reduce intake of sugary and fatty foods, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate triglyceride levels."
    },
    "hdl_cholesterol": {
        "type": "lower_bound",
        "gender_specific": False,
        "range": (1.0, 100),
        "unit": "mmol/L",
        "explanation": "HDL cholesterol is known as 'good' cholesterol. Higher levels are better for heart health.",
        "advice_high": "Maintain your healthy lifestyle to keep your HDL levels high.",
        "advice_low": "Incorporate healthy fats into your diet and exercise regularly."
    },
    "ldl_cholesterol": {
        "type": "hilo",
        "gender_specific": False,
        "range": (1.0, 3.0),
        "unit": "mmol/L",
        "explanation": "LDL cholesterol is known as 'bad' cholesterol. High levels can increase the risk of heart disease.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate LDL levels."
    },
    "tc_hdl_ratio": {
        "type": "hilo",
        "gender_specific": False,
        "range": (3, 4),
        "unit": "",
        "explanation": "The total cholesterol to HDL ratio is used to assess heart disease risk. Lower ratios are better for heart health.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure an adequate cholesterol ratio."   
    },
    "hdl_percentage_of_total_cholesterol": {
        "type": "hilo",
        "gender_specific": False,
        "range": (25, 35),
        "unit": "%",
        "explanation": "The percentage of HDL cholesterol in total cholesterol is used to assess heart disease risk. Higher percentages are better for heart health.",
        "advice_high": "Maintain your healthy lifestyle to keep your HDL percentage high.",
        "advice_low": "Incorporate healthy fats into your diet and exercise regularly."
    },
    "hs_crp": {
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 3.0),
        "unit": "mg/L",
        "explanation": "High-sensitivity C-reactive protein (hs-CRP) is a marker of inflammation in the body. High levels can indicate an increased risk of heart disease.",   
        "advice_high": "Adopt a heart-healthy lifestyle, including diet, exercise, and smoking cessation.",
        "advice_low": "Maintain your healthy lifestyle to keep inflammation low."
    },
    "apolipoprotein_a1": {
        "type": "lower_bound",
        "gender_specific": False,
        "range": (1.2, 100),
        "unit": "g/L",
        "explanation": "Apolipoprotein A1 is a component of HDL cholesterol. Higher levels are better for heart health.",
        "advice_high": "Maintain your healthy lifestyle to keep your ApoA1 levels high.",
        "advice_low": "Incorporate healthy fats into your diet and exercise regularly."
    },
    "apolipoprotein_b": {
        "type": "hilo",
        "gender_specific": False,
        "range": (0.6, 1.1),
        "unit": "g/L",
        "explanation": "Apolipoprotein B is a component of LDL cholesterol. High levels can increase the risk of heart disease.",
        "advice_high": "Adopt a heart-healthy diet, exercise regularly, and avoid smoking.",
        "advice_low": "Maintain a balanced diet to ensure adequate ApoB levels."
    },
    "lipoprotein_a": {
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 30.0),
        "unit": "mg/dL",
        "explanation": "Lipoprotein(a) is a type of lipoprotein that can increase the risk of heart disease. High levels are a concern.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Maintain a healthy lifestyle to keep Lipoprotein(a) levels low."
    }
}

DIABETES_MARKERS = {
    "hba1c": {
        "type": "hilo", 
        "gender_specific": False,
        "range": (42, 47),  
        "unit": "mmol/mol",
        "explanation": "HbA1c reflects your average blood glucose levels over the past 2-3 months. High levels can indicate diabetes or prediabetes.",    
        "advice_high": "Adopt a healthy diet, exercise regularly, and monitor your blood sugar levels.",    
        "advice_low": "Maintain a balanced diet to ensure adequate blood sugar levels."    
    },
    "glucose": {
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
        "type": "hilo",
        "gender_specific": False,
        "range": (10, 30),
        "unit": "µmol/L",
        "explanation": "Serum iron measures the amount of iron in your blood. Abnormal levels can indicate iron deficiency or overload.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase intake of iron-rich foods and consider supplements if advised."
    },
    "transferrin": {
        "type": "hilo",
        "gender_specific": False,
        "range": (2.0, 3.6),
        "unit": "g/L",
        "explanation": "Transferrin is a protein that transports iron in your blood. Abnormal levels can indicate iron deficiency or overload.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase intake of iron-rich foods and consider supplements if advised."
    },
    "ferritin": {
        "type": "hilo",
        "gender_specific": True,
        "range": (15, 150, 30, 400),
        "unit": "µg/L",
        "explanation": "Ferritin is a protein that stores iron in your body. Abnormal levels can indicate iron deficiency or overload.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "Increase intake of iron-rich foods and consider supplements if advised."
    },
    "uric_acid": {
        "type": "hilo",
        "gender_specific": True,
        "range": (143, 357, 202, 416),
        "unit": "µmol/L",
        "explanation": "Uric acid is a waste product formed from the breakdown of purines. High levels can indicate gout or kidney issues.",
        "advice_high": "Reduce intake of purine-rich foods and ensure adequate hydration.",
        "advice_low": "Maintain a balanced diet and ensure adequate hydration."
    }
}

BONE_PROFILE = {
    "vitamin_d": {
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
        "type": "hilo", 
        "gender_specific": True,
        "range": (26, 192, 39, 308),
        "unit": "IU/L",
        "explanation": "Creatine kinase (CK) is an enzyme found in the heart, brain, and skeletal muscle. High levels can indicate muscle damage.",
        "advice_high": "Avoid strenuous exercise and consult a healthcare professional for further evaluation.",
        "advice_low": "Maintain a balanced diet and regular exercise routine."
    }
}

LIVER_FUNCTION = {
    "albumin": {
        "type": "hilo",
        "gender_specific": False,
        "range": (35, 50), 
        "unit": "g/L",
        "explanation": "Albumin is a protein made by the liver. Low levels can indicate liver disease or malnutrition.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Ensure adequate protein intake and consult a healthcare professional."
    },
    "total_bilirubin": {
        "type": "hilo",
        "gender_specific": False,
        "range": (5, 21),
        "unit": "µmol/L",
        "explanation": "Bilirubin is a yellow compound that occurs in the normal catabolism of red blood cells. High levels can indicate liver or bile duct issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "alkaline_phosphatase": {
        "type": "hilo",
        "gender_specific": False,
        "range": (40, 130),
        "unit": "IU/L",
        "explanation": "Alkaline phosphatase is an enzyme related to the bile ducts; high levels can indicate liver disease or bone disorders.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "alt/gpt": {
        "type": "hilo",
        "gender_specific": False,
        "range": (7, 56),
        "unit": "IU/L",
        "explanation": "Alanine aminotransferase (ALT) is an enzyme found in the liver. High levels can indicate liver damage.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "ast/got": {
        "type": "hilo",
        "gender_specific": False,
        "range": (5, 40),
        "unit": "IU/L",
        "explanation": "Aspartate aminotransferase (AST) is an enzyme found in the liver and heart. High levels can indicate liver or heart damage.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    },
    "gamma_gt": {
        "type": "hilo",
        "gender_specific": False,
        "range": (9, 48),
        "unit": "IU/L",
        "explanation": "Gamma-glutamyl transferase (GGT) is an enzyme found in the liver. High levels can indicate liver or bile duct issues.",
        "advice_high": "Consult a healthcare professional for further evaluation.",
        "advice_low": "No specific advice; low levels are generally not a concern."
    }
}

URINE_ANALYSIS = {
    "ph": {
        "type": "hilo",
        "gender_specific": False,
        "range": (4.5, 8.0),
        "unit": "",
        "explanation": "Urine pH indicates the acidity or alkalinity of your urine. Abnormal levels can indicate kidney issues or urinary tract infections.",   
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."    
    },
    "urine_protein": {
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Protein in urine can indicate kidney damage or disease. Presence of protein should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of protein is generally not a concern."    
    },
    "urine_glucose": {
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Glucose in urine can indicate high blood sugar levels, often associated with diabetes. Presence of glucose should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of glucose is generally not a concern."    
    },
    "ketones": {
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Ketones in urine can indicate that the body is using fat for energy instead of glucose. Presence of ketones should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of ketones is generally not a concern."    
    },
    "wbcs": {
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "White blood cells (WBCs) in urine can indicate a urinary tract infection. Presence of WBCs should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of WBCs is generally not a concern." 
    },
    "rbcs": {
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "Red blood cells (RBCs) in urine can indicate bleeding in the urinary tract. Presence of RBCs should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of RBCs is generally not a concern." 
    },
    "casts": {
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "casts/µL",
        "explanation": "Casts in urine can indicate kidney issues. Presence of casts should be evaluated by a healthcare professional.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; absence of casts is generally not a concern." 
    },
    "bacterial_count": {
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
        "type": "hilo",
        "gender_specific": False,
        "range": (10, 22),
        "unit": "pmol/L",
        "explanation": "Free thyroxine (FT4) is a hormone produced by the thyroid gland. Abnormal levels can indicate thyroid dysfunction.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."    
    },
    "tsh": {
        "type": "hilo", 
        "gender_specific": False,
        "range": (0.4, 4.0),
        "unit": "mIU/L",
        "explanation": "Thyroid-stimulating hormone (TSH) regulates thyroid function. Abnormal levels can indicate thyroid dysfunction.",   
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."
    },
    "ft3": {
        "type": "hilo",
        "gender_specific": False,
        "range": (3.5, 6.5),
        "unit": "pmol/L",
        "explanation": "Free triiodothyronine (FT3) is a hormone produced by the thyroid gland. Abnormal levels can indicate thyroid dysfunction.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."    
    }
}

CANCER_MARKERS = {
    "ca_125": {
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 35),
        "unit": "U/mL",
        "explanation": "CA 125 is a tumor marker often used to monitor ovarian cancer. Elevated levels may indicate cancer or other conditions. Note that CA_125 is not a reliable marker for those without ovaries.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; normal levels are generally not a concern." 
    },
    "psa": {
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 4),
        "unit": "ng/mL",
        "explanation": "Prostate-specific antigen (PSA) is a tumor marker used to screen for prostate cancer. Elevated levels may indicate cancer or other prostate conditions. Note that PSA is not a reliable marker for those without a prostate.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "No specific advice; low levels are generally not a concern."
    }
}

VITAMINS = {
    "ab12": {
        "type": "hilo",
        "gender_specific": False,
        "range": (130, 700),
        "unit": "pmol/L",
        "explanation": "Vitamin B12 is essential for neurological function and the production of DNA and red blood cells. Deficiency can lead to anemia and neurological problems.",    
        "advice_high": "Consult a healthcare professional for further evaluation.", 
        "advice_low": "Consult a healthcare professional for further evaluation."
    },
    "folate": {
        "type": "lower_bound",
        "gender_specific": False,
        "range": (7, 100),
        "unit": "nmol/L",
        "explanation": "Folate (vitamin B9) is essential for DNA synthesis and cell division. Deficiency can lead to anemia and birth defects during pregnancy.",    
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

def interpret_result(metric_name, value, unit):
    """
    Interprets a single blood test result based on the defined data.
    Returns a tuple: (status, explanation, advice)
    """
    
    # 1. Standardize the metric name for lookup
    metric_name = metric_name.lower().replace(' ', '_')
    
    # 2. Check if the metric is known
    if metric_name not in BLOOD_METRIC_DATA:
        return ("Unknown", "This metric is not yet in our database.", "Consult your doctor for interpretation.")

    data = BLOOD_METRIC_DATA[metric_name]
    low_end, high_end = data["range"]
    
    # 3. Simple interpretation logic
    if value < low_end:
        status = "Low"
        advice = data.get("advice_low", "See a healthcare professional for specific advice.")
    elif value > high_end:
        status = "High"
        advice = data.get("advice_high", "See a healthcare professional for specific advice.")
    else:
        status = "Normal"
        advice = "Maintain your current healthy lifestyle."

    explanation = data["explanation"]
    
    return status, explanation, advice