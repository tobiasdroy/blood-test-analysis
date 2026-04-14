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
    }
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
    }
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
    }
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
    }
}

URINE_ANALYSIS = {
    "ph": {
        "name": "pH",
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
        "name": "Ketones",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "mg/dL",
        "explanation": "Ketones are produced when your body burns fat for energy instead of glucose. This happens when glucose isn't readily available, such as during fasting, prolonged exercise, a very low-carbohydrate or ketogenic diet, or when your body can't use glucose properly (as in uncontrolled diabetes). Small amounts of ketones in urine can be normal in certain circumstances, but larger amounts may need investigation.",
        "advice_high": "Ketones in your urine can be perfectly harmless if you've been fasting, following a low-carbohydrate diet, doing intense or prolonged exercise, or if you were unwell with vomiting or reduced food intake around the time of the test. However, for people with diabetes (especially type 1), significant ketones in the urine can indicate diabetic ketoacidosis (DKA), a serious condition that needs urgent medical attention. If you have diabetes and are feeling unwell with nausea, abdominal pain, rapid breathing, or confusion, seek medical help immediately. If you don't have diabetes and the ketones are likely from diet or fasting, no action is usually needed.",
        "advice_low": "Absence of ketones in your urine is the expected, normal finding when your body is using glucose as its primary energy source."    
    },
    "wbcs": {
        "name": "White Blood Cells",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "White blood cells in your urine indicate that your immune system is responding to something in your urinary tract. In small numbers they can be normal, but higher levels suggest inflammation or infection somewhere along the tract (kidneys, ureters, bladder, or urethra). A urinary tract infection (UTI) is by far the most common cause, particularly in women.",
        "advice_high": "White blood cells in your urine most likely indicate a urinary tract infection, especially if you're also experiencing symptoms like a burning sensation when urinating, needing to go more frequently, lower abdominal discomfort, or cloudy or strong-smelling urine. Contact your GP, who may prescribe a short course of antibiotics after confirming the infection. In the meantime, drink plenty of water to help flush bacteria from your system. If you're getting recurrent UTIs, your doctor can advise on prevention strategies. Less common causes of urinary white cells include kidney inflammation, sexually transmitted infections, or contamination of the sample.",
        "advice_low": "Absence of white blood cells in your urine is the expected, normal finding. It indicates no active infection or inflammation in your urinary tract." 
    },
    "rbcs": {
        "name": "Red Blood Cells",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cells/µL",
        "explanation": "Red blood cells in urine (haematuria) means there is some blood in your urine, whether visible to the eye or only detectable under a microscope. The blood can come from anywhere along the urinary tract: the kidneys, ureters, bladder, or urethra. There are many possible causes, ranging from completely benign to those that warrant investigation. In women, contamination from menstrual blood is a common and harmless reason for a positive result.",
        "advice_high": "Finding red blood cells in your urine doesn't automatically mean something serious is wrong. Common benign causes include urinary tract infections, vigorous exercise (especially running), kidney stones, menstrual contamination in women, and minor irritation of the urethra. However, because haematuria can occasionally indicate conditions that need treatment (such as bladder or kidney problems), your GP will typically want to investigate. They may repeat the urine test, check your kidney function with a blood test, arrange an ultrasound, or refer you for further evaluation depending on your age, symptoms, and other risk factors. Don't delay in mentioning this result to your doctor.",
        "advice_low": "Absence of red blood cells in your urine is the expected, normal finding." 
    },
    "casts": {
        "name": "Casts",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "casts/µL",
        "explanation": "Casts are tiny tube-shaped particles that form inside the kidney's tubules (the microscopic tubes where urine is produced). They're made of protein, cells, or other material that has moulded to the shape of the tubule, a bit like a jelly mould. Different types of casts can point to different conditions. Hyaline casts (made of pure protein) can appear in healthy people after exercise or dehydration, while other types (red cell casts, white cell casts, granular casts) are more significant and suggest kidney inflammation or damage.",
        "advice_high": "The presence of casts in your urine suggests something is happening in the kidneys that warrants a closer look. The significance depends on what type of casts were found: hyaline casts after exercise or dehydration are usually harmless, while other types may indicate kidney inflammation (nephritis), infection, or other kidney conditions. Your GP will interpret this alongside your other urine and blood results and may refer you for further kidney function assessment if needed. Staying well hydrated and avoiding excessive use of anti-inflammatory painkillers supports kidney health in the meantime.",
        "advice_low": "Absence of casts in your urine is the expected, normal finding." 
    },
    "bacterial_count": {
        "name": "Bacterial Count",
        "type": "presence",
        "gender_specific": False,
        "range": (0, 0),
        "unit": "cfu/mL",
        "explanation": "This measures the number of bacteria present in your urine sample. Healthy urine is normally sterile (free of bacteria), so the presence of significant numbers of bacteria usually indicates an infection in the urinary tract. However, some contamination can occur during sample collection (especially if the sample wasn't a 'clean catch' midstream sample), so a small number of bacteria doesn't always mean infection.",
        "advice_high": "A significant bacterial count in your urine strongly suggests a urinary tract infection (UTI), especially if white blood cells are also present and you have symptoms such as burning or pain when urinating, frequent urination, urgency, lower abdominal pain, or cloudy and strong-smelling urine. Contact your GP, who may prescribe antibiotics based on the type of bacteria found. Drink plenty of water to help flush bacteria from your system. If this is a recurrent problem, your GP can discuss prevention strategies and may want to investigate whether there's an underlying cause. If you have no symptoms, your doctor may want to repeat the test to rule out contamination before starting treatment.",
        "advice_low": "Absence of bacteria in your urine is the expected, normal finding. It confirms there's no urinary tract infection." 
    }
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
    }
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