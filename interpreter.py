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
        "explanation": "Blood pressure is the force your blood exerts on the walls of your arteries as it flows through them. It's written as two numbers: the top number (systolic) is the pressure when your heart squeezes to pump blood out, and the bottom number (diastolic) is the pressure when your heart relaxes between beats. Together, these two numbers give a picture of how hard your heart is working and how much resistance your arteries are putting up. Blood pressure naturally fluctuates throughout the day depending on activity, stress, and even the time of day, so a single reading isn't always the full story.",
        "advice_high": "A raised reading doesn't necessarily mean you have a problem, especially if it was taken when you were feeling anxious or rushed. That said, consistently elevated blood pressure is worth addressing because over time it puts extra strain on your heart and blood vessels. Practical steps include reducing your salt intake (aim for less than 6g a day), eating more fruit, vegetables, and whole grains, staying physically active (even regular brisk walking helps), limiting alcohol, and finding ways to manage stress. If your reading remains high across multiple checks, speak with your GP, as medication may be appropriate alongside these lifestyle changes.",
        "advice_low": "Low blood pressure is often harmless and some people naturally run on the lower side without any symptoms. However, if you're experiencing dizziness, lightheadedness, or fainting, it's worth looking into. Make sure you're drinking enough water throughout the day, eating regular meals, and getting up slowly from sitting or lying positions. If symptoms persist, your GP can help identify whether there's an underlying cause and whether any adjustments to diet, fluid intake, or medication are needed."
    },
    "pulse_rate": {
        "name": "Pulse Rate",
        "type": "hilo",
        "gender_specific": False,
        "range": (60, 100),  # Normal resting heart rate in bpm
        "unit": "bpm",
        "explanation": "Your pulse rate is the number of times your heart beats in one minute while you're at rest. It reflects how efficiently your heart is pumping blood around your body. A lower resting heart rate generally suggests your heart is working efficiently, which is why fit athletes often have rates in the 40s or 50s. Your pulse can be temporarily raised by caffeine, stress, illness, or recent physical activity, so context matters when interpreting this number.",
        "advice_high": "A resting heart rate above the normal range can sometimes reflect dehydration, stress, caffeine, lack of sleep, or recent illness rather than anything serious. If it's consistently elevated without an obvious explanation, it's worth mentioning to your GP. Regular cardiovascular exercise (like walking, cycling, or swimming) tends to bring resting heart rate down over time. Reducing caffeine and practising relaxation or breathing techniques can also help.",
        "advice_low": "A low resting heart rate is common in people who are physically fit, and in that context it's usually a sign of a healthy, efficient heart. However, if you're not particularly active and your heart rate is low, or if you're experiencing dizziness, fatigue, or fainting, it's worth checking in with a doctor. Some medications (like beta-blockers) can also lower heart rate, so mention any medicines you're taking."
    },
    "bmi": {
        "name": "Body Mass Index (BMI)",
        "type": "hilo",
        "gender_specific": False,
        "range": (18.5, 24.9),  # Normal BMI range
        "unit": "kg/m²",
        "explanation": "BMI is a simple calculation that uses your height and weight to estimate whether you're carrying a healthy amount of body weight. It's a useful screening tool, but it has limitations: it doesn't distinguish between muscle and fat, so very muscular people can have a high BMI without carrying excess fat. It also doesn't tell you where your fat is distributed, which matters because fat around the middle carries more health risk than fat elsewhere. Your doctor will usually consider BMI alongside other measurements.",
        "advice_high": "A BMI above the normal range suggests you may be carrying more weight than is ideal for your height. This doesn't mean you need to go on a crash diet. Gradual, sustainable changes tend to work best: increasing your activity levels, eating more vegetables and whole foods, reducing processed foods and sugary drinks, and watching portion sizes. Even a modest weight loss of 5-10% of your body weight can meaningfully improve blood pressure, blood sugar, and cholesterol. If you're muscular and active, your BMI may overstate the picture, so discuss it with your GP in the context of your other results.",
        "advice_low": "A BMI below the normal range means you may be underweight for your height. This can happen for many reasons, including a naturally slight build, high activity levels, stress, or not eating enough. Being underweight can affect your energy levels, immune function, and bone health over time. Try to include calorie-dense, nutritious foods in your diet (nuts, avocados, whole grains, dairy), eat regularly rather than skipping meals, and consider adding some resistance or strength training to build muscle. If you've lost weight unintentionally, it's a good idea to speak with your GP."
    },
    "muscle_mass": {
        "name": "Muscle Mass",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (30, 100),  # Example range in %
        "unit": "%",
        "explanation": "This measures how much of your total body weight is made up of skeletal muscle, the muscles you use to move, lift, and support your frame. Higher muscle mass is generally a good sign: it's linked to a faster metabolism, better blood sugar control, stronger bones, and greater physical resilience as you age. Muscle mass naturally tends to decline from your 30s onwards (a process called sarcopenia), which is why maintaining it matters at every stage of life.",
        "advice_high": "A high muscle mass reading is positive. Keep doing what you're doing: staying active, eating enough protein, and including resistance or strength-based exercise in your routine.",
        "advice_low": "Lower muscle mass can result from a sedentary lifestyle, insufficient protein intake, or natural age-related decline. The good news is that muscle responds well to training at any age. Incorporating resistance exercises (bodyweight exercises, free weights, resistance bands, or gym machines) two to three times a week, alongside adequate protein (roughly 1.2-1.6g per kg of body weight daily, spread across meals), can make a real difference. If you're new to exercise, start gently and build up gradually."
    },
    "average_peak_flow": {
        "name": "Average Peak Flow",
        "type": "lower_bound",
        "range": (300, 700),  # Example range in L/min
        "unit": "L/min",
        "explanation": "Peak flow measures the fastest rate at which you can blow air out of your lungs in a single, sharp breath. It's a snapshot of how open your airways are and how well your lungs are functioning. It's commonly used to monitor conditions like asthma, but it's also a useful general indicator of respiratory health. Your expected peak flow depends on your age, height, and sex, so the number is most meaningful when compared against what's predicted for someone like you.",
        "advice_high": "A high peak flow reading is generally a good sign and suggests your airways are open and your lungs are functioning well. Keep up regular physical activity and avoid smoking or prolonged exposure to air pollution to maintain your lung health.",
        "advice_low": "A low peak flow reading suggests your airways may be narrower than expected, which could be due to asthma, a respiratory infection, or another condition affecting your lungs. If this is a new finding, or if you're experiencing shortness of breath, wheezing, or chest tightness, speak with your GP. They may want to do further breathing tests or review any existing treatment you're on. Regular exercise, avoiding smoking, and minimising exposure to allergens and pollutants all support better lung function."
    },
    "body_fat_percentage": {
        "name": "Body Fat Percentage",
        "type": "hilo",
        "gender_specific": True,
        "range": (10, 32, 10, 25),  # Example range in %
        "unit": "%",
        "explanation": "Body fat percentage tells you how much of your total body weight is fat versus lean tissue (muscle, bone, organs, water). Everyone needs some body fat for energy storage, hormone production, insulation, and protecting organs, so having zero fat isn't the goal. What matters is being within a healthy range. Women naturally carry more essential fat than men (for reproductive and hormonal reasons), which is why the healthy ranges differ between sexes. Where your fat sits also matters: fat around the abdomen carries more health risk than fat on the hips and thighs.",
        "advice_high": "A body fat percentage above the healthy range means your body is storing more fat than is ideal. This can gradually increase risk factors for conditions like type 2 diabetes, heart disease, and joint problems. The most effective approach combines regular physical activity (both cardiovascular exercise and resistance training) with a balanced diet that's rich in whole foods and moderate in portion size. Resistance training is especially helpful because building muscle raises your resting metabolic rate, making it easier to manage body fat over time. Aim for gradual, sustainable change rather than drastic cuts.",
        "advice_low": "A body fat percentage below the healthy range means your body may not have enough fat reserves to support normal hormone production, immune function, and energy needs. This can affect your menstrual cycle (for women), bone density, and overall energy levels. Make sure you're eating enough to support your activity levels, including healthy fats from sources like nuts, seeds, olive oil, oily fish, and avocados. If you're doing a lot of endurance exercise, you may need more calories than you think. If your body fat is low and you're experiencing fatigue, frequent illness, or hormonal changes, speak with your GP."
    },
    "blood_oxygen_saturation": {
        "name": "Blood Oxygen Saturation",
        "type": "lower_bound",
        "range": (92, 100),  # Normal SpO2 range in %
        "unit": "%",
        "explanation": "Blood oxygen saturation (SpO2) tells you what percentage of your haemoglobin (the oxygen-carrying protein in red blood cells) is currently loaded with oxygen. Healthy lungs and a well-functioning circulatory system keep this number above 95% in most people. It's usually measured with a pulse oximeter clipped to your finger. Readings can be temporarily affected by cold hands, nail polish, or poor circulation to the fingertips, so a single slightly low reading isn't always cause for concern.",
        "advice_high": "An oxygen saturation in the normal range or slightly above is exactly what you'd hope to see. Keep supporting your lung and heart health with regular physical activity and by avoiding smoking.",
        "advice_low": "A low oxygen saturation reading means your blood isn't carrying as much oxygen as it should be. This can happen with respiratory conditions (like asthma, COPD, or pneumonia), heart problems, or at high altitude. If your reading is consistently below 95%, or if you're experiencing breathlessness, confusion, or a bluish tinge to your lips or fingertips, contact your GP or seek medical attention promptly. If the reading was a one-off, try warming your hands and retesting. Mention the result at your next appointment either way."
    },
    "qrisk_score": {
        "name": "QRISK Score",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 20),  # Example range in %
        "unit": "%",
        "explanation": "Your QRISK score is an estimate of your percentage chance of having a heart attack or stroke within the next 10 years. It's calculated using a combination of factors including your age, sex, blood pressure, cholesterol, smoking status, diabetes status, BMI, family history of heart disease, and ethnicity. A score of 10%, for example, means that out of 100 people with a similar profile, roughly 10 would be expected to have a cardiovascular event over the next decade. It's a risk estimate, not a prediction of what will happen to you personally.",
        "advice_high": "A higher QRISK score means you have more risk factors for heart disease and stroke, but many of these factors are things you can influence. The most impactful changes include stopping smoking (the single biggest thing you can do), being physically active for at least 150 minutes a week, eating a diet rich in vegetables, fruit, whole grains, and oily fish while limiting saturated fat and salt, keeping alcohol moderate, and managing stress. Your GP may also discuss whether medication (such as statins or blood pressure tablets) would be appropriate given your overall profile. Even modest improvements across several risk factors can meaningfully lower your score.",
        "advice_low": "A low QRISK score is reassuring and suggests your current risk of a heart attack or stroke over the next 10 years is relatively small. Continue with your current healthy habits. It's still worth being mindful of the basics: staying active, eating well, not smoking, and keeping an eye on your blood pressure and cholesterol over time."
    }
}

FULL_BLOOD_COUNT = {
    "haemoglobin": {
        "name": "Haemoglobin",
        "type": "hilo",
        "gender_specific": True,
        "range": (120, 150, 130, 170),  #
        "unit": "g/L",
        "explanation": "Haemoglobin is the protein inside your red blood cells that picks up oxygen in your lungs and delivers it to every tissue in your body. It's also what gives blood its red colour. Your haemoglobin level is one of the most important numbers in a blood test because it tells you whether your blood can carry enough oxygen to meet your body's needs. Men typically have slightly higher levels than women, partly due to hormonal differences and partly because menstruation causes regular iron loss.",
        "advice_high": "Elevated haemoglobin means your blood is thicker than usual, which can sometimes happen due to dehydration, smoking, living at high altitude, or conditions that cause your body to produce extra red blood cells. Make sure you're drinking enough water and mention this result to your GP, especially if you smoke or have been experiencing headaches, dizziness, or itching after hot baths. Your doctor may want to repeat the test or investigate further if the level is persistently high.",
        "advice_low": "Low haemoglobin is the hallmark of anaemia, which means your blood isn't carrying enough oxygen. This can leave you feeling tired, short of breath, pale, or dizzy. The most common cause is iron deficiency, especially in women with heavy periods, but it can also result from low vitamin B12 or folate, chronic conditions, or blood loss you may not be aware of. Eating iron-rich foods (red meat, dark leafy greens, lentils, fortified cereals) alongside vitamin C (which helps iron absorption) is a good start. Your GP will likely want to investigate the cause and may recommend supplements or further tests."
    },
    "red_blood_cell_count": {
        "name": "Red Blood Cell Count",
        "type": "hilo",
        "gender_specific": True,
        "range": (3.8, 4.8, 4.7, 6.1),
        "unit": "x10¹²/L",
        "explanation": "This counts the total number of red blood cells in a given volume of your blood. Red blood cells are produced in your bone marrow and live for about 120 days before being broken down and replaced. Their primary job is carrying oxygen from your lungs to your tissues and bringing carbon dioxide back to be exhaled. The count is closely related to your haemoglobin level, but looking at both together (along with other red cell indices) gives your doctor a more complete picture of how your blood is functioning.",
        "advice_high": "A high red blood cell count means your body is producing more red cells than usual. This can be a response to smoking, dehydration, living at altitude, or chronic lung conditions that reduce oxygen levels. In rarer cases, it can point to a bone marrow condition called polycythaemia. Stay well hydrated, and if you smoke, consider stopping. Mention this result to your GP, who may want to investigate further if it persists.",
        "advice_low": "A low red blood cell count suggests your body either isn't making enough red cells or is losing or destroying them faster than normal. Common causes include iron, B12, or folate deficiency, chronic illness, and blood loss. You may feel tired, weak, or short of breath. Focus on eating a nutrient-rich diet with plenty of iron and B vitamins, and speak with your GP to identify the underlying cause. They may recommend supplements or further blood tests."
    },
    "hct": {
        "name": "Haematocrit (HCT)",
        "type": "hilo",
        "gender_specific": True,
        "range": (36, 46, 40, 54),
        "unit": "%",
        "explanation": "Haematocrit measures the proportion of your blood that's made up of red blood cells, expressed as a percentage. The rest of your blood is plasma (the liquid part), white blood cells, and platelets. Think of it as a measure of how 'concentrated' your red blood cells are. It moves in the same direction as your haemoglobin and red cell count, so doctors look at all three together to get the full picture.",
        "advice_high": "A high haematocrit means a larger-than-normal share of your blood volume is red blood cells. Dehydration is the most common cause (because less plasma makes the red cells more concentrated), but it can also result from smoking, lung disease, or bone marrow conditions. Drink plenty of fluids and mention this to your GP if it's a persistent finding, especially if combined with high haemoglobin.",
        "advice_low": "A low haematocrit means your red blood cells make up a smaller proportion of your blood than expected, which usually goes hand-in-hand with anaemia. Causes include iron, B12, or folate deficiency, chronic illness, or blood loss. The advice here mirrors that for low haemoglobin: focus on a nutrient-rich diet, and speak with your GP to find and address the underlying cause."
    },
    "mcv": {
        "name": "Mean Corpuscular Volume",
        "type": "hilo",
        "gender_specific": False,
        "range": (83, 101),
        "unit": "fL",
        "explanation": "MCV tells you the average size of your red blood cells. This is useful because the size of your red cells can point to the cause of anaemia or other blood conditions. Normal-sized cells are called normocytic, unusually large cells are macrocytic, and unusually small cells are microcytic. Your doctor uses MCV alongside other indices (like MCH and MCHC) to narrow down what might be going on.",
        "advice_high": "Larger-than-normal red blood cells (macrocytosis) are most commonly caused by vitamin B12 or folate deficiency, but can also be related to excess alcohol intake, certain medications, or thyroid problems. Make sure your diet includes good sources of B12 (meat, fish, eggs, dairy) and folate (leafy greens, legumes, fortified cereals). If you drink alcohol regularly, reducing your intake may help. Your GP will likely want to check your B12, folate, and thyroid levels to pinpoint the cause.",
        "advice_low": "Smaller-than-normal red blood cells (microcytosis) are most commonly caused by iron deficiency, though they can also occur with thalassaemia trait (a genetic condition that's common in certain ethnic groups) or chronic illness. Include iron-rich foods in your diet (red meat, lentils, dark leafy greens) and pair them with vitamin C to boost absorption. Your GP may check your iron levels and possibly arrange further tests if iron deficiency isn't the explanation."
    },
    "mch": {
        "name": "Mean Corpuscular Haemoglobin",
        "type": "hilo",
        "gender_specific": False,
        "range": (27, 32),
        "unit": "pg",
        "explanation": "MCH tells you the average amount of haemoglobin inside each individual red blood cell. Since haemoglobin is what carries oxygen, this number helps your doctor understand how well-equipped each red cell is to do its job. MCH tends to move in the same direction as MCV (cell size), because bigger cells usually contain more haemoglobin and smaller cells contain less.",
        "advice_high": "A high MCH usually goes along with large red blood cells (high MCV) and points towards the same causes: vitamin B12 or folate deficiency, excess alcohol, or thyroid issues. The advice is the same too: ensure adequate B12 and folate through your diet or supplements, moderate alcohol, and speak with your GP to investigate further.",
        "advice_low": "A low MCH means your red blood cells are carrying less haemoglobin than normal, which typically happens alongside small red cells (low MCV). Iron deficiency is the most common reason. Focus on iron-rich foods, consider taking iron with vitamin C to improve absorption, and talk to your GP about whether supplements or further investigation are needed."
    },
    "mchc": {
        "name": "Mean Corpuscular Haemoglobin Concentration (MCHC)",
        "type": "hilo",
        "gender_specific": False,
        "range": (315, 345),
        "unit": "g/L",
        "explanation": "MCHC measures the average concentration of haemoglobin within your red blood cells. While MCH tells you the total amount of haemoglobin per cell, MCHC tells you how densely packed that haemoglobin is relative to the cell's size. It's another piece of the puzzle your doctor uses alongside MCV and MCH to work out what type of anaemia or blood condition might be present.",
        "advice_high": "A high MCHC is relatively uncommon and can occur with conditions like hereditary spherocytosis (where red blood cells are an unusual shape) or severe dehydration. It can also sometimes be a lab artefact. Mention this result to your GP, who can assess whether further testing is needed based on your other blood results and symptoms.",
        "advice_low": "A low MCHC means your red blood cells contain less haemoglobin than expected for their size. This is often seen with iron deficiency anaemia or thalassaemia trait. Improving your iron intake through diet (red meat, pulses, green vegetables) and potentially supplements can help if iron deficiency is the cause. Your GP will be able to advise based on the full picture of your blood results."
    },
    "rdw": {
        "name": "Red Cell Distribution Width (RDW)",
        "type": "hilo", 
        "gender_specific": False,
        "range": (11.6, 14),
        "unit": "%",
        "explanation": "RDW measures how much variation there is in the size of your red blood cells. In a healthy person, red blood cells are all roughly the same size. A wider distribution (higher RDW) means there's a bigger mix of large and small cells, which can help your doctor identify the type and cause of anaemia. It's especially useful when your MCV is borderline or normal but something still doesn't look right.",
        "advice_high": "A high RDW means your red blood cells vary more in size than expected. This is commonly seen with iron deficiency (where new, smaller cells are being made alongside older, normal-sized ones), but can also occur with B12 or folate deficiency, or after a blood transfusion. On its own, a high RDW isn't a diagnosis, but it's a clue that prompts your doctor to look at your other blood results more closely. Ensure you're getting adequate iron, B12, and folate in your diet, and discuss the finding with your GP.",
        "advice_low": "A low RDW simply means your red blood cells are very uniform in size, which is generally normal and not a cause for concern."
    },
    "platelets": {
        "name": "Platelet Count",
        "type": "hilo",
        "gender_specific": False,
        "range": (150, 410),
        "unit": "x10⁹/L",
        "explanation": "Platelets are tiny cell fragments made in your bone marrow. Their main job is to help your blood clot when you cut or injure yourself. They rush to the site of damage, stick together, and form a plug to stop the bleeding. Your platelet count tells your doctor whether you have enough of these clotting helpers, or too many, which can both cause problems in different ways.",
        "advice_high": "A high platelet count (thrombocytosis) can be a temporary response to infection, inflammation, surgery, or iron deficiency. In these cases it usually settles on its own once the underlying trigger resolves. Less commonly, it can be related to a bone marrow condition. Your GP will interpret this alongside your other results and symptoms. In the meantime, staying hydrated and active is sensible, as these support healthy circulation.",
        "advice_low": "A low platelet count (thrombocytopenia) means your blood may not clot as effectively, which can lead to easier bruising, longer bleeding from cuts, or in more pronounced cases, tiny red or purple spots on the skin. Common causes include viral infections, certain medications, alcohol, and autoimmune conditions. If your count is mildly low and you feel well, it may just need monitoring. Avoid aspirin and ibuprofen (which can further affect clotting) unless your GP advises otherwise, and mention this result at your next appointment."
    },
    "mpv": {
        "name": "Mean Platelet Volume (MPV)",
        "type": "hilo",
        "gender_specific": False,
        "range": (7.1, 10.1),
        "unit": "fL",
        "explanation": "MPV tells you the average size of your platelets. Younger, freshly made platelets tend to be larger and more active, while older ones are smaller. So MPV gives your doctor a sense of how quickly your bone marrow is producing new platelets and how active your clotting system is. It's most useful when interpreted alongside your platelet count.",
        "advice_high": "A high MPV means your platelets are larger than average, which often indicates your bone marrow is working hard to produce new platelets. This can happen when platelets are being used up or destroyed faster than normal (such as with immune conditions or after blood loss), or alongside inflammatory conditions. On its own it's rarely a concern, but your GP will consider it in the context of your full blood count.",
        "advice_low": "A low MPV means your platelets are smaller than average, which can sometimes be seen with bone marrow conditions that affect platelet production, or with certain inflammatory disorders. It's a subtle finding and usually only meaningful alongside other abnormal results. Mention it to your GP if your platelet count is also outside the normal range."
    },
    "white_blood_cell_count": {
        "name": "White Blood Cell Count",
        "type": "hilo",
        "gender_specific": False,
        "range": (4.0, 10.0),
        "unit": "x10⁹/L",
        "explanation": "White blood cells are your immune system's frontline defence. They patrol your bloodstream looking for bacteria, viruses, fungi, and other threats, and they coordinate the immune response when something harmful is detected. Your total white cell count gives an overall picture of immune activity, but the different types of white cells (neutrophils, lymphocytes, monocytes, eosinophils, basophils) each have different roles, so doctors often look at the breakdown too.",
        "advice_high": "A high white blood cell count most commonly means your immune system is actively fighting something, like an infection, inflammation, or allergic reaction. Stress, smoking, and strenuous exercise can also temporarily raise the count. It usually comes back down once the trigger resolves. If your count is persistently elevated without an obvious cause, your GP may want to do follow-up tests to understand why.",
        "advice_low": "A low white blood cell count means your body has fewer immune cells available to fight infections. This can happen with certain viral infections, some medications (including chemotherapy), autoimmune conditions, or bone marrow problems. If your count is mildly low and you feel well, it may just be your normal baseline, as some people naturally run on the lower end. Practice good hygiene (regular handwashing, food safety), keep up to date with vaccinations, and let your GP know so they can decide whether monitoring or further tests are needed." 
    },
    "neutrophils": {
        "name": "Neutrophils",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.0, 7.0),
        "unit": "x10⁹/L",
        "explanation": "Neutrophils are the most abundant type of white blood cell, typically making up 40-70% of the total. They're the first responders of your immune system, arriving quickly at the site of an infection to engulf and destroy bacteria and fungi. Because they react so rapidly, neutrophil levels are often one of the first things to change when an infection or inflammation is present.",
        "advice_high": "Elevated neutrophils (neutrophilia) usually mean your body is responding to a bacterial infection, inflammation, physical stress, or injury. Smoking can also raise neutrophil counts. This is typically a normal, healthy immune response, and levels usually return to normal once the underlying cause resolves. If the elevation persists without a clear trigger, your GP may investigate further.",
        "advice_low": "Low neutrophils (neutropenia) reduce your body's ability to fight off bacterial infections. This can be caused by viral infections, certain medications, autoimmune conditions, or bone marrow issues. Mild neutropenia is common and often temporary. Some ethnic groups (particularly people of African, Middle Eastern, or West Indian heritage) naturally have lower neutrophil counts without any increased infection risk, a condition called benign ethnic neutropenia. If your count is low, practise good hygiene, avoid close contact with people who are unwell, and mention the result to your GP." 
    },
    "lymphocytes": {
        "name": "Lymphocytes",
        "type": "hilo",
        "gender_specific": False,
        "range": (1.0, 3.0),
        "unit": "x10⁹/L",
        "explanation": "Lymphocytes are white blood cells that form the backbone of your adaptive immune system. There are several types: B cells produce antibodies to tag invaders, T cells directly attack infected cells and coordinate the immune response, and natural killer cells destroy virus-infected or abnormal cells. Lymphocytes are also responsible for immune memory, which is why you can become immune to certain infections after having them once or being vaccinated.",
        "advice_high": "Elevated lymphocytes (lymphocytosis) are very commonly seen during or after viral infections like colds, flu, glandular fever, or COVID-19. This is your immune system doing its job. Chronic stress or smoking can also play a role. The count usually returns to normal within a few weeks. If lymphocytes remain persistently elevated without an obvious infection, your GP may want to investigate further, but in most cases this is a normal immune response.",
        "advice_low": "Low lymphocytes (lymphopenia) can occur during or after certain viral infections (including HIV and COVID-19), with some autoimmune conditions, or as a side effect of medications like corticosteroids or immunosuppressants. Severe stress or malnutrition can also be factors. A mildly low count often resolves on its own. Supporting your immune system through a balanced diet, adequate sleep, regular exercise, and stress management is always sensible. Mention this result to your GP, especially if it's a recurring finding."
    },
    "monocytes": {
        "name": "Monocytes",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.2, 1.0),
        "unit": "x10⁹/L",
        "explanation": "Monocytes are white blood cells that act as your immune system's cleanup crew. They move into tissues and transform into macrophages, which engulf and digest dead cells, bacteria, and other debris. They also play a role in presenting fragments of invaders to other immune cells, helping to coordinate the broader immune response. They typically make up a small percentage of your total white blood cells.",
        "advice_high": "Elevated monocytes (monocytosis) often reflect a chronic infection, an inflammatory condition, or the recovery phase after an acute infection. They can also be raised in autoimmune disorders or, rarely, certain blood cancers. A mildly elevated count after a recent illness is usually nothing to worry about and tends to settle on its own. If the elevation persists, your GP may want to look into it further.",
        "advice_low": "Low monocytes are uncommon and usually only significant in the context of an overall low white cell count. They can occasionally be seen with certain bone marrow conditions or as a side effect of some medications. A mildly low monocyte count on its own, with everything else normal, is rarely a concern. Mention it to your GP if other white cell types are also low."
    },
    "eosinophils": {
        "name": "Eosinophils",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.02, 0.5),
        "unit": "x10⁹/L",
        "explanation": "Eosinophils are specialised white blood cells involved in fighting parasitic infections and in allergic and inflammatory responses. They make up a small proportion of your total white cells but can increase dramatically in response to allergens, parasites, or certain inflammatory conditions. They release chemicals that help control inflammation but can also cause tissue damage if they're overactive.",
        "advice_high": "Elevated eosinophils (eosinophilia) are most commonly caused by allergies (hay fever, eczema, asthma), food sensitivities, or parasitic infections. Certain medications and autoimmune conditions can also raise the count. If you have known allergies, managing them effectively (with antihistamines, avoiding triggers, or speaking to your GP about treatment) may help bring the count down. If you've recently travelled to a tropical region, mention this to your doctor as parasitic infections should be considered.",
        "advice_low": "Low eosinophils are normal and generally not a concern. The count is naturally low in most healthy people." 
    },
    "basophils": {
        "name": "Basophils",    
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.02, 0.1),
        "unit": "x10⁹/L",
        "explanation": "Basophils are the least common type of white blood cell, normally making up less than 1% of the total. They play a role in allergic reactions and inflammation by releasing histamine and other chemicals. Despite their small numbers, they contribute to the body's defence against parasites and help regulate the inflammatory response.",
        "advice_high": "Elevated basophils (basophilia) can occur with allergic reactions, chronic inflammatory conditions, certain infections, or thyroid problems. On its own, a mildly raised basophil count is rarely significant and is usually interpreted alongside your other results. If you have allergies, managing them well may help. Mention the finding to your GP if it persists or if other white cell types are also abnormal.",
        "advice_low": "Low basophils are very common and entirely normal. Because the baseline count is already so small, a low reading carries no clinical significance in the vast majority of cases." 
    },
}

KIDNEY_FUNCTION = {
    "sodium": {
        "name": "Sodium",
        "type": "hilo",
        "gender_specific": False,
        "range": (133, 146),
        "unit": "mmol/L",
        "explanation": "Sodium is an electrolyte that your body uses to control fluid balance, maintain blood pressure, and keep nerves and muscles working properly. Your kidneys are the main regulators, adjusting how much sodium is retained or excreted in urine depending on what your body needs. Most of the sodium in our diet comes from salt in food.",
        "advice_high": "High sodium (hypernatraemia) usually means your body has lost more water than salt, which most commonly happens with dehydration (not drinking enough, excessive sweating, vomiting, or diarrhoea). It can also occur if you're eating a very salty diet or taking certain medications. The simplest first step is to increase your water intake and cut back on processed and salty foods. If symptoms like confusion, excessive thirst, or muscle twitching are present, seek medical advice promptly.",
        "advice_low": "Low sodium (hyponatraemia) means there's too much water relative to sodium in your blood. This can happen from drinking excessive amounts of water, from certain medications (particularly diuretics and some antidepressants), or from conditions affecting the kidneys, liver, or hormones. Mild cases may cause no symptoms, but lower levels can cause nausea, headaches, confusion, or fatigue. Don't try to fix this by simply eating more salt without medical guidance. Speak with your GP, who can identify the cause and advise appropriately." 
    },
    "potassium": {
        "name": "Potassium",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.5, 5.3),
        "unit": "mmol/L",
        "explanation": "Potassium is an electrolyte that's essential for your heart, muscles, and nerves to function properly. It works closely with sodium to maintain fluid balance and helps regulate your heartbeat. Your kidneys control potassium levels by adjusting how much is excreted in urine. Even small shifts outside the normal range can affect how your heart and muscles behave, which is why doctors pay close attention to this number.",
        "advice_high": "High potassium (hyperkalaemia) can affect your heart rhythm, so it's taken seriously. Common causes include kidney problems, certain medications (ACE inhibitors, potassium-sparing diuretics, some anti-inflammatories), and occasionally a diet very high in potassium-rich foods. It's also one of the most commonly falsely elevated results in blood tests, because if the sample is squeezed too hard during collection or left too long before processing, potassium leaks out of red blood cells. Your GP may want to recheck the level before taking action. In the meantime, avoid potassium supplements and be mindful of very high-potassium foods like bananas, dried fruit, and potatoes if your level is significantly raised.",
        "advice_low": "Low potassium (hypokalaemia) can cause muscle weakness, cramps, fatigue, and in more severe cases, heart rhythm disturbances. It's often caused by vomiting, diarrhoea, excessive sweating, or diuretic medications. Eating potassium-rich foods (bananas, oranges, potatoes, spinach, avocados, yoghurt) can help bring mild deficiency back up. If your level is significantly low or you're on diuretics, your GP may recommend a potassium supplement or adjust your medication." 
    },
    "urea": {
        "name": "Urea",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.2, 8.2),
        "unit": "mmol/L",
        "explanation": "Urea is a waste product that your liver creates when it breaks down protein. It travels through your blood to the kidneys, which filter it out and excrete it in urine. Measuring urea gives your doctor a rough indicator of how well your kidneys are working and can also reflect how much protein you're eating or how hydrated you are.",
        "advice_high": "A raised urea level can mean your kidneys aren't filtering as efficiently as they should, but it can also simply reflect dehydration or a high-protein diet. Intense exercise, certain medications, and gastrointestinal bleeding can raise it too. Make sure you're drinking enough water and mention this result to your GP, especially if your creatinine is also elevated. They'll be able to tell whether your kidney function needs further assessment.",
        "advice_low": "A low urea level is less commonly a concern. It can occur with a low-protein diet, liver disease (since the liver produces urea), overhydration, or during pregnancy. If your diet is very low in protein, ensuring you're getting enough from sources like meat, fish, eggs, dairy, legumes, or tofu may help. Mention it to your GP if other liver or kidney markers are also outside the normal range." 
    },
    "creatinine": {
        "name": "Creatinine",
        "type": "hilo",
        "gender_specific": True,
        "range": (49, 90, 62, 115),
        "unit": "µmol/L",
        "explanation": "Creatinine is a waste product generated by normal muscle activity. Your muscles break down a compound called creatine for energy, and creatinine is the byproduct. It's produced at a fairly constant rate and filtered out by the kidneys, which makes it a reliable marker of kidney function. Because men typically have more muscle mass than women, the normal range differs between the sexes. People who are very muscular may naturally have higher creatinine levels without any kidney problem.",
        "advice_high": "Elevated creatinine can indicate that your kidneys aren't filtering waste as efficiently as expected. However, it can also be temporarily raised by intense exercise, a high-protein meal before the test, certain supplements (like creatine), dehydration, or some medications. Your GP will usually look at creatinine alongside your eGFR (estimated glomerular filtration rate) to get a more accurate picture of kidney function. Stay well hydrated, and if the level is persistently elevated, your doctor may arrange further tests or a repeat blood draw.",
        "advice_low": "Low creatinine is less common and usually reflects lower muscle mass, which can occur with ageing, a very sedentary lifestyle, or certain conditions that cause muscle wasting. It can also be seen in pregnancy or with a very low-protein diet. On its own, a slightly low creatinine isn't usually a cause for concern, but if you've noticed a loss of muscle strength or unintentional weight loss, mention it to your GP."    
    }
}

HEART_HEALTH = {
    "cholesterol": {
        "name": "Cholesterol",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.5, 5.18),
        "unit": "mmol/L",
        "explanation": "Total cholesterol is the combined amount of all types of cholesterol in your blood. Cholesterol is a waxy, fat-like substance that your body actually needs for building cell membranes, making hormones, and producing vitamin D. Your liver makes most of your cholesterol; the rest comes from food. The total number on its own doesn't tell the full story, because it includes both 'good' (HDL) and 'bad' (LDL) cholesterol, which have opposite effects on heart health. Your doctor will look at the breakdown alongside this total.",
        "advice_high": "Elevated total cholesterol increases the risk of fatty deposits building up in your arteries over time, which can lead to heart disease and stroke. Dietary changes that help include reducing saturated fat (fatty cuts of meat, butter, cheese, pastries), eating more oily fish, nuts, seeds, and olive oil, increasing fibre intake (oats, beans, lentils, fruits, vegetables), and limiting alcohol. Regular physical activity raises HDL and improves the overall cholesterol profile. If lifestyle changes alone aren't enough, your GP may discuss statins or other medication depending on your overall cardiovascular risk.",
        "advice_low": "Very low total cholesterol is uncommon and usually only a concern if it's significantly below the range. It can occasionally be linked to malnutrition, liver problems, an overactive thyroid, or certain genetic conditions. If your other results and general health are fine, a slightly low reading is unlikely to be an issue. Mention it to your GP if you've had unintentional weight loss or other symptoms."
    },
    "triglycerides": {
        "name": "Triglycerides",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.4, 1.7),
        "unit": "mmol/L",
        "explanation": "Triglycerides are the most common type of fat in your blood. When you eat, your body converts calories it doesn't need right away into triglycerides and stores them in fat cells for energy later. Between meals, hormones trigger their release to fuel your body. Triglyceride levels are heavily influenced by what you've eaten recently (which is why you're sometimes asked to fast before a blood test), as well as by alcohol, sugar, and refined carbohydrate intake.",
        "advice_high": "Elevated triglycerides increase cardiovascular risk, often alongside other lipid abnormalities. The good news is that triglycerides respond well to lifestyle changes. Cutting back on sugar, refined carbohydrates (white bread, pastries, sugary drinks), and alcohol can bring them down noticeably. Increasing omega-3 fats from oily fish (salmon, mackerel, sardines) or supplements, exercising regularly, and losing excess weight all help too. If this test wasn't done fasting, your GP may want to recheck it after an overnight fast for a more accurate reading.",
        "advice_low": "Low triglycerides are generally a sign of good metabolic health and not a concern. Very low levels can occasionally be associated with a very low-fat diet, malabsorption, an overactive thyroid, or malnutrition, but this is uncommon. If you're eating a balanced diet and feeling well, there's nothing to worry about."
    },
    "hdl_cholesterol": {
        "name": "HDL Cholesterol",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (1.04, 100),
        "unit": "mmol/L",
        "explanation": "HDL (high-density lipoprotein) cholesterol is often called 'good' cholesterol because it works like a cleanup service for your arteries. HDL particles pick up excess cholesterol from your artery walls and carry it back to the liver, where it's broken down and removed from the body. Higher HDL levels are associated with a lower risk of heart disease. Regular exercise, healthy fats, and moderate alcohol intake tend to raise HDL, while smoking, excess sugar, and a sedentary lifestyle tend to lower it.",
        "advice_high": "A high HDL level is protective and something to be pleased about. Keep up the habits that are supporting it: regular exercise, a diet rich in healthy fats (olive oil, nuts, avocados, oily fish), not smoking, and maintaining a healthy weight.",
        "advice_low": "Low HDL means you have less of the 'cleanup' cholesterol working to remove excess fat from your artery walls, which can increase cardiovascular risk. The most effective ways to raise HDL are regular aerobic exercise (brisk walking, cycling, swimming for at least 30 minutes most days), eating more monounsaturated and polyunsaturated fats (olive oil, nuts, seeds, oily fish), quitting smoking, reducing refined carbohydrates and sugar, and maintaining a healthy weight. Even modest increases in HDL can make a meaningful difference."
    },
    "ldl_cholesterol": {
        "name": "LDL Cholesterol",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.5, 3.0),
        "unit": "mmol/L",
        "explanation": "LDL (low-density lipoprotein) cholesterol is often called 'bad' cholesterol because when there's too much of it, it can deposit into the walls of your arteries and form plaques. Over time, these plaques narrow the arteries and can eventually lead to heart attacks or strokes. LDL is influenced by diet (especially saturated fat), genetics, body weight, and physical activity. Many experts now consider LDL the single most important cholesterol number for assessing heart risk.",
        "advice_high": "Reducing LDL is one of the most effective things you can do for long-term heart health. Dietary changes that lower LDL include reducing saturated fat (less butter, cheese, fatty meat, coconut oil, pastries), eating more soluble fibre (oats, beans, lentils, apples, aubergine), adding plant sterols (found in fortified spreads and drinks), and eating nuts and oily fish regularly. Regular exercise and maintaining a healthy weight also help. If lifestyle changes aren't enough, or if your overall cardiovascular risk is elevated, your GP may recommend statins, which are very effective at lowering LDL.",
        "advice_low": "Low LDL cholesterol is generally considered beneficial for cardiovascular health. Very low levels are uncommon and can occasionally be associated with certain genetic conditions, liver issues, or malabsorption, but in most cases a low LDL is a positive finding. If you feel well and your other results are normal, no action is needed."
    },
    "tc_hdl_ratio": {
        "name": "Total Cholesterol to HDL Ratio",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 4.5),
        "unit": "",
        "explanation": "This ratio divides your total cholesterol by your HDL ('good') cholesterol. It's a quick way to gauge your cardiovascular risk because it captures both how much cholesterol you have overall and how much of the protective type is present. A lower ratio is better. For example, someone with a total cholesterol of 5.0 and HDL of 1.5 has a ratio of 3.3, which is favourable. The ratio can sometimes be more informative than total cholesterol alone.",
        "advice_high": "A high ratio means either your total cholesterol is too high, your HDL is too low, or both. The strategies for improving it overlap: increase physical activity (which raises HDL), eat more healthy fats and fibre while reducing saturated fat and refined carbohydrates, maintain a healthy weight, quit smoking, and moderate alcohol intake. Your GP may also consider medication if your overall cardiovascular risk warrants it.",
        "advice_low": "A low ratio is a positive sign of good cardiovascular health. It means you have a healthy balance of total cholesterol and protective HDL. Continue with the habits that are supporting this."   
    },
    "hdl_percentage_of_total_cholesterol": {
        "name": "HDL Percentage of Total Cholesterol",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (20, 100),
        "unit": "%",
        "explanation": "This shows what proportion of your total cholesterol is made up of HDL, the 'good' cholesterol that helps remove fat from your arteries. A higher percentage means more of your cholesterol is the protective kind. It's another way of looking at the same balance captured by the TC:HDL ratio, just expressed differently.",
        "advice_high": "A high HDL percentage is excellent and indicates your cholesterol profile is weighted towards the protective type. Keep up whatever you're doing: regular exercise, a diet rich in healthy fats, not smoking, and maintaining a healthy weight.",
        "advice_low": "A low HDL percentage means the protective fraction of your cholesterol is smaller than ideal. Boosting HDL through regular aerobic exercise, eating more healthy fats (olive oil, nuts, oily fish), quitting smoking, reducing sugar and refined carbs, and maintaining a healthy weight will improve this ratio over time."
    },
    "hs_crp": {
        "name": "High-sensitivity C-reactive Protein (hs-CRP)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 5.0),
        "unit": "mg/L",
        "explanation": "hs-CRP measures a protein called C-reactive protein that your liver produces in response to inflammation anywhere in the body. The 'high-sensitivity' version of this test can detect very low levels of CRP, which makes it useful for assessing chronic, low-grade inflammation linked to cardiovascular risk. It's not specific to the heart though, so any source of inflammation (an infection, an injury, an autoimmune condition, even intense exercise the day before) can raise it.",
        "advice_high": "An elevated hs-CRP suggests there's some degree of inflammation in your body. If you had an infection, injury, or illness around the time of the test, that's likely the explanation and the level will come down once you've recovered. If the elevation is persistent and unexplained, it may reflect chronic low-grade inflammation that contributes to cardiovascular risk. Regular exercise, a diet rich in fruits, vegetables, whole grains, and omega-3 fats, maintaining a healthy weight, not smoking, and managing stress all help reduce systemic inflammation. Your GP may want to retest once any acute causes have resolved.",
        "advice_low": "A low hs-CRP is a good sign and suggests minimal inflammation in your body. This is associated with a lower cardiovascular risk. Continue with healthy habits that support this."
    },
    "apolipoprotein_a1": {
        "name": "Apolipoprotein A1",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.76, 2.14),
        "unit": "g/L",
        "explanation": "Apolipoprotein A1 (ApoA1) is the main protein component of HDL ('good') cholesterol. It plays an active role in the process of reverse cholesterol transport, helping to pull cholesterol out of artery walls and ferry it back to the liver for disposal. Some researchers consider ApoA1 a more precise marker of cardiovascular protection than HDL cholesterol alone, because it directly measures the functional protein rather than just the cholesterol it carries.",
        "advice_high": "A high ApoA1 level is a positive finding and reflects good cardiovascular protection. Continue with the habits supporting it: regular physical activity, a diet rich in healthy fats, not smoking, and maintaining a healthy weight.",
        "advice_low": "Low ApoA1 suggests you may have less cardiovascular protection from your HDL system. The same lifestyle factors that raise HDL also raise ApoA1: regular aerobic exercise, eating healthy fats (olive oil, nuts, oily fish), quitting smoking, limiting sugar and refined carbohydrates, and keeping a healthy weight. Discuss this result with your GP, especially if other lipid markers are also unfavourable."
    },
    "apolipoprotein_b": {
        "name": "Apolipoprotein B",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.46, 1.42),
        "unit": "g/L",
        "explanation": "Apolipoprotein B (ApoB) is the main protein found on LDL ('bad') cholesterol particles, as well as on other atherogenic (artery-damaging) lipoproteins. Each of these harmful particles carries exactly one ApoB molecule, so measuring ApoB effectively counts the total number of potentially dangerous particles in your blood. Many cardiologists now view ApoB as a better predictor of heart disease risk than LDL cholesterol alone, because two people can have the same LDL cholesterol level but different numbers of particles.",
        "advice_high": "A high ApoB means you have a larger number of atherogenic particles circulating in your blood, which increases the risk of plaque building up in your arteries. The same strategies that lower LDL cholesterol also reduce ApoB: cutting saturated fat, eating more fibre, exercising regularly, maintaining a healthy weight, and not smoking. If your level is significantly elevated, your GP may discuss medication such as statins, which are very effective at reducing ApoB.",
        "advice_low": "A low ApoB is a favourable result, indicating fewer harmful cholesterol particles in your bloodstream. This is associated with lower cardiovascular risk. Continue with your current healthy habits."
    },
    "lipoprotein_a": {
        "name": "Lipoprotein(a)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0.0, 0.3),
        "unit": "g/L",
        "explanation": "Lipoprotein(a), often written as Lp(a), is a type of LDL-like particle with an extra protein (apolipoprotein(a)) attached. It's been linked to an increased risk of heart disease and stroke. What makes Lp(a) unusual is that your level is almost entirely determined by genetics, not by diet or lifestyle. It doesn't change much over your lifetime, so a single measurement is generally enough to know where you stand. Not everyone gets tested for Lp(a), so having this result gives your doctor an extra piece of the cardiovascular risk picture.",
        "advice_high": "An elevated Lp(a) is an inherited risk factor for cardiovascular disease, and because it's genetically determined, diet and exercise don't significantly change the level itself. However, this makes it all the more important to manage every other risk factor you can control: keeping LDL cholesterol low, maintaining a healthy blood pressure, not smoking, exercising regularly, and eating well. Discuss this result with your GP or a cardiologist, as they may want to take a more aggressive approach to managing your other lipid levels. Research into specific Lp(a)-lowering therapies is ongoing.",
        "advice_low": "A low Lp(a) is reassuring and means this particular genetic risk factor isn't contributing to your cardiovascular risk. No action is needed."
    },
    "apo_b_a1_ratio": {
        "name": "Apolipoprotein B/A1 Ratio",
        "type": "upper_bound",
        "gender_specific": True,
        "range": (0, 0.8, 0, 0.9),
        "unit": "ratio",
        "explanation": "The Apolipoprotein B/A1 ratio compares the amount of atherogenic (artery-damaging) ApoB particles against the cardioprotective ApoA1 particles. A lower ratio means relatively more protective HDL-associated particles compared to harmful ones, which is favourable. Many cardiologists consider this ratio one of the most informative single markers for cardiovascular risk, as it captures both sides of the equation simultaneously. The threshold differs slightly between men and women because women typically have higher ApoA1 levels.",
        "advice_high": "A high ApoB/A1 ratio means you have more harmful lipoprotein particles relative to protective ones, which increases cardiovascular risk. The most effective actions are the same as for managing LDL and HDL individually: reduce saturated fat, eat more fibre and healthy fats (olive oil, oily fish, nuts), exercise regularly, quit smoking, and maintain a healthy weight. These changes tend to lower ApoB and raise ApoA1 simultaneously, improving the ratio from both ends. If your ratio remains elevated after lifestyle changes, your GP may consider medication.",
        "advice_low": "A low ApoB/A1 ratio is a favourable finding, indicating a good balance between harmful and protective lipoproteins. Continue with the habits supporting this."
    },
    "non_hdl_cholesterol": {
        "name": "Non-HDL Cholesterol",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 3.36),
        "unit": "mmol/L",
        "explanation": "Non-HDL cholesterol is calculated by subtracting your HDL ('good') cholesterol from your total cholesterol. The result captures all the potentially atherogenic (artery-damaging) lipoproteins in a single number: LDL, VLDL, IDL, and lipoprotein(a). Some guidelines prefer it over LDL alone because it includes these other harmful particles. It's particularly useful when triglycerides are elevated, as high triglycerides can make LDL calculations less accurate.",
        "advice_high": "Elevated non-HDL cholesterol means the combined burden of harmful lipoproteins in your blood is higher than ideal, raising cardiovascular risk. The approach is the same as for reducing LDL: cut saturated fat, increase fibre and omega-3 fats, exercise regularly, avoid smoking, and maintain a healthy weight. If other risk factors are present, your GP may discuss lipid-lowering medication.",
        "advice_low": "A low non-HDL cholesterol is a positive finding, suggesting a low overall burden of atherogenic lipoproteins. Continue with healthy habits."
    },
    "vldl": {
        "name": "VLDL Cholesterol",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 1.65),
        "unit": "mmol/L",
        "explanation": "Very low-density lipoprotein (VLDL) is produced by the liver and carries triglycerides to tissues throughout the body. After delivering triglycerides, VLDL is converted into LDL. Elevated VLDL is closely linked to high triglycerides, and high levels contribute to the build-up of plaques in artery walls. VLDL is usually calculated rather than directly measured, often estimated as approximately one-fifth of your triglyceride level.",
        "advice_high": "High VLDL reflects excess triglycerides being transported in your blood, which is associated with cardiovascular risk and often with metabolic syndrome. The same lifestyle changes that lower triglycerides will reduce VLDL: cutting sugar and refined carbohydrates, reducing alcohol, eating more omega-3 fats from oily fish, exercising regularly, and losing excess weight. If levels remain elevated, your GP may consider medication.",
        "advice_low": "A low VLDL is a positive finding and indicates that triglyceride transport in the blood is within a healthy range. No action needed."
    },
    "homocysteine": {
        "name": "Homocysteine",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 10),
        "unit": "µmol/L",
        "explanation": "Homocysteine is an amino acid produced naturally during the metabolism of another amino acid, methionine, which comes from dietary protein. Normally, B vitamins (particularly B6, B12, and folate) recycle homocysteine back into useful compounds. When these B vitamins are insufficient, or in certain genetic conditions, homocysteine accumulates in the blood. Elevated homocysteine is linked to increased cardiovascular risk, as well as to cognitive decline and bone health. It's both a nutritional and a cardiovascular risk marker.",
        "advice_high": "Elevated homocysteine is most commonly caused by low levels of folate, vitamin B12, or vitamin B6. The first step is to increase your intake of these vitamins through diet (dark leafy greens, legumes, whole grains, meat, fish, eggs, dairy) or targeted supplementation. Your GP may check your B vitamin levels alongside this result. If supplementation doesn't bring levels down, further investigation into absorption, genetic factors (such as the MTHFR gene variant), or other causes may be warranted. Staying active, not smoking, and limiting alcohol also help keep homocysteine in check.",
        "advice_low": "A low homocysteine level is reassuring and suggests your B vitamin status is adequate and this particular cardiovascular risk marker is not elevated. No action needed."
    },
}

DIABETES_MARKERS = {
    "hba1c": {
        "name": "HbA1c",
        "type": "hilo", 
        "gender_specific": False,
        "range": (20, 42),
        "unit": "mmol/mol",
        "explanation": "HbA1c (glycated haemoglobin) measures the percentage of your haemoglobin that has glucose attached to it. Because red blood cells live for about 2-3 months, this test gives a picture of your average blood sugar levels over that period, rather than just a snapshot on the day of the test. It's the main test used to diagnose and monitor type 2 diabetes and prediabetes. Unlike a fasting glucose test, it isn't affected by what you ate that morning.",
        "advice_high": "An elevated HbA1c means your blood sugar has been running higher than ideal over recent months. A result between 42-47 mmol/mol is typically classified as prediabetes, meaning your blood sugar is higher than normal but not yet in the diabetic range. Above 48 mmol/mol usually indicates diabetes. The encouraging thing about prediabetes is that it's often reversible with lifestyle changes: reducing refined carbohydrates and sugar, eating more fibre and whole foods, increasing physical activity (even regular walking makes a real difference), losing 5-10% of body weight if you're overweight, and improving sleep quality. Your GP will advise on whether monitoring, further testing, or medication is needed based on your level.",
        "advice_low": "A low HbA1c means your average blood sugar has been on the lower end. This is generally fine, but if it's significantly below the range and you're experiencing episodes of shakiness, sweating, confusion, or feeling faint (symptoms of hypoglycaemia), mention it to your GP. This can occasionally happen with certain medications, excessive exercise without adequate food intake, or other metabolic issues."    
    },
    "glucose": {
        "name": "Glucose",
        "type": "hilo",
        "gender_specific": False,
        "range": (3.9, 6.9),
        "unit": "mmol/L",
        "explanation": "Blood glucose is the amount of sugar currently circulating in your blood. It's your body's primary source of quick energy, derived from the carbohydrates you eat. After a meal, glucose rises as food is digested, then falls as insulin (a hormone from the pancreas) helps move it into cells for energy. A fasting glucose test is taken after you haven't eaten for 8-12 hours, giving a baseline reading. A non-fasting test will naturally be higher and is interpreted differently.",
        "advice_high": "Elevated blood glucose can indicate prediabetes or diabetes, but a single raised reading doesn't confirm a diagnosis, especially if you weren't fasting or were feeling unwell at the time. Your GP may want to repeat the test or check your HbA1c for a longer-term picture. In the meantime, reducing sugar and refined carbohydrates, eating more fibre-rich whole foods, staying physically active, and maintaining a healthy weight are the most effective ways to bring blood sugar under control. Even small changes (swapping sugary drinks for water, taking a walk after meals) can have a measurable effect.",
        "advice_low": "Low blood glucose (hypoglycaemia) can cause shakiness, sweating, dizziness, irritability, and difficulty concentrating. It's most common in people taking diabetes medication, but can also occur after prolonged fasting, intense exercise, or heavy alcohol consumption on an empty stomach. If you experience these symptoms, eating or drinking something sugary (a glass of juice, glucose tablets) should help quickly. If low readings are a recurring pattern, speak with your GP to investigate further."
    },
    "insulin": {
        "name": "Insulin (Fasting)",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.6, 24.9),
        "unit": "mIU/L",
        "explanation": "Insulin is a hormone produced by the beta cells of the pancreas that acts as the key that unlocks your cells to allow glucose to enter and be used for energy. Fasting insulin (measured after at least 8-12 hours without food) reflects how much insulin your body needs to maintain normal blood sugar when no food is being digested. Persistently high fasting insulin is often a sign of insulin resistance, a state where cells don't respond well to insulin and the pancreas has to work harder to compensate. This is an early precursor to type 2 diabetes and is associated with weight gain, particularly around the abdomen.",
        "advice_high": "Elevated fasting insulin suggests your cells may be resistant to insulin's effects, meaning your pancreas is producing more than usual to keep blood sugar under control. This is strongly associated with excess body weight (especially abdominal fat), a sedentary lifestyle, and a diet high in refined carbohydrates and sugar. The most effective interventions are reducing refined carbohydrates and sugary foods, increasing fibre, exercising regularly (both aerobic and resistance training are helpful), losing excess weight, and improving sleep quality. Even moderate weight loss of 5-10% of body weight can significantly improve insulin sensitivity. Your GP may want to check your HbA1c and fasting glucose alongside this result.",
        "advice_low": "A low fasting insulin level reflects good insulin sensitivity, meaning your cells respond well to insulin and your pancreas doesn't need to produce large amounts. This is generally a positive finding. Very low insulin, particularly alongside high blood glucose, could indicate type 1 diabetes or advanced pancreatic disease, but this would typically be identified through other results."
    },
}

IRON_STATUS = {
    "serum_iron": {
        "name": "Serum Iron",
        "type": "hilo",
        "gender_specific": False,
        "range": (9, 30.4),
        "unit": "µmol/L",
        "explanation": "Serum iron measures the amount of iron currently circulating in your blood, bound to a transport protein called transferrin. Iron is essential for making haemoglobin (the oxygen-carrying part of red blood cells), supporting energy production, and maintaining a healthy immune system. Serum iron fluctuates throughout the day and is affected by recent meals, so it's best interpreted alongside other iron markers like ferritin and transferrin rather than in isolation.",
        "advice_high": "Elevated serum iron can result from taking iron supplements, eating a very iron-rich meal before the test, or from conditions where the body absorbs or stores too much iron (such as haemochromatosis, a relatively common genetic condition). Excess iron over time can damage organs including the liver. If your level is high and you're taking iron supplements, speak to your GP about whether you still need them. If you're not supplementing, your doctor may want to check your ferritin and transferrin saturation to understand whether iron is accumulating, and may test for haemochromatosis.",
        "advice_low": "Low serum iron is very common, especially in women of reproductive age, vegetarians, vegans, and people with digestive conditions that affect absorption. It can contribute to iron deficiency anaemia, leaving you feeling tired, weak, and breathless. Boost your intake of iron-rich foods: red meat, poultry, fish, lentils, beans, tofu, dark leafy greens, and fortified cereals. Eating vitamin C alongside iron-rich foods (for example, a glass of orange juice with a meal) significantly improves absorption. Tea and coffee with meals can reduce absorption. Your GP may recommend iron supplements if dietary changes aren't sufficient."
    },
    "transferrin": {
        "name": "Transferrin",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.5, 3.8),
        "unit": "g/L",
        "explanation": "Transferrin is a protein made by the liver that transports iron through your bloodstream to where it's needed. Think of it as iron's taxi service. Your body adjusts transferrin production based on how much iron is available: when iron stores are low, the liver makes more transferrin to maximise the capture and transport of whatever iron is available. When iron stores are plentiful, less transferrin is needed.",
        "advice_high": "High transferrin usually means your body is producing extra transport protein because iron stores are running low. It's a common finding in iron deficiency. Focus on increasing iron intake through diet (red meat, lentils, dark leafy greens, fortified cereals) and pairing iron-rich foods with vitamin C to boost absorption. Your GP will interpret this alongside your ferritin and serum iron to confirm whether you need supplements.",
        "advice_low": "Low transferrin can indicate that there's already plenty of iron available (so less transport protein is needed), or it can reflect liver disease, chronic inflammation, or malnutrition, since the liver is responsible for making transferrin. Your GP will look at this in the context of your other iron markers and liver function tests to determine what's going on."
    },
    "ferritin": {
        "name": "Ferritin",
        "type": "hilo",
        "gender_specific": True,
        "range": (10, 291, 30, 400),
        "unit": "ng/mL",
        "explanation": "Ferritin is a protein that stores iron inside your cells, particularly in the liver, spleen, and bone marrow. Measuring ferritin in your blood gives the best indication of your body's total iron reserves. It's considered the most useful single test for detecting iron deficiency. Women generally have lower ferritin than men due to menstrual iron losses, which is why the reference ranges differ. Ferritin can also rise during inflammation or infection (it's an acute phase reactant), which can mask an underlying iron deficiency.",
        "advice_high": "Elevated ferritin means your body is storing more iron than usual. This can happen with inflammation, infection, liver disease, heavy alcohol use, or a genetic condition called haemochromatosis (which causes the body to absorb too much iron from food). If your ferritin is high and you're taking iron supplements, stop and discuss with your GP. If you're not supplementing, your doctor may want to check your transferrin saturation and liver function, and possibly test for haemochromatosis. Reducing alcohol intake can also help if that's a contributing factor.",
        "advice_low": "Low ferritin is the earliest sign that your iron stores are depleting, and it can drop before your haemoglobin does. You may already be feeling the effects: fatigue, brain fog, hair thinning, brittle nails, or restless legs. Dietary iron from red meat is the most easily absorbed form, but plant sources (lentils, chickpeas, spinach, fortified cereals) combined with vitamin C also work well. Avoid drinking tea or coffee with meals, as they reduce iron absorption. Your GP will likely recommend iron supplements if your ferritin is significantly low, and may want to investigate the cause of the deficiency."
    },
    "uric_acid": {
        "name": "Uric Acid",
        "type": "hilo",
        "gender_specific": False,
        "range": (184, 464),
        "unit": "µmol/L",
        "explanation": "Uric acid is a waste product your body creates when it breaks down purines, which are natural substances found in your cells and in certain foods (especially organ meats, red meat, shellfish, and beer). Normally, uric acid dissolves in the blood, passes through the kidneys, and leaves the body in urine. Problems arise when the body produces too much or the kidneys don't excrete enough, causing levels to build up.",
        "advice_high": "Elevated uric acid (hyperuricaemia) increases the risk of gout, a painful form of arthritis caused by uric acid crystals forming in joints (often the big toe). It's also associated with kidney stones and may contribute to cardiovascular risk. To lower uric acid: reduce purine-rich foods (organ meats, game, shellfish, anchovies), limit alcohol (especially beer and spirits), cut back on sugary drinks containing fructose, drink plenty of water (at least 2 litres a day), and maintain a healthy weight. If you've had gout attacks or kidney stones, your GP may prescribe medication to lower uric acid levels.",
        "advice_low": "Low uric acid is uncommon and usually not a concern. It can occasionally be seen with certain genetic conditions, liver disease, or very high fluid intake. If your other results are normal and you feel well, no action is needed."
    },
    "iron_binding_capacity": {
        "name": "Total Iron Binding Capacity (TIBC)",
        "type": "hilo",
        "gender_specific": False,
        "range": (45, 81),
        "unit": "µmol/L",
        "explanation": "TIBC measures the total capacity of your blood to bind and transport iron using transferrin, the main iron-carrying protein. When iron stores are low, the liver produces more transferrin, raising the TIBC. When iron stores are plentiful, less transferrin is made, lowering TIBC. Think of it as the size of the transport fleet: a bigger fleet (high TIBC) means the body is trying harder to capture what little iron is available. TIBC is most useful when interpreted alongside serum iron and ferritin to build a complete picture of your iron status.",
        "advice_high": "A high TIBC usually indicates that your iron stores are depleted and your body is producing extra transferrin to maximise iron capture. This pattern is typical of iron deficiency. Focus on iron-rich foods (red meat, lentils, dark leafy greens, fortified cereals), pair them with vitamin C to improve absorption, and avoid tea and coffee with meals. Your GP will likely recommend iron supplements if dietary changes are insufficient, and may want to investigate the cause of the deficiency.",
        "advice_low": "Low TIBC can occur when iron stores are high (the body produces less transferrin when it doesn't need more iron), in chronic inflammation, liver disease, or malnutrition. Your GP will interpret this alongside your ferritin and serum iron to determine the underlying cause."
    },
    "transferrin_saturation": {
        "name": "Transferrin Saturation",
        "type": "hilo",
        "gender_specific": False,
        "range": (20, 50),
        "unit": "%",
        "explanation": "Transferrin saturation tells you what percentage of your available transferrin (iron transport protein) is actually loaded with iron. If serum iron is the amount of iron in transit and TIBC is the total transport capacity, transferrin saturation is the percentage of that capacity that's currently being used. A low saturation means plenty of empty transport proteins, suggesting iron is scarce. A high saturation means most of the transport protein is already carrying iron, which can indicate iron overload.",
        "advice_high": "A high transferrin saturation means a large proportion of your iron transport capacity is occupied, suggesting more iron is circulating than usual. When combined with high ferritin, this pattern raises concern for iron overload conditions such as haemochromatosis, a common inherited condition where the gut absorbs too much iron from food. Your GP may want to check the full iron panel and consider genetic testing for haemochromatosis. If you are taking iron supplements, they may recommend stopping them. Reducing red meat and alcohol can also help manage iron levels while investigations are underway.",
        "advice_low": "A low transferrin saturation, particularly when accompanied by low ferritin and high TIBC, is a classic sign of iron deficiency. This often precedes the development of anaemia. Increasing dietary iron and potentially taking supplements (under GP guidance) will help replenish stores. Eating vitamin C alongside iron-rich foods significantly improves absorption."
    },
}

BONE_PROFILE = {
    "vitamin_d": {
        "name": "Vitamin D",
        "type": "hilo",
        "gender_specific": False,
        "range": (50, 125),
        "unit": "nmol/L",
        "explanation": "Vitamin D is essential for absorbing calcium, building and maintaining strong bones, and supporting immune function and muscle health. Your body produces it when sunlight hits your skin, and you can also get it from foods like oily fish, egg yolks, and fortified products. In the UK and similar latitudes, vitamin D deficiency is very common, especially between October and March when sunlight isn't strong enough for your skin to make it. People with darker skin, those who spend limited time outdoors, and older adults are at higher risk of deficiency.",
        "advice_high": "Very high vitamin D levels (usually from taking high-dose supplements over a long period) can cause the body to absorb too much calcium, leading to nausea, kidney problems, and in extreme cases, calcium deposits in the heart and blood vessels. If you're taking vitamin D supplements, check the dose and speak with your GP about whether you need to reduce or stop them. Vitamin D toxicity doesn't happen from sun exposure or food alone.",
        "advice_low": "Low vitamin D is extremely common and very treatable. In the UK, Public Health England recommends that everyone consider taking a daily supplement of 10 micrograms (400 IU) during autumn and winter, and some people (those with limited sun exposure, darker skin, or who are housebound) should supplement year-round. Your GP may recommend a higher loading dose to bring levels up more quickly if you're significantly deficient. Eating oily fish, eggs, and fortified foods also contributes, though it's difficult to get enough from diet alone. Spending time outdoors in sunlight (with sensible sun protection) during spring and summer helps your body build up its stores."
    },
    "calcium": {
        "name": "Calcium",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.20, 2.60),
        "unit": "mmol/L",
        "explanation": "Calcium is the most abundant mineral in the body, making up around 99% of your bones and teeth. The remaining 1% circulates in your blood and plays critical roles in muscle contraction, nerve signalling, blood clotting, and heart rhythm. Your body tightly regulates blood calcium levels through a system involving parathyroid hormone (PTH), vitamin D, and the kidneys. Because of this tight regulation, blood calcium can remain normal even when bone calcium stores are depleting, which is why bone density scans are sometimes needed alongside blood tests.",
        "advice_high": "Elevated blood calcium (hypercalcaemia) most commonly results from overactive parathyroid glands (primary hyperparathyroidism) or, less commonly, from certain cancers that release calcium from bones. Other causes include vitamin D toxicity from excess supplementation, sarcoidosis, or prolonged immobility. Mild hypercalcaemia may cause fatigue, constipation, increased thirst, and muscle weakness. Your GP will want to check your parathyroid hormone level and may arrange further investigations. Staying well hydrated is important as calcium can affect kidney function.",
        "advice_low": "Low calcium (hypocalcaemia) can cause muscle cramps, tingling or numbness in the hands and feet, muscle spasms, and in severe cases, problems with heart rhythm. Common causes include vitamin D deficiency (which impairs calcium absorption), underactive parathyroid glands, low magnesium, or kidney problems. Your GP will likely check your vitamin D and PTH levels alongside this result. Ensuring adequate vitamin D intake and eating calcium-rich foods (dairy, fortified plant milks, leafy greens, almonds, tinned fish with bones) are the first practical steps."
    },
}

MUSCLE_HEALTH = {
    "ck": {
        "name": "Creatine Kinase (CK)",
        "type": "hilo",
        "gender_specific": False,
        "range": (25, 200),
        "unit": "U/L",
        "explanation": "Creatine kinase (CK) is an enzyme found mainly in your skeletal muscles, heart, and brain. It's released into the bloodstream when muscle cells are damaged or stressed. CK levels are very sensitive to physical activity, so a raised level after a hard gym session, a long run, or any vigorous exercise is completely normal and expected. The test is most useful when interpreted in the context of your recent activity levels and symptoms.",
        "advice_high": "Elevated CK most commonly reflects recent strenuous exercise, and levels can remain raised for several days after a hard workout. If you exercised heavily in the 48-72 hours before your blood test, that's very likely the explanation. Other causes include muscle injury, falls, seizures, certain medications (especially statins, which can occasionally cause muscle pain and CK elevation), and in rare cases, conditions affecting the muscles or heart. If you're experiencing unexplained muscle pain, weakness, or dark-coloured urine (a sign of serious muscle breakdown), contact your GP. Otherwise, if you were active before the test, consider having it rechecked after a few days of rest.",
        "advice_low": "A low CK level simply reflects lower muscle mass or less recent muscle activity. It's not a cause for concern and no specific action is needed. If you'd like to build muscle mass, regular resistance training combined with adequate protein intake is the way to go."
    }
}

LIVER_FUNCTION = {
    "albumin": {
        "name": "Albumin",
        "type": "hilo",
        "gender_specific": False,
        "range": (34, 50),
        "unit": "g/L",
        "explanation": "Albumin is the most abundant protein in your blood and is made by the liver. It has several jobs: keeping fluid inside your blood vessels (preventing swelling), transporting hormones, vitamins, and medications around the body, and acting as a general indicator of nutritional status and liver health. Because albumin levels change slowly, they reflect your overall health over recent weeks rather than day-to-day fluctuations.",
        "advice_high": "Mildly elevated albumin is usually the result of dehydration rather than overproduction. Drinking more water and reassessing after rehydration is typically all that's needed. Significantly high levels are rare and may warrant a repeat test. Mention it to your GP if it persists.",
        "advice_low": "Low albumin can indicate liver disease (since the liver makes it), kidney disease (where protein leaks into urine), malnutrition, chronic inflammation, or conditions that cause the body to lose protein. It can also drop temporarily during illness or after surgery. If your level is low, your GP will want to understand why by looking at your other liver and kidney markers, your diet, and your general health. Eating adequate protein (meat, fish, eggs, dairy, legumes) supports albumin production, but addressing the underlying cause is the priority."
    },
    "total_bilirubin": {
        "name": "Total Bilirubin",
        "type": "hilo",
        "gender_specific": False,
        "range": (5, 21),
        "unit": "µmol/L",
        "explanation": "Bilirubin is a yellow-orange pigment produced when your body breaks down old red blood cells. The liver processes bilirubin so it can be excreted in bile (which helps digest fats in your gut) and eventually leave the body in stool, which is what gives stool its brown colour. A small amount of bilirubin in the blood is completely normal. Higher levels can cause a yellowish tinge to the skin and whites of the eyes (jaundice).",
        "advice_high": "Elevated bilirubin has several possible explanations. The most common benign cause is Gilbert's syndrome, a harmless genetic condition affecting about 5-10% of the population, where the liver is slightly slower at processing bilirubin. This can cause mild, intermittent jaundice, especially during illness, stress, or fasting. Other causes include liver inflammation (from alcohol, medications, or viral hepatitis), gallstones blocking bile ducts, or conditions that cause red blood cells to break down faster than normal. Your GP will look at this alongside your other liver tests to determine the cause. If you already know you have Gilbert's syndrome, a mildly elevated result is expected and doesn't require any action.",
        "advice_low": "Low bilirubin is not a clinical concern and requires no action."
    },
    "alkaline_phosphatase": {
        "name": "Alkaline Phosphatase",
        "type": "hilo",
        "gender_specific": False,
        "range": (46, 116),
        "unit": "IU/L",
        "explanation": "Alkaline phosphatase (ALP) is an enzyme found in several tissues, but mainly in the liver and bones. In the liver, it's concentrated near the bile ducts. In bones, it's involved in the process of building new bone tissue. Because it comes from two main sources, a raised ALP can point to either liver/bile duct issues or bone conditions, and your doctor will use other tests to work out which.",
        "advice_high": "Elevated ALP can indicate bile duct obstruction (such as gallstones), liver disease, or bone conditions (such as Paget's disease, fracture healing, or vitamin D deficiency causing the bones to work harder). It's also normally higher in children and adolescents (because their bones are still growing) and during pregnancy. Your GP will look at your other liver tests (GGT is particularly helpful here, as it rises with liver/bile duct problems but not bone issues) to narrow down the source. If it's liver-related, reducing alcohol and discussing medications with your GP is advisable. If it's bone-related, checking vitamin D and calcium is the next step.",
        "advice_low": "Low ALP is uncommon and usually not a significant finding. It can occasionally occur with zinc or magnesium deficiency, hypothyroidism, or certain rare genetic conditions. Mention it to your GP if other markers are also abnormal."
    },
    "alt/gpt": {
        "name": "Alanine Aminotransferase (ALT/GPT)",
        "type": "hilo",
        "gender_specific": False,
        "range": (5, 56),
        "unit": "IU/L",
        "explanation": "ALT is an enzyme found predominantly in liver cells. When liver cells are damaged or inflamed, ALT leaks into the bloodstream, making it one of the most specific markers of liver injury. It's the test doctors rely on most to detect liver inflammation, whether from alcohol, medications, fatty liver disease, or viral hepatitis. Small, temporary elevations can occur after intense exercise or from common medications like paracetamol, ibuprofen, or statins.",
        "advice_high": "Elevated ALT means some degree of liver cell damage or inflammation is occurring. The most common causes in the general population are non-alcoholic fatty liver disease (often linked to being overweight or having type 2 diabetes), excess alcohol consumption, and medications. Other causes include viral hepatitis, autoimmune liver disease, and coeliac disease. Practical steps include reducing or eliminating alcohol, maintaining a healthy weight, being careful with paracetamol dosing, and reviewing any medications or supplements you're taking with your GP. If the elevation is persistent, your doctor may arrange further blood tests, an ultrasound of your liver, or a referral to a specialist.",
        "advice_low": "A low ALT is not a clinical concern and is generally a sign that your liver cells are healthy. No action is needed."
    },
    "ast/got": {
        "name": "Aspartate Aminotransferase (AST/GOT)",
        "type": "hilo",
        "gender_specific": False,
        "range": (13, 45),
        "unit": "IU/L",
        "explanation": "AST is an enzyme found in the liver, heart, muscles, and other tissues. Like ALT, it's released into the blood when cells are damaged. Because AST is present in multiple organs (not just the liver), an elevated AST is less specific to the liver than ALT. Doctors often compare the two: if both are raised, a liver cause is likely. If AST is raised but ALT is normal, the source might be the heart or muscles instead.",
        "advice_high": "Elevated AST can reflect liver damage (from alcohol, medications, fatty liver disease, or hepatitis), but also muscle injury, intense exercise, or heart problems. If your ALT is also elevated, a liver cause is most likely. If only AST is raised, your doctor may consider non-liver sources. The same general liver-protective steps apply: moderate alcohol, maintain a healthy weight, review medications with your GP, and avoid excessive paracetamol. If you exercised heavily before the test, mention that to your doctor, as vigorous activity can raise AST for several days.",
        "advice_low": "A low AST is not a clinical concern and indicates no significant cell damage in the liver, heart, or muscles. No action needed."
    },
    "gamma_gt": {
        "name": "Gamma-Glutamyl Transferase (GGT)",
        "type": "hilo",
        "gender_specific": False,
        "range": (4, 38),
        "unit": "IU/L",
        "explanation": "GGT is an enzyme found mainly in the liver and bile ducts. It's one of the most sensitive markers of liver and bile duct problems, and it's particularly responsive to alcohol use. Doctors often use GGT alongside ALP to determine whether an elevated ALP is coming from the liver or from the bones: if GGT is also raised, the liver is the likely source. GGT is sometimes informally considered a marker of alcohol consumption, though it can be elevated by other things too.",
        "advice_high": "The most common cause of elevated GGT is alcohol use, even at levels that might not seem excessive. Other causes include fatty liver disease, certain medications (including some commonly used drugs like antiepileptics and some antibiotics), bile duct obstruction, and chronic liver conditions. If you drink alcohol, reducing or stopping intake is often the single most effective way to bring GGT down, and levels typically improve within weeks. If you don't drink, your GP will look at other liver markers and may arrange an ultrasound to investigate further. Maintaining a healthy weight and reviewing medications you're taking are also worthwhile steps.",
        "advice_low": "A low GGT is not a clinical concern and suggests your liver and bile ducts are functioning well. No action needed."
    },
    "total_protein": {
        "name": "Total Protein",
        "type": "hilo",
        "gender_specific": False,
        "range": (60, 80),
        "unit": "g/L",
        "explanation": "Total protein measures the combined amount of all proteins in your blood plasma, primarily albumin and globulins. Proteins serve countless functions: transporting substances around the body, fighting infections (antibodies are globulins), clotting blood, maintaining fluid balance, and acting as enzymes and hormones. Total protein is a broad indicator of nutritional status and liver and kidney health. It's usually interpreted alongside albumin, and the difference between the two gives a globulin value.",
        "advice_high": "Elevated total protein can occur with dehydration (making all blood components more concentrated) or when the body produces excess immunoglobulins, as happens in some inflammatory conditions, chronic infections, or conditions like multiple myeloma. Your GP will look at this alongside your albumin to calculate your globulin level, and may arrange protein electrophoresis (a test that separates the different protein types) if a specific protein abnormality is suspected.",
        "advice_low": "Low total protein can result from inadequate protein intake (malnutrition), conditions causing protein loss (kidney disease, protein-losing enteropathy), liver disease (which impairs protein synthesis), or excessive fluid retention diluting protein concentrations. Make sure your diet includes adequate protein from varied sources, and mention this result to your GP so they can investigate alongside your other liver, kidney, and nutritional markers."
    },
    "globulin": {
        "name": "Globulin",
        "type": "hilo",
        "gender_specific": False,
        "range": (18, 36),
        "unit": "g/L",
        "explanation": "Globulins are a group of proteins in your blood that includes many important immune and transport proteins. They're typically calculated by subtracting albumin from total protein. The main types are alpha globulins (acute-phase proteins that rise during inflammation), beta globulins (lipid transport proteins), and gamma globulins (immunoglobulins or antibodies). An abnormally high or low globulin level can point to immune system disorders, chronic infections, liver disease, or inflammatory conditions.",
        "advice_high": "Elevated globulins can indicate chronic inflammation, ongoing infection, autoimmune disease, or in some cases a blood disorder affecting immunoglobulin production (such as multiple myeloma or other plasma cell conditions). Your GP may arrange further tests including protein electrophoresis to determine which fraction is elevated and why. The appropriate action depends entirely on the underlying cause.",
        "advice_low": "Low globulins can occur with immune deficiency conditions, certain liver diseases, or protein loss through the kidneys or gut. Immune deficiency can increase susceptibility to infections. Your GP will look at this result alongside your albumin, total protein, and other markers to assess what's driving the low level."
    },
}

URINE_ANALYSIS = {
    "ph": {
        "name": "pH (Urine)",
        "type": "hilo",
        "gender_specific": False,
        "range": (4.5, 8.0),
        "unit": "",
        "explanation": "Urine pH measures how acidic or alkaline your urine is on a scale from about 4.5 (quite acidic) to 8.0 (quite alkaline). Your kidneys adjust the pH of your urine to help maintain a stable acid-base balance in your body. Urine pH fluctuates throughout the day depending on what you eat and drink: a diet high in meat and protein tends to produce more acidic urine, while a diet rich in fruits and vegetables tends to produce more alkaline urine. On its own, urine pH is mainly useful for assessing kidney stone risk and monitoring urinary tract infections.",
        "advice_high": "Highly alkaline urine can be associated with urinary tract infections (certain bacteria make urine more alkaline), a diet very rich in fruits and vegetables, or certain medications. Persistently alkaline urine may increase the risk of certain types of kidney stones (calcium phosphate and struvite stones). If you have symptoms of a urinary tract infection (burning when you urinate, needing to go frequently, cloudy or strong-smelling urine), contact your GP. Otherwise, this finding is usually interpreted alongside other urine results.",
        "advice_low": "Very acidic urine can result from a high-protein diet, dehydration, or certain metabolic conditions. Persistently acidic urine may increase the risk of uric acid kidney stones. Staying well hydrated and eating a balanced diet that includes plenty of fruits and vegetables can help normalise urine pH. If you have a history of kidney stones, discuss this with your GP."    
    },
    "urine_protein": {
        "name": "Urine Protein",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Healthy kidneys filter waste out of your blood while keeping useful things like protein in. Finding protein in your urine (proteinuria) can suggest that the kidney's filters are letting protein through that should be staying in the bloodstream. Small, temporary amounts of protein can appear after vigorous exercise, during a fever, in hot weather, or with dehydration, and don't necessarily mean anything is wrong. Persistent proteinuria, however, can be an early sign of kidney damage.",
        "advice_high": "If protein has been detected in your urine, don't panic. A single positive result often turns out to be temporary and benign. Your GP will likely want to repeat the test (ideally a first-morning urine sample, which is more accurate) and may also check your blood for kidney function markers like creatinine and eGFR. If proteinuria persists, it's important to manage blood pressure and blood sugar carefully, as high blood pressure and diabetes are the two most common causes of kidney damage. Staying hydrated, not smoking, and avoiding excessive use of anti-inflammatory painkillers (ibuprofen, naproxen) all support kidney health.",
        "advice_low": "Absence of protein in your urine is the expected, normal finding. Your kidneys are filtering properly."    
    },
    "urine_glucose": {
        "name": "Urine Glucose",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Normally, your kidneys reabsorb all the glucose that passes through them, so none ends up in your urine. Glucose starts appearing in urine when blood sugar levels rise above the kidney's reabsorption threshold, which is typically around 10 mmol/L. This is most commonly associated with diabetes, where blood sugar is persistently elevated. Occasionally, glucose can appear in urine even with normal blood sugar due to a harmless condition called renal glycosuria, where the kidneys have a lower-than-usual threshold for reabsorbing glucose.",
        "advice_high": "Finding glucose in your urine suggests your blood sugar may have been elevated at the time the sample was taken. If you haven't already been diagnosed with diabetes, your GP will likely want to check your fasting blood glucose and HbA1c to get a clearer picture. If you are diabetic, glucose in your urine can indicate that your blood sugar control could be improved. In either case, the standard advice applies: reduce sugar and refined carbohydrates, eat more fibre and whole foods, stay active, and discuss your results with your GP to see whether medication adjustments are needed.",
        "advice_low": "Absence of glucose in your urine is the expected, normal finding. It means your blood sugar is staying within the range your kidneys can handle."    
    },
    "ketones": {
        "name": "Ketones (Urine)",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Ketones are produced when your body burns fat for energy instead of glucose. This happens when glucose isn't readily available, such as during fasting, prolonged exercise, a very low-carbohydrate or ketogenic diet, or when your body can't use glucose properly (as in uncontrolled diabetes). Small amounts of ketones in urine can be normal in certain circumstances, but larger amounts may need investigation.",
        "advice_high": "Ketones in your urine can be perfectly harmless if you've been fasting, following a low-carbohydrate diet, doing intense or prolonged exercise, or if you were unwell with vomiting or reduced food intake around the time of the test. However, for people with diabetes (especially type 1), significant ketones in the urine can indicate diabetic ketoacidosis (DKA), a serious condition that needs urgent medical attention. If you have diabetes and are feeling unwell with nausea, abdominal pain, rapid breathing, or confusion, seek medical help immediately. If you don't have diabetes and the ketones are likely from diet or fasting, no action is usually needed.",
        "advice_low": "Absence of ketones in your urine is the expected, normal finding when your body is using glucose as its primary energy source."    
    },
    "wbcs": {
        "name": "White Blood Cells (Urine)",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "White blood cells in your urine indicate that your immune system is responding to something in your urinary tract. In small numbers they can be normal, but higher levels suggest inflammation or infection somewhere along the tract (kidneys, ureters, bladder, or urethra). A urinary tract infection (UTI) is by far the most common cause, particularly in women.",
        "advice_high": "White blood cells in your urine most likely indicate a urinary tract infection, especially if you're also experiencing symptoms like a burning sensation when urinating, needing to go more frequently, lower abdominal discomfort, or cloudy or strong-smelling urine. Contact your GP, who may prescribe a short course of antibiotics after confirming the infection. In the meantime, drink plenty of water to help flush bacteria from your system. If you're getting recurrent UTIs, your doctor can advise on prevention strategies. Less common causes of urinary white cells include kidney inflammation, sexually transmitted infections, or contamination of the sample.",
        "advice_low": "Absence of white blood cells in your urine is the expected, normal finding. It indicates no active infection or inflammation in your urinary tract." 
    },
    "rbcs": {
        "name": "Red Blood Cells (Urine)",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "Red blood cells in urine (haematuria) means there is some blood in your urine, whether visible to the eye or only detectable under a microscope. The blood can come from anywhere along the urinary tract: the kidneys, ureters, bladder, or urethra. There are many possible causes, ranging from completely benign to those that warrant investigation. In women, contamination from menstrual blood is a common and harmless reason for a positive result.",
        "advice_high": "Finding red blood cells in your urine doesn't automatically mean something serious is wrong. Common benign causes include urinary tract infections, vigorous exercise (especially running), kidney stones, menstrual contamination in women, and minor irritation of the urethra. However, because haematuria can occasionally indicate conditions that need treatment (such as bladder or kidney problems), your GP will typically want to investigate. They may repeat the urine test, check your kidney function with a blood test, arrange an ultrasound, or refer you for further evaluation depending on your age, symptoms, and other risk factors. Don't delay in mentioning this result to your doctor.",
        "advice_low": "Absence of red blood cells in your urine is the expected, normal finding." 
    },
    "casts": {
        "name": "Casts (Urine)",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "casts/µL",
        "explanation": "Casts are tiny tube-shaped particles that form inside the kidney's tubules (the microscopic tubes where urine is produced). They're made of protein, cells, or other material that has moulded to the shape of the tubule, a bit like a jelly mould. Different types of casts can point to different conditions. Hyaline casts (made of pure protein) can appear in healthy people after exercise or dehydration, while other types (red cell casts, white cell casts, granular casts) are more significant and suggest kidney inflammation or damage.",
        "advice_high": "The presence of casts in your urine suggests something is happening in the kidneys that warrants a closer look. The significance depends on what type of casts were found: hyaline casts after exercise or dehydration are usually harmless, while other types may indicate kidney inflammation (nephritis), infection, or other kidney conditions. Your GP will interpret this alongside your other urine and blood results and may refer you for further kidney function assessment if needed. Staying well hydrated and avoiding excessive use of anti-inflammatory painkillers supports kidney health in the meantime.",
        "advice_low": "Absence of casts in your urine is the expected, normal finding." 
    },
    "bacterial_count": {
        "name": "Bacterial Count (Urine)",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cfu/mL",
        "explanation": "This measures the number of bacteria present in your urine sample. Healthy urine is normally sterile (free of bacteria), so the presence of significant numbers of bacteria usually indicates an infection in the urinary tract. However, some contamination can occur during sample collection (especially if the sample wasn't a 'clean catch' midstream sample), so a small number of bacteria doesn't always mean infection.",
        "advice_high": "A significant bacterial count in your urine strongly suggests a urinary tract infection (UTI), especially if white blood cells are also present and you have symptoms such as burning or pain when urinating, frequent urination, urgency, lower abdominal pain, or cloudy and strong-smelling urine. Contact your GP, who may prescribe antibiotics based on the type of bacteria found. Drink plenty of water to help flush bacteria from your system. If this is a recurrent problem, your GP can discuss prevention strategies and may want to investigate whether there's an underlying cause. If you have no symptoms, your doctor may want to repeat the test to rule out contamination before starting treatment.",
        "advice_low": "Absence of bacteria in your urine is the expected, normal finding. It confirms there's no urinary tract infection." 
    },
    "urine_culture": {
        "name": "Urine Culture and Sensitivities",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "",
        "explanation": "A urine culture is a laboratory test where a urine sample is placed on a growth medium and incubated to see whether bacteria grow, and if so, which species are present. It's more specific than a dipstick test and can confirm the exact organism causing a urinary tract infection. The sensitivity part of the test determines which antibiotics will kill the identified bacteria, guiding treatment choices. This ensures you're given the most effective antibiotic rather than a broad-spectrum guess.",
        "advice_high": "A positive urine culture means bacteria were detected in your sample, confirming a urinary tract infection. The sensitivity results tell your GP which antibiotic to prescribe, making treatment more targeted and effective. Complete the full course of antibiotics even if your symptoms improve quickly. Drink plenty of water to help flush your urinary tract. If you suffer from recurrent UTIs, your GP may want to investigate contributing factors (such as anatomy, kidney stones, or immune function) and may consider a longer preventive antibiotic course or other strategies.",
        "advice_low": "A negative culture means no significant bacterial growth was detected, indicating no active urinary tract infection. If you had symptoms, these may have another cause, or the infection may have been resolving at the time of sampling. Discuss any persistent symptoms with your GP."
    },
}

THYROID_FUNCTION = {
    "free_thyroxine": {
        "name": "Free Thyroxine (FT4)",
        "type": "hilo",
        "gender_specific": False,
        "range": (10.4, 19.4),
        "unit": "pmol/L",
        "explanation": "Free thyroxine (FT4) is the unbound, active form of the main hormone your thyroid gland produces. Thyroxine acts like your body's metabolic thermostat: it influences how fast your cells burn energy, how quickly your heart beats, how warm you feel, and how your brain, gut, and muscles function. 'Free' means the portion that's not attached to carrier proteins and is therefore available for your body to use. FT4 is usually interpreted alongside TSH to get a complete picture of thyroid health.",
        "advice_high": "High FT4 typically indicates an overactive thyroid (hyperthyroidism), where the gland is producing more hormone than your body needs. This can speed up your metabolism, causing symptoms like unexplained weight loss, a rapid or irregular heartbeat, anxiety, trembling hands, difficulty sleeping, increased sweating, and feeling hot. Common causes include Graves' disease (an autoimmune condition), thyroid nodules, or thyroiditis (inflammation). If your FT4 is elevated, your GP will likely check your TSH (which should be low if hyperthyroidism is the cause) and may arrange further tests or a referral to an endocrinologist. Treatment is available and effective.",
        "advice_low": "Low FT4 suggests an underactive thyroid (hypothyroidism), where the gland isn't producing enough hormone. This slows your metabolism, which can cause tiredness, weight gain, feeling cold, constipation, dry skin, thinning hair, low mood, and difficulty concentrating. The most common cause is Hashimoto's thyroiditis, an autoimmune condition. Your GP will check your TSH (which should be high if hypothyroidism is confirmed) and may start you on levothyroxine, a daily tablet that replaces the missing hormone. Once the dose is right, most people feel much better and the treatment is straightforward."    
    },
    "tsh": {
        "name": "Thyroid-Stimulating Hormone (TSH)",
        "type": "hilo", 
        "gender_specific": False,
        "range": (0.55, 4.78),
        "unit": "mIU/L",
        "explanation": "TSH is produced by your pituitary gland (a pea-sized gland at the base of your brain) and tells your thyroid how much hormone to make. It works like a thermostat: when thyroid hormone levels drop, the pituitary releases more TSH to stimulate the thyroid. When thyroid hormone levels rise, TSH drops. This means TSH and thyroid hormones (FT4, FT3) typically move in opposite directions. TSH is usually the first test doctors check when screening for thyroid problems, and it's very sensitive to even small changes in thyroid function.",
        "advice_high": "High TSH means your pituitary gland is working harder than usual to stimulate the thyroid, which typically indicates the thyroid is underperforming (hypothyroidism). You may experience fatigue, weight gain, feeling cold, constipation, dry skin, or low mood. The most common cause is Hashimoto's thyroiditis. A mildly elevated TSH with normal FT4 is called subclinical hypothyroidism, and your GP may choose to monitor it or treat it depending on the level and whether you have symptoms. If treatment is needed, levothyroxine (a daily tablet) is effective and well-tolerated.",
        "advice_low": "Low TSH means your pituitary gland has dialled back its signal because there's already plenty of thyroid hormone circulating, which typically indicates an overactive thyroid (hyperthyroidism). You may notice weight loss, a racing heart, anxiety, tremor, difficulty sleeping, or heat intolerance. Common causes include Graves' disease and thyroid nodules. Your GP will check your FT4 and FT3 alongside this result and may arrange further tests or refer you to a specialist. Effective treatments are available."
    },
    "ft3": {
        "name": "Free Triiodothyronine (FT3)",
        "type": "hilo",
        "gender_specific": False,
        "range": (2.6, 7.1),
        "unit": "pmol/L",
        "explanation": "Free triiodothyronine (FT3) is the most active form of thyroid hormone. Most FT3 is actually produced by converting FT4 in your tissues (liver, kidneys, and elsewhere) rather than being released directly by the thyroid gland. It's roughly three to four times more potent than FT4 at influencing your metabolism, heart rate, temperature regulation, and energy levels. FT3 is sometimes the last thyroid marker to become abnormal, so it adds useful information when FT4 or TSH is borderline.",
        "advice_high": "High FT3 supports a diagnosis of hyperthyroidism (overactive thyroid), especially if TSH is low and FT4 is also elevated. In some cases, FT3 can be high while FT4 is normal, a pattern called T3 thyrotoxicosis, which is more common in early or mild hyperthyroidism and in certain thyroid nodule conditions. Symptoms are the same as for high FT4: weight loss, rapid heartbeat, anxiety, tremor, and heat intolerance. Your GP will interpret this alongside your other thyroid results and may refer you to an endocrinologist for further assessment and treatment.",
        "advice_low": "Low FT3 can indicate hypothyroidism, but it can also drop in response to non-thyroid illness, stress, poor nutrition, or calorie restriction (sometimes called 'sick euthyroid syndrome' or 'low T3 syndrome'). In these cases, the body is reducing metabolic activity as a protective response, and levels typically recover once you're well again. If FT3 is low alongside an abnormal TSH, your GP will manage it as part of thyroid treatment. If your TSH is normal but FT3 is low, focus on eating well, resting, and recovering from any illness. Mention the result to your GP for a follow-up check."    
    },
    "tpo_antibodies": {
        "name": "Thyroid Peroxidase Antibodies (TPOAb)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 35),
        "unit": "IU/mL",
        "explanation": "Thyroid peroxidase antibodies (TPOAb) are antibodies produced by the immune system that mistakenly target thyroid peroxidase, an enzyme essential for making thyroid hormones. Their presence indicates that the immune system is attacking the thyroid gland, which is the hallmark of autoimmune thyroid conditions, most commonly Hashimoto's thyroiditis (which tends to cause an underactive thyroid) and sometimes Graves' disease (which causes an overactive thyroid). TPOAb can be present for years before thyroid function is affected.",
        "advice_high": "Elevated TPO antibodies confirm autoimmune activity against your thyroid. This doesn't necessarily mean your thyroid function is abnormal right now, but it does mean you're at higher risk of developing thyroid dysfunction in the future, particularly hypothyroidism. Your GP will monitor your TSH and FT4 over time, often annually, to catch any changes early. Currently, there's no treatment specifically to reduce the antibodies themselves, but managing general health factors (adequate selenium intake, vitamin D sufficiency, and a balanced diet) may support thyroid health. If your thyroid function is already abnormal, that will be treated on its own merits.",
        "advice_low": "A result below the reference threshold suggests autoimmune thyroid antibodies are not detectable at a clinically significant level. No action is needed based on this result alone."
    },
    "thyroglobulin_antibody": {
        "name": "Thyroglobulin Antibody (TgAb)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 115),
        "unit": "IU/mL",
        "explanation": "Thyroglobulin antibodies (TgAb) target thyroglobulin, a protein made by the thyroid that serves as a precursor to thyroid hormones. Like TPO antibodies, elevated TgAb indicate autoimmune activity against the thyroid and are associated with Hashimoto's thyroiditis and other autoimmune thyroid conditions. TgAb are also important in monitoring people who have had thyroid cancer treatment, as they can interfere with the measurement of thyroglobulin (used to check for cancer recurrence).",
        "advice_high": "Elevated thyroglobulin antibodies point to autoimmune activity against the thyroid. This is often seen alongside elevated TPO antibodies in Hashimoto's thyroiditis. Your GP will monitor your thyroid function (TSH and FT4) over time to check whether the gland remains working normally. If you've been treated for thyroid cancer, the presence of these antibodies is particularly significant as it can affect the interpretation of thyroglobulin tumour marker measurements and should be discussed with your specialist.",
        "advice_low": "Thyroglobulin antibodies are not detectable at a clinically significant level. No specific action is required based on this finding alone."
    },
}

CANCER_MARKERS = {
    "ca_125": {
        "name": "CA 125",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 35),
        "unit": "U/mL",
        "explanation": "CA-125 is a protein that can be found at higher-than-normal levels in the blood of some people with ovarian cancer. However, it's not a definitive cancer test. Many non-cancerous conditions can also raise CA-125, including endometriosis, fibroids, pelvic inflammatory disease, liver disease, menstruation, and even pregnancy. Because of this, CA-125 is most useful for monitoring people who've already been diagnosed with ovarian cancer (to track treatment response), rather than as a screening test in the general population. This marker is not relevant for those without ovaries.",
        "advice_high": "An elevated CA-125 does not mean you have ovarian cancer. Many common, benign conditions can raise this marker. That said, it's a finding your GP will want to follow up on, typically with a pelvic ultrasound and possibly a repeat blood test in a few weeks. The combination of CA-125, imaging, and your symptoms (if any) gives a much more complete picture than the blood test alone. Try not to jump to worst-case conclusions based on this single number. If further investigation is recommended, it's to rule things out and put your mind at rest.",
        "advice_low": "A normal CA-125 level is reassuring, though it's worth knowing that not all ovarian cancers cause CA-125 to rise (particularly early-stage disease). If you have persistent symptoms such as bloating, pelvic pain, difficulty eating, or urinary frequency, mention them to your GP regardless of this result." 
    },
    "psa": {
        "name": "Prostate-Specific Antigen (PSA)",
        "type": "upper_bound",
        "gender_specific": False,
        "range": (0, 4),
        "unit": "ng/mL",
        "explanation": "PSA is a protein produced by the prostate gland. All men with a prostate have some PSA in their blood, and levels naturally tend to increase with age as the prostate grows. PSA testing is used to help detect prostate cancer, but an elevated PSA does not mean you have cancer. Many non-cancerous conditions raise PSA, including benign prostatic hyperplasia (an enlarged prostate, which is very common in older men), prostatitis (prostate infection or inflammation), urinary tract infections, and even vigorous exercise or sexual activity in the 48 hours before the test. This marker is not relevant for those without a prostate.",
        "advice_high": "An elevated PSA warrants further investigation, but it's not a cancer diagnosis. Most men with a raised PSA turn out not to have prostate cancer. Your GP will consider your age, the degree of elevation, your symptoms, any family history of prostate cancer, and may want to repeat the test to confirm the result (as PSA can fluctuate). If the level remains elevated, you may be referred for further assessment, which could include an MRI scan and potentially a biopsy. Try not to assume the worst at this stage. Avoid cycling, ejaculation, and vigorous exercise for 48 hours before any repeat test, as these can temporarily raise PSA.",
        "advice_low": "A low PSA level is reassuring and suggests the prostate is not producing excessive amounts of this protein. No action is needed based on this result alone."
    }
}

VITAMINS = {
    "ab12": {
        "name": "Vitamin B12 (cobalamin)",
        "type": "hilo",
        "gender_specific": False,
        "range": (25.1, 165),
        "unit": "pmol/L",
        "explanation": "Vitamin B12 is essential for making red blood cells, maintaining a healthy nervous system, and synthesising DNA. Your body can't produce it, so it must come from your diet (meat, fish, eggs, dairy) or supplements. B12 is stored in the liver in relatively large amounts, so deficiency tends to develop slowly over months or years. Vegetarians and vegans are at higher risk of deficiency because plant foods don't naturally contain B12. Absorption also requires a protein called intrinsic factor, produced in the stomach, so conditions affecting the stomach or gut can impair B12 uptake even if dietary intake is adequate.",
        "advice_high": "Very high B12 levels are less commonly investigated but can occasionally be associated with liver disease, certain blood cancers, or kidney failure. High levels from supplements or diet are generally not harmful, as excess B12 is usually excreted in urine. If you're not taking B12 supplements and your level is significantly elevated, mention it to your GP, who may want to check your liver function and blood count to rule out any underlying cause.",
        "advice_low": "Low B12 can cause a type of anaemia where red blood cells become abnormally large (macrocytic anaemia), along with neurological symptoms such as numbness or tingling in the hands and feet, difficulty walking, memory problems, and mood changes. If caught early, B12 deficiency is very treatable. For mild deficiency, oral supplements or dietary changes (more meat, fish, eggs, dairy, or fortified foods) may be sufficient. For more significant deficiency, or if absorption is the problem (as in pernicious anaemia or after gastric surgery), your GP may recommend B12 injections. It's important to treat B12 deficiency promptly because prolonged nerve damage can become difficult to reverse."
    },
    "folate": {
        "name": "Folate (vitamin B9)",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (3, 17),
        "unit": "ng/mL",
        "explanation": "Folate (vitamin B9) is essential for making and repairing DNA, producing red blood cells, and supporting the rapid cell division that occurs during growth and pregnancy. Your body doesn't store large amounts of folate, so you need a regular dietary supply. Good sources include dark leafy greens (spinach, kale, broccoli), legumes (lentils, chickpeas, beans), oranges, fortified cereals, and liver. Folate is particularly important during pregnancy because deficiency in early pregnancy increases the risk of neural tube defects in the developing baby.",
        "advice_high": "High folate levels from food or supplements are generally not harmful, as excess is excreted in urine. Very high levels are occasionally seen in people taking high-dose supplements. One thing to be aware of is that high folate intake can mask the blood signs of vitamin B12 deficiency (by correcting the anaemia while allowing neurological damage to progress), so if your folate is high, it's worth making sure your B12 level is adequate too.",
        "advice_low": "Low folate can cause a type of anaemia where red blood cells become abnormally large (megaloblastic anaemia), leading to tiredness, weakness, and shortness of breath. It can also cause mouth ulcers, a sore tongue, and mood changes. Increasing folate-rich foods in your diet is the first step: leafy greens, legumes, citrus fruits, and fortified cereals are all good sources. Your GP may recommend a folic acid supplement, especially if you're pregnant or planning to become pregnant (400 micrograms daily is the standard recommendation before conception and during the first 12 weeks). If your folate is low alongside low B12, both should be addressed."
    },
    "vitamin_b12": {
        "name": "Vitamin B12 (Total Serum)",
        "type": "hilo",
        "gender_specific": False,
        "range": (148, 900),
        "unit": "pmol/L",
        "explanation": "Total serum vitamin B12 measures the overall concentration of cobalamin in your blood, including both the active fraction (bound to transcobalamin II) and the inactive fraction (bound to haptocorrin). B12 is essential for red blood cell production, DNA synthesis, and nervous system function. Your body stores B12 in the liver for several years, so deficiency develops slowly and may not be apparent until stores are significantly depleted. This test measures total B12; in some cases, an additional test for active B12 (holotranscobalamin) may be done to detect early deficiency.",
        "advice_high": "High serum B12 is most commonly due to B12 supplementation or regular consumption of B12-rich foods (meat, fish, eggs, dairy). This is generally not harmful, as excess B12 is water-soluble and excreted. However, significantly elevated levels without supplementation can sometimes be associated with liver conditions, certain blood disorders, or kidney disease, and may warrant further investigation by your GP.",
        "advice_low": "Low serum B12 can cause megaloblastic anaemia (large, abnormally formed red blood cells), neurological symptoms such as tingling or numbness in the hands and feet, memory problems, and fatigue. Deficiency is more common in vegans and vegetarians, older adults, and people with conditions affecting absorption (such as pernicious anaemia or after gastric surgery). Oral B12 supplements or dietary changes (more meat, fish, eggs, dairy, or fortified foods) are usually sufficient for mild deficiency. Your GP may recommend B12 injections if absorption is impaired or deficiency is severe."
    },
    "vitamin_a": {
        "name": "Vitamin A (Retinol)",
        "type": "hilo",
        "gender_specific": False,
        "range": (1.05, 3.50),
        "unit": "µmol/L",
        "explanation": "Vitamin A (retinol) is a fat-soluble vitamin essential for vision (particularly night vision), immune function, skin health, and cell growth and differentiation. Your body can also make vitamin A from beta-carotene found in orange and yellow vegetables. Because vitamin A is fat-soluble, it's stored in the liver, which means toxicity from excessive intake is possible — unlike water-soluble vitamins that are excreted in urine. Good dietary sources include liver, oily fish, dairy products, and eggs, while beta-carotene comes from carrots, sweet potatoes, and leafy greens.",
        "advice_high": "Elevated serum vitamin A usually results from very high supplement intake, particularly from preformed vitamin A (retinol) in high-dose supplements or excessive liver consumption. Toxicity (hypervitaminosis A) can cause headaches, nausea, liver damage, hair loss, dry skin, and in pregnant women can be teratogenic (harmful to the developing foetus). Review any supplements you're taking and discuss with your GP. Excess beta-carotene from food causes a harmless yellowing of the skin (carotenaemia) but doesn't raise retinol levels to toxic concentrations.",
        "advice_low": "Low vitamin A can lead to night blindness, dry eyes, dry skin, and impaired immune function. Deficiency is uncommon in the UK in people eating a balanced diet, but can occur with very restricted diets, fat malabsorption conditions (such as Crohn's disease or cystic fibrosis), or significant alcohol misuse. Increase your intake of vitamin A-rich foods such as liver (once a week), oily fish, eggs, and dairy, along with orange and yellow vegetables for beta-carotene. If a digestive condition is causing malabsorption, your GP can advise on targeted supplementation."
    },
    "vitamin_b1": {
        "name": "Vitamin B1 (Thiamine)",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (70, 180),
        "unit": "nmol/L",
        "explanation": "Thiamine (vitamin B1) is a water-soluble vitamin that plays a fundamental role in energy metabolism, helping cells convert carbohydrates into usable energy. It's particularly important for the nervous system, heart, and muscles, which have high energy demands. Because the body stores only small amounts of thiamine, deficiency can develop within weeks of inadequate intake. Thiamine deficiency is most commonly associated with heavy alcohol consumption (which impairs absorption and utilisation), but can also occur with severely restricted diets or certain medical conditions.",
        "advice_high": "Thiamine levels above the reference range are not typically a clinical concern. B1 is water-soluble, so excess is excreted in urine. No specific action is needed for a high result.",
        "advice_low": "Low thiamine can cause Wernicke's encephalopathy (a neurological emergency characterised by confusion, poor coordination, and eye problems) and Korsakoff syndrome (severe memory impairment). Earlier, less severe deficiency can manifest as fatigue, irritability, poor memory, muscle weakness, and tingling sensations. If you drink alcohol heavily, this is the most likely cause and stopping drinking is the priority alongside supplementation. For others, increasing thiamine-rich foods (whole grains, legumes, nuts, seeds, pork, and yeast extract) or taking a B-complex supplement is appropriate. Your GP may recommend high-dose thiamine if levels are very low."
    },
    "vitamin_b2": {
        "name": "Vitamin B2 (Riboflavin)",
        "type": "lower_bound",
        "gender_specific": False,
        "range": (106, 638),
        "unit": "nmol/L",
        "explanation": "Riboflavin (vitamin B2) is a water-soluble vitamin that acts as a building block for two important coenzymes involved in energy production and the metabolism of fats, drugs, and steroids. It also plays a role in maintaining normal levels of other B vitamins, including B6 and folate. Unlike some other vitamins, riboflavin deficiency is rarely severe in developed countries, but marginal deficiency is not uncommon, particularly in people with restricted diets, heavy alcohol use, or dairy-free diets. Good sources include dairy products, meat, fish, eggs, and fortified cereals.",
        "advice_high": "Riboflavin is water-soluble and excess is excreted in urine (which can turn a bright yellow colour when taking supplements). High levels from supplements are not considered harmful. No specific action is needed.",
        "advice_low": "Low riboflavin can cause mouth sores and cracks at the corners of the lips (angular cheilitis), a sore and magenta-coloured tongue (glossitis), skin rashes, and sensitivity to light. Because riboflavin is needed to activate other B vitamins, deficiency can also affect B6 and folate pathways. Increase riboflavin-rich foods: dairy products, meat and poultry, fish, eggs, and dark leafy greens are good sources. A B-complex supplement can provide all the B vitamins in balanced amounts. Avoid leaving food in bright light for long periods, as riboflavin is degraded by ultraviolet light."
    },
    "vitamin_b6": {
        "name": "Vitamin B6 (Pyridoxine)",
        "type": "hilo",
        "gender_specific": False,
        "range": (20, 200),
        "unit": "nmol/L",
        "explanation": "Vitamin B6 (pyridoxine) is a water-soluble vitamin involved in over 100 enzymatic reactions, most of which involve protein and amino acid metabolism. It's also needed to make neurotransmitters (including serotonin and dopamine), to produce haemoglobin, and to support immune function. Unlike many other water-soluble vitamins, vitamin B6 can cause neurological toxicity when taken in very high supplemental doses over prolonged periods, which is why both low and high levels are worth monitoring.",
        "advice_high": "Chronically elevated vitamin B6 is almost always due to high-dose supplementation (typically doses above 50-100 mg/day over a prolonged period) rather than dietary intake. This can cause peripheral neuropathy — numbness, tingling, and sensory changes in the hands and feet. If you're taking high-dose B6 supplements, reduce the dose and discuss with your GP. Levels from food alone are not harmful. Nerves typically recover slowly once supplementation is reduced.",
        "advice_low": "Low vitamin B6 can cause anaemia, peripheral neuropathy, skin conditions (seborrhoeic dermatitis), a sore tongue, and mood disturbances including depression and irritability. Deficiency is more common in older adults, people with autoimmune conditions, heavy drinkers, and those taking certain medications (including isoniazid for tuberculosis). Increasing vitamin B6-rich foods (poultry, fish, potatoes, bananas, chickpeas, fortified cereals) usually corrects mild deficiency. A B-complex supplement may be recommended if dietary changes are insufficient."
    },
    "vitamin_c": {
        "name": "Vitamin C",
        "type": "hilo",
        "gender_specific": False,
        "range": (23, 85),
        "unit": "µmol/L",
        "explanation": "Vitamin C (ascorbic acid) is a water-soluble antioxidant that is essential for the synthesis of collagen (a structural protein in skin, bones, blood vessels, and connective tissue), immune function, wound healing, and the absorption of non-haem iron from plant foods. Unlike most mammals, humans cannot synthesise vitamin C and must obtain it entirely from the diet. Citrus fruits, berries, kiwi, peppers, broccoli, and leafy greens are excellent sources. Because it's water-soluble, the body cannot store large amounts, so regular daily intake is important.",
        "advice_high": "High vitamin C levels are usually a result of supplementation and are generally not harmful as excess is excreted in urine. However, very high supplemental doses (above 1-2g/day) can occasionally cause digestive symptoms (nausea, diarrhoea, stomach cramps) and may increase the risk of kidney oxalate stones in susceptible individuals. If you're taking high-dose supplements, consider whether this is necessary and discuss with your GP if you have a history of kidney stones.",
        "advice_low": "Mild vitamin C deficiency can cause fatigue, poor wound healing, dry skin, and frequent infections. Severe deficiency leads to scurvy, characterised by bleeding gums, bruising, joint pain, and impaired wound healing — this is uncommon in developed countries but can occur in people with very restricted diets or malabsorption conditions. Increase your intake of fresh fruit and vegetables: a glass of orange juice, a portion of strawberries, half a red pepper, or a serving of broccoli each provides well over the recommended daily amount. Cooking destroys some vitamin C, so raw or lightly cooked vegetables help preserve it."
    },
    "vitamin_e": {
        "name": "Vitamin E (Alpha-Tocopherol)",
        "type": "hilo",
        "gender_specific": False,
        "range": (11.6, 46.4),
        "unit": "µmol/L",
        "explanation": "Vitamin E is a fat-soluble antioxidant that protects cell membranes from oxidative damage. Alpha-tocopherol is the most active form in the human body. It works alongside vitamin C and other antioxidants to neutralise free radicals, supports immune function, and helps prevent the oxidation of LDL cholesterol (which is an early step in the formation of artery plaques). Good dietary sources include nuts and seeds (especially sunflower seeds and almonds), vegetable oils, avocados, and leafy green vegetables.",
        "advice_high": "Elevated vitamin E levels are almost always due to high-dose supplementation. While dietary vitamin E is safe, very high supplemental doses (above ~400 IU/day consistently) may interfere with vitamin K's role in blood clotting, increasing bleeding risk. If you're taking high-dose vitamin E supplements, particularly alongside blood-thinning medication, discuss this with your GP. Levels from food sources alone are extremely unlikely to cause harm.",
        "advice_low": "Low vitamin E can impair antioxidant defences, potentially increasing cellular damage from oxidative stress. Clinical deficiency is rare in healthy adults but can occur with fat malabsorption conditions (such as cystic fibrosis, Crohn's disease, or cholestatic liver disease) because vitamin E requires fat for absorption. Symptoms of severe deficiency include muscle weakness, neurological problems, and a tendency to infections. Include more nuts, seeds, vegetable oils, and green leafy vegetables in your diet. If a fat malabsorption condition is suspected, discuss supplementation with your GP."
    },
    "beta_carotene": {
        "name": "Beta-Carotene",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.19, 2.53),
        "unit": "µmol/L",
        "explanation": "Beta-carotene is a plant pigment that gives orange, yellow, and some green vegetables their colour. It's a precursor to vitamin A: your body can convert it to retinol as needed, making it a safe dietary source of vitamin A without the toxicity risk of preformed vitamin A (retinol) in high doses. Beta-carotene also functions as a direct antioxidant in its own right. Serum beta-carotene reflects both dietary intake and the body's ability to absorb fat-soluble nutrients, making it a useful marker of fruit and vegetable intake and nutritional status.",
        "advice_high": "Very high beta-carotene levels from dietary sources (eating large quantities of carrots, sweet potatoes, or other carotenoid-rich foods) cause carotenaemia, a harmless yellowing of the skin particularly visible on the palms and soles. This resolves when intake is reduced. Unlike preformed vitamin A, beta-carotene from food does not cause vitamin A toxicity. High-dose beta-carotene supplements, however, have been associated with increased lung cancer risk in smokers and should be avoided in that group.",
        "advice_low": "Low beta-carotene typically reflects a diet low in fruits and vegetables, fat malabsorption (which impairs carotenoid absorption), or heavy smoking. It suggests your antioxidant intake from plant foods may be insufficient. Increasing your consumption of colourful fruits and vegetables — particularly carrots, sweet potatoes, butternut squash, spinach, kale, and apricots — is the most straightforward way to raise levels. Eating these foods with a small amount of fat improves absorption significantly."
    },
}


HORMONES = {
    "fsh": {
        "name": "Follicle Stimulating Hormone (FSH)",
        "type": "hilo",
        "gender_specific": True,
        "range": (1.5, 21.5, 1.5, 12.4),
        "unit": "IU/L",
        "explanation": "FSH is produced by the pituitary gland and plays a central role in reproductive function. In women, it stimulates the growth and maturation of ovarian follicles (which contain eggs) and triggers oestrogen production. In men, it stimulates sperm production in the testes. FSH levels fluctuate throughout the menstrual cycle in women, rising sharply mid-cycle to trigger ovulation, so the same level can be entirely normal or abnormal depending on the phase of the cycle. In women approaching or after menopause, FSH rises substantially as the pituitary tries harder to stimulate increasingly unresponsive ovaries.",
        "advice_high": "In premenopausal women, a high FSH may indicate reduced ovarian reserve (fewer good-quality follicles remaining), which can affect fertility, or may reflect an early transition towards menopause. Very high FSH alongside irregular or absent periods may indicate premature ovarian insufficiency. In men, high FSH can point to impaired sperm production or testicular problems. In all cases, a raised FSH should be discussed with a GP or specialist, who will consider your age, symptoms, and cycle history when interpreting the result.",
        "advice_low": "Low FSH may indicate a problem with the pituitary gland's ability to produce sufficient hormones, which can affect reproductive function and fertility. This can result from excessive exercise, significant underweight or malnutrition, high stress, pituitary conditions, or certain medications. In women it may be associated with infrequent or absent periods. Your GP will look at this alongside other hormones (LH, oestradiol, prolactin) and your symptoms to identify the cause."
    },
    "lh": {
        "name": "Luteinising Hormone (LH)",
        "type": "hilo",
        "gender_specific": True,
        "range": (1.0, 12.6, 1.7, 8.6),
        "unit": "IU/L",
        "explanation": "LH is produced by the pituitary gland alongside FSH. In women, LH levels surge dramatically at mid-cycle to trigger ovulation — the release of a mature egg. After ovulation, LH stimulates the corpus luteum (the remnant of the follicle) to produce progesterone. In men, LH stimulates the Leydig cells in the testes to produce testosterone. LH is highly pulse-dependent and varies significantly across the menstrual cycle in women, so the clinical significance of a single measurement depends heavily on the timing and context.",
        "advice_high": "In women, a high LH outside the expected mid-cycle peak — particularly when combined with a high LH:FSH ratio — is associated with polycystic ovary syndrome (PCOS). High LH in postmenopausal women is normal. In men, elevated LH alongside low testosterone suggests the testes are not responding adequately (primary hypogonadism). Your GP will interpret this result in the context of your cycle phase, symptoms, and other hormone levels.",
        "advice_low": "Low LH may reflect hypothalamic-pituitary dysfunction, which can result from excessive exercise, low body weight, chronic stress, or conditions affecting the pituitary gland. It can contribute to irregular or absent menstrual cycles in women and low testosterone in men. Your GP will assess this alongside other reproductive hormones and your overall health picture."
    },
    "testosterone": {
        "name": "Testosterone (Total)",
        "type": "hilo",
        "gender_specific": True,
        "range": (0.3, 2.8, 9.0, 29.0),
        "unit": "nmol/L",
        "explanation": "Testosterone is the primary male sex hormone, though it's present and important in both sexes. In men, it's responsible for the development of male secondary sexual characteristics, libido, muscle and bone mass, mood, and energy. In women, testosterone is produced in smaller amounts by the ovaries and adrenal glands and plays a role in libido, energy, bone density, and overall wellbeing. Blood levels of testosterone fluctuate during the day (highest in the morning) and are influenced by sleep, exercise, stress, and weight.",
        "advice_high": "In women, elevated testosterone is associated with polycystic ovary syndrome (PCOS), adrenal conditions, or use of certain medications or supplements. Symptoms can include acne, excess hair growth (hirsutism), irregular periods, and in some cases deepening of the voice. In men, high testosterone may result from anabolic steroid use or, rarely, certain tumours. Discuss this result with your GP, who will consider your symptoms and may arrange further hormone testing.",
        "advice_low": "In men, low testosterone (hypogonadism) can cause fatigue, reduced libido, erectile dysfunction, low mood, difficulty concentrating, reduced muscle mass, and bone loss. Common causes include ageing, obesity, chronic illness, stress, or pituitary problems. Lifestyle factors such as improving sleep, regular exercise, and weight loss can help. Your GP may consider testosterone replacement therapy if levels are consistently low with significant symptoms. In women, very low testosterone can contribute to low energy, reduced libido, and mood changes; discuss with your GP if this applies."
    },
    "free_testosterone": {
        "name": "Free Testosterone",
        "type": "hilo",
        "gender_specific": True,
        "range": (1, 12, 150, 500),
        "unit": "pmol/L",
        "explanation": "Most testosterone in the blood is bound to proteins (mainly sex hormone binding globulin and albumin) and is unavailable for use by cells. Free testosterone is the unbound fraction — typically just 1-3% of the total — and is the portion that is biologically active. It's often a more useful measure than total testosterone when SHBG levels are abnormal (SHBG rises with age, liver disease, and oestrogen, and falls with obesity and hypothyroidism), because changes in SHBG can make total testosterone misleading.",
        "advice_high": "Elevated free testosterone in women is often associated with PCOS, adrenal conditions, or exogenous androgen use, and may cause symptoms such as acne, excess hair, and irregular periods. In men, significantly high free testosterone may result from anabolic steroid use. Discuss with your GP, who will look at this alongside total testosterone and SHBG.",
        "advice_low": "Low free testosterone despite normal total testosterone can occur when SHBG is elevated, leaving less testosterone in the active unbound state. In men, this can contribute to fatigue, reduced libido, and low mood. In women, very low free testosterone may affect energy and libido. Your GP will interpret this result alongside SHBG and total testosterone levels."
    },
    "oestradiol": {
        "name": "Oestradiol (E2)",
        "type": "hilo",
        "gender_specific": True,
        "range": (77, 921, 28, 156),
        "unit": "pmol/L",
        "explanation": "Oestradiol is the most potent and predominant form of oestrogen in the body. In women, it's produced primarily by the ovaries and plays a central role in the menstrual cycle, female secondary sexual characteristics, bone density, cardiovascular health, and mood. Levels fluctuate considerably across the menstrual cycle — rising in the follicular phase to stimulate follicle growth, peaking just before ovulation, and falling during the luteal phase. After menopause, oestradiol levels drop dramatically. In men, oestradiol is produced in small amounts from testosterone and plays a role in bone health, libido, and brain function.",
        "advice_high": "In women of reproductive age, high oestradiol may reflect the normal mid-cycle peak, stimulated follicle development (in fertility treatment), or occasionally ovarian cysts or tumours. In men, elevated oestradiol can cause gynaecomastia (breast tissue development), reduced libido, and other feminising effects — this can result from obesity (fat tissue converts testosterone to oestradiol), liver disease, certain medications, or, rarely, testicular conditions. Your GP will interpret this result in the context of your cycle phase (for women), symptoms, and other hormone levels.",
        "advice_low": "In premenopausal women, low oestradiol can cause irregular or absent periods, hot flushes, vaginal dryness, mood changes, and reduced bone density. Causes include premature ovarian insufficiency, hypopituitarism, excessive exercise, significant underweight, or stress. In postmenopausal women, low oestradiol is expected. In men, very low levels can affect bone density and libido. Your GP will assess this alongside your symptoms, FSH/LH levels, and overall health."
    },
    "progesterone": {
        "name": "Progesterone",
        "type": "hilo",
        "gender_specific": True,
        "range": (0.18, 75.9, 0.15, 1.40),
        "unit": "nmol/L",
        "explanation": "Progesterone is a steroid hormone produced mainly by the corpus luteum in the ovary after ovulation (the luteal phase) and by the placenta during pregnancy. It prepares the uterus lining for implantation of a fertilised egg and maintains early pregnancy. Outside of pregnancy, progesterone levels are low in the follicular phase and rise substantially after ovulation — this is why a progesterone blood test taken around day 21 of a 28-day cycle is used to confirm that ovulation has occurred. In men, progesterone is produced in small amounts by the adrenal glands and testes.",
        "advice_high": "Elevated progesterone outside of pregnancy most commonly indicates that you are in the mid-luteal phase of your cycle or that you're taking progesterone-containing medication (such as some contraceptives or hormone replacement therapy). Rarely, very high levels can indicate certain adrenal or ovarian conditions. Your GP will consider the timing of your test in relation to your cycle when interpreting this result.",
        "advice_low": "In women trying to conceive, a low mid-luteal progesterone (typically checked around day 21) suggests ovulation may not have occurred, or that the luteal phase is insufficient to support implantation. Other causes of low progesterone include stress, excessive exercise, low body weight, or conditions affecting ovarian function. If you're not trying to conceive, low progesterone may still explain symptoms such as irregular periods, premenstrual spotting, or mood changes. Your GP can advise on whether any intervention is appropriate."
    },
    "prolactin": {
        "name": "Prolactin",
        "type": "hilo",
        "gender_specific": True,
        "range": (102, 496, 86, 324),
        "unit": "mIU/L",
        "explanation": "Prolactin is a hormone produced by the pituitary gland, best known for stimulating milk production after childbirth. It's present at low levels in everyone (not just new mothers). Prolactin levels are naturally higher during pregnancy and breastfeeding. A single mildly elevated prolactin result can be caused by everyday factors such as stress, strenuous exercise, sexual activity, or having eaten recently before the test, all of which can transiently raise levels. Persistently elevated prolactin (hyperprolactinaemia) can, however, affect reproductive function in both men and women.",
        "advice_high": "An elevated prolactin is fairly common as a one-off result due to transient causes (stress, exercise, recent eating). If it's persistently elevated on repeat testing under relaxed fasting conditions, it should be investigated. Causes of true hyperprolactinaemia include a prolactin-secreting pituitary adenoma (prolactinoma, which is usually benign), certain medications (including antipsychotics, antidepressants, and stomach medications like metoclopramide), hypothyroidism, and kidney or liver disease. In women, high prolactin can cause irregular or absent periods, infertility, and unexpected milk production. In men, it can cause reduced libido, erectile dysfunction, and gynaecomastia. Treatment depends on the cause.",
        "advice_low": "Low prolactin levels are not typically a clinical concern and do not require specific action."
    },
    "shbg": {
        "name": "Sex Hormone Binding Globulin (SHBG)",
        "type": "hilo",
        "gender_specific": True,
        "range": (18, 144, 13, 71),
        "unit": "nmol/L",
        "explanation": "SHBG is a protein made by the liver that binds tightly to sex hormones — primarily testosterone and to a lesser extent oestradiol — transporting them in the blood. Hormones bound to SHBG are inactive; only unbound (free) hormones are biologically available to cells. SHBG levels profoundly affect how much active sex hormone your body has available. Higher SHBG means less free hormone; lower SHBG means more. Many factors influence SHBG: it rises with oestrogen, ageing, hyperthyroidism, and liver disease; it falls with obesity, insulin resistance, hypothyroidism, and androgenic steroids.",
        "advice_high": "High SHBG means more of your testosterone and oestradiol is bound and inactive, potentially leaving you with less bioavailable hormone than your total levels suggest. In women, this can contribute to symptoms of low androgen (fatigue, low libido, mood changes). In men, very high SHBG can mask functional testosterone deficiency. The cause of high SHBG should be explored — possibilities include hyperthyroidism, liver conditions, anorexia, or high oestrogen states. Your GP will look at this alongside total and free sex hormone levels.",
        "advice_low": "Low SHBG means more of your sex hormones are circulating freely. In women, this is associated with insulin resistance, obesity, PCOS, hypothyroidism, and high androgen levels — it effectively amplifies androgenic effects and is a marker of metabolic risk. In men, low SHBG may indicate insulin resistance and is associated with an increased risk of type 2 diabetes and cardiovascular disease. Improving insulin sensitivity through a healthier diet, regular exercise, and weight loss if appropriate can help normalise SHBG levels."
    },
    "free_androgen_index": {
        "name": "Free Androgen Index (FAI)",
        "type": "hilo",
        "gender_specific": True,
        "range": (0.5, 5.0, 30, 80),
        "unit": "%",
        "explanation": "The Free Androgen Index (FAI) is a calculated ratio that estimates the level of biologically active (free) testosterone. It's calculated as: (Total Testosterone ÷ SHBG) × 100. In women, it's a clinically useful marker for assessing androgen status, particularly in the investigation of PCOS, where excessive androgen activity is common. A high FAI in women suggests more free testosterone is available than normal. In men, where free testosterone is more commonly measured directly, FAI provides an indirect estimate of androgen bioavailability.",
        "advice_high": "In women, a high FAI suggests excess free androgen activity, which is the hallmark finding in PCOS. This can be associated with irregular periods, acne, excess facial or body hair (hirsutism), and fertility difficulties. Other causes include congenital adrenal hyperplasia or androgen-secreting tumours (rare). Your GP will interpret this alongside clinical symptoms, ultrasound findings, and other hormone tests. Lifestyle interventions (regular exercise, reducing refined carbohydrates, weight management if appropriate) can reduce androgen activity in insulin-resistant women with PCOS.",
        "advice_low": "In women, a low FAI suggests low androgen bioavailability, which can contribute to fatigue, low libido, reduced motivation, and mood changes. This can occur with elevated SHBG (which binds up more testosterone) or genuinely low testosterone production. In men, a low FAI suggests functional androgen deficiency. Your GP will consider this alongside symptoms and other hormone levels when deciding if any treatment is appropriate."
    },
}

MINERALS = {
    "magnesium": {
        "name": "Magnesium",
        "type": "hilo",
        "gender_specific": False,
        "range": (0.70, 1.00),
        "unit": "mmol/L",
        "explanation": "Magnesium is the fourth most abundant mineral in the body and is involved in over 300 enzymatic reactions, including energy production, protein synthesis, DNA repair, muscle contraction, nerve function, and blood sugar regulation. About 60% of the body's magnesium is stored in bones, with most of the rest in muscle and soft tissue. Only about 1% circulates in the blood, which is why blood levels don't always reflect total body stores — normal serum magnesium can coexist with intracellular deficiency. Good dietary sources include nuts, seeds, dark chocolate, leafy greens, legumes, and whole grains.",
        "advice_high": "Elevated serum magnesium (hypermagnesaemia) is uncommon in people with normal kidney function, as the kidneys efficiently excrete excess magnesium. It most often occurs in people with kidney disease or those taking large doses of magnesium-containing antacids or laxatives. Mild hypermagnesaemia may cause flushing, nausea, and low blood pressure. Higher levels can cause muscle weakness, slowed breathing, and heart rhythm problems. If you have kidney disease, discuss your magnesium intake with your GP.",
        "advice_low": "Low magnesium (hypomagnesaemia) can cause muscle cramps, twitching, fatigue, insomnia, anxiety, irregular heart rhythm, and headaches. It's more common than often recognised and can result from a diet low in magnesium-rich foods, heavy alcohol use, medications (including proton pump inhibitors and some diuretics), or conditions causing excessive gastrointestinal losses. Increase your intake of magnesium-rich foods — nuts (especially almonds and cashews), pumpkin seeds, dark chocolate, spinach, and whole grains. A magnesium supplement (magnesium glycinate or citrate are well absorbed) may be recommended by your GP if levels remain low."
    },
    "copper": {
        "name": "Copper",
        "type": "hilo",
        "gender_specific": True,
        "range": (12.6, 24.4, 11.0, 22.0),
        "unit": "µmol/L",
        "explanation": "Copper is an essential trace mineral involved in the production of red blood cells, collagen and connective tissue formation, iron metabolism, and the functioning of several important enzymes. It's also a component of the antioxidant enzyme superoxide dismutase. Women typically have slightly higher copper levels than men, partly because oestrogen increases copper levels. Good dietary sources include shellfish (especially oysters), liver, nuts, seeds, dark chocolate, and whole grains. Copper balance is closely linked to zinc intake, as high zinc supplementation can deplete copper.",
        "advice_high": "Elevated copper can occur with liver disease (the liver regulates copper metabolism), oestrogen therapy or pregnancy (which raise copper-binding proteins), chronic inflammation, or, rarely, the genetic condition Wilson's disease, in which copper accumulates in the liver, brain, and other organs. Your GP will look at this in the context of your liver function tests and other results. Reducing high-dose zinc supplementation (which can impair copper metabolism in some contexts) and limiting dietary copper-rich foods may be advised if levels are significantly elevated.",
        "advice_low": "Low copper can cause anaemia (copper is needed for iron absorption and red blood cell formation), fatigue, poor immune function, and neurological symptoms including weakness and balance problems. Deficiency is uncommon but can occur with excessive zinc supplementation (zinc and copper compete for absorption), malabsorption conditions, bariatric surgery, or prolonged parenteral nutrition. Include more copper-rich foods in your diet (shellfish, liver, nuts, seeds, legumes), and if you take zinc supplements, ensure the dose is not excessive. Your GP may recommend copper supplementation if levels are significantly low."
    },
    "red_cell_magnesium": {
        "name": "Red Cell Magnesium",
        "type": "hilo",
        "gender_specific": False,
        "range": (1.65, 2.65),
        "unit": "mmol/L",
        "explanation": "Red cell magnesium measures the magnesium content inside red blood cells, rather than in the liquid portion of the blood (serum). Because most of the body's magnesium is intracellular, red cell magnesium is considered a more sensitive marker of total body magnesium status than serum magnesium alone. A person can have a normal serum magnesium while their intracellular stores are depleted, making this test particularly useful for identifying magnesium deficiency that serum testing might miss. The test is most helpful when symptoms suggest magnesium deficiency despite a normal serum level.",
        "advice_high": "Elevated red cell magnesium is unusual and generally not a clinical concern. It may be seen with very high magnesium supplementation. If you're supplementing magnesium, discuss the dose with your GP.",
        "advice_low": "Low red cell magnesium indicates that intracellular magnesium stores are depleted, which may persist even when serum magnesium appears normal. This is a more sensitive indicator of functional magnesium deficiency and can be associated with symptoms such as muscle cramps, fatigue, poor sleep, irritability, and heart palpitations. The approach is the same as for low serum magnesium: increase magnesium-rich foods (nuts, seeds, dark leafy greens, whole grains, dark chocolate) and consider a well-absorbed magnesium supplement (glycinate or citrate). Address any underlying causes such as heavy alcohol use or medications that deplete magnesium, and discuss with your GP."
    },
}

DIGESTIVE_ENZYMES = {
    "amylase": {
        "name": "Amylase",
        "type": "hilo",
        "gender_specific": False,
        "range": (30, 110),
        "unit": "U/L",
        "explanation": "Amylase is an enzyme produced primarily by the pancreas and the salivary glands that breaks down carbohydrates (starches) into sugars. Small amounts are normally present in the blood, but when the pancreas becomes inflamed or damaged, amylase leaks out in larger quantities, causing blood levels to rise sharply. Because amylase also comes from the salivary glands, elevated levels can occasionally result from non-pancreatic causes. Amylase levels rise and fall more quickly than lipase, meaning it may return to normal within 2-3 days of an acute episode, even if the underlying problem persists.",
        "advice_high": "A significantly elevated amylase is most commonly associated with acute pancreatitis (sudden inflammation of the pancreas) or a blocked pancreatic duct. Other causes include salivary gland inflammation (mumps), bowel obstruction, or kidney problems (since amylase is excreted by the kidneys). If you're experiencing severe abdominal pain, particularly in the upper abdomen radiating to the back, nausea, and vomiting, seek medical attention promptly, as acute pancreatitis can be serious. Common triggers include gallstones and heavy alcohol consumption. Mildly elevated amylase without symptoms may be investigated further but is often less urgent.",
        "advice_low": "Low amylase can occasionally be seen in chronic pancreatitis (where long-term damage reduces the pancreas's ability to produce enzymes) or in conditions causing the replacement of pancreatic tissue. If combined with digestive symptoms such as fatty stools, bloating, or weight loss, this may indicate exocrine pancreatic insufficiency and warrants further investigation. Mention this result to your GP alongside any relevant symptoms."
    },
    "lipase": {
        "name": "Lipase",
        "type": "hilo",
        "gender_specific": False,
        "range": (13, 60),
        "unit": "U/L",
        "explanation": "Lipase is an enzyme produced almost exclusively by the pancreas that breaks down fats (triglycerides) during digestion. Because it's so specific to the pancreas, elevated serum lipase is a more specific marker of pancreatic injury than amylase. Importantly, lipase remains elevated in the blood for longer than amylase after an acute episode (up to 2 weeks), making it a more sensitive test for pancreatitis when there's been a delay between the event and the blood test.",
        "advice_high": "Elevated lipase strongly suggests pancreatic inflammation or injury, with acute pancreatitis being the most common cause. Very high levels (more than three times the upper limit) are particularly significant. Other causes include pancreatic duct obstruction, chronic pancreatitis, and occasionally bowel conditions. If you're experiencing upper abdominal pain radiating to the back, nausea, or vomiting, seek medical attention promptly. Avoiding alcohol and following a low-fat diet during recovery from pancreatitis episodes is important. Your GP will investigate the underlying cause.",
        "advice_low": "Low lipase can occur in advanced chronic pancreatitis where the gland has lost significant enzyme-producing capacity. This may be associated with fat malabsorption (greasy, floating stools), weight loss, and nutritional deficiencies. If you have symptoms suggesting fat malabsorption, mention this result to your GP, who may arrange further pancreatic function tests and consider enzyme replacement therapy."
    },
}

INFLAMMATORY_MARKERS = {
    "esr": {
        "name": "Erythrocyte Sedimentation Rate (ESR)",
        "type": "upper_bound",
        "gender_specific": True,
        "range": (0, 20, 0, 15),
        "unit": "mm/hr",
        "explanation": "ESR measures how quickly red blood cells settle to the bottom of a test tube over one hour. When there is inflammation anywhere in the body, proteins such as fibrinogen and immunoglobulins cause red blood cells to clump together and fall more quickly, raising the ESR. It's a non-specific marker: it can be elevated by many conditions, from infections and autoimmune diseases to malignancy, anaemia, and even ageing. ESR tends to rise and fall more slowly than other inflammatory markers like CRP, making it useful for tracking chronic inflammatory conditions over time. Women naturally have slightly higher ESR values than men.",
        "advice_high": "An elevated ESR indicates inflammation somewhere in the body, but doesn't identify the source. In the context of specific symptoms, it can support diagnoses such as rheumatoid arthritis, other autoimmune conditions, infections, temporal arteritis (especially important in older adults with headaches), or malignancy. A mildly elevated ESR with no symptoms is common and often has a benign explanation, including age-related changes or anaemia. Your GP will interpret this result alongside your symptoms, other blood tests, and clinical examination. If ESR is very high or accompanied by concerning symptoms, further investigation will be arranged.",
        "advice_low": "A low or normal ESR is reassuring and suggests significant systemic inflammation is unlikely at the time of testing. No action is needed based on this finding alone."
    },
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
BLOOD_METRIC_DATA.update(HORMONES)
BLOOD_METRIC_DATA.update(MINERALS)
BLOOD_METRIC_DATA.update(DIGESTIVE_ENZYMES)
BLOOD_METRIC_DATA.update(INFLAMMATORY_MARKERS)

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
    metric_type = data.get("type", "hilo")
    if metric_type == "lower_bound":
        # Only the low end matters — being high is not abnormal
        if data["value"] < low_end:
            status = "Low"
            advice = data.get("advice_low", "See a healthcare professional for specific advice.")
        else:
            status = "Normal"
            advice = "Maintain your current healthy lifestyle."
    elif metric_type == "upper_bound":
        # Only the high end matters — being low is not abnormal
        if data["value"] > high_end:
            status = "High"
            advice = data.get("advice_high", "See a healthcare professional for specific advice.")
        else:
            status = "Normal"
            advice = "Maintain your current healthy lifestyle."
    else:
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