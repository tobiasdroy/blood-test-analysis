# New Metrics — Clinical Advisor Review

**Date:** 7 May 2026  
**Prepared by:** Development team  
**Purpose:** 36 new blood test metrics have been added to the interpreter. Please review the reference ranges, units, explanations, and advice text below and flag any corrections.

---

## How to read this document

Each entry shows:
- **Internal key** (used in CSV uploads)
- **Display name**
- **Reference range(s)** and **unit**
- **Explanation** (shown to the patient)
- **Advice (High)** and **Advice (Low)** (or just one where the metric is one-directional)

---

## Group 1: Heart Health additions

### `apo_b_a1_ratio` — Apolipoprotein B/A1 Ratio
**Type:** Upper bound (high = concern)  
**Reference range:** Female ≤ 0.8 | Male ≤ 0.9  
**Unit:** ratio (dimensionless)

> **Explanation:** The Apolipoprotein B/A1 ratio compares the amount of atherogenic (artery-damaging) ApoB particles against the cardioprotective ApoA1 particles. A lower ratio means relatively more protective HDL-associated particles compared to harmful ones, which is favourable. Many cardiologists consider this ratio one of the most informative single markers for cardiovascular risk, as it captures both sides of the equation simultaneously. The threshold differs slightly between men and women because women typically have higher ApoA1 levels.

> **Advice (High):** A high ApoB/A1 ratio means you have more harmful lipoprotein particles relative to protective ones, which increases cardiovascular risk. The most effective actions are the same as for managing LDL and HDL individually: reduce saturated fat, eat more fibre and healthy fats (olive oil, oily fish, nuts), exercise regularly, quit smoking, and maintain a healthy weight. These changes tend to lower ApoB and raise ApoA1 simultaneously, improving the ratio from both ends. If your ratio remains elevated after lifestyle changes, your GP may consider medication.

> **Advice (Low/Normal):** A low ApoB/A1 ratio is a favourable finding, indicating a good balance between harmful and protective lipoproteins. Continue with the habits supporting this.

---

### `non_hdl_cholesterol` — Non-HDL Cholesterol
**Type:** Upper bound (high = concern)  
**Reference range:** ≤ 3.36 mmol/L  
**Unit:** mmol/L  
*(Based on NICE guidelines: desirable non-HDL < 3.4 mmol/L)*

> **Explanation:** Non-HDL cholesterol is calculated by subtracting your HDL ('good') cholesterol from your total cholesterol. The result captures all the potentially atherogenic (artery-damaging) lipoproteins in a single number: LDL, VLDL, IDL, and lipoprotein(a). Some guidelines prefer it over LDL alone because it includes these other harmful particles. It's particularly useful when triglycerides are elevated, as high triglycerides can make LDL calculations less accurate.

> **Advice (High):** Elevated non-HDL cholesterol means the combined burden of harmful lipoproteins in your blood is higher than ideal, raising cardiovascular risk. The approach is the same as for reducing LDL: cut saturated fat, increase fibre and omega-3 fats, exercise regularly, avoid smoking, and maintain a healthy weight. If other risk factors are present, your GP may discuss lipid-lowering medication.

---

### `vldl` — VLDL Cholesterol (Very Low-Density Lipoprotein Calculated)
**Type:** Upper bound (high = concern)  
**Reference range:** ≤ 1.65 mmol/L  
**Unit:** mmol/L  
*(Calculated as approximately triglycerides ÷ 2.18)*

> **Explanation:** Very low-density lipoprotein (VLDL) is produced by the liver and carries triglycerides to tissues throughout the body. After delivering triglycerides, VLDL is converted into LDL. Elevated VLDL is closely linked to high triglycerides, and high levels contribute to the build-up of plaques in artery walls. VLDL is usually calculated rather than directly measured, often estimated as approximately one-fifth of your triglyceride level.

> **Advice (High):** High VLDL reflects excess triglycerides being transported in your blood, which is associated with cardiovascular risk and often with metabolic syndrome. The same lifestyle changes that lower triglycerides will reduce VLDL: cutting sugar and refined carbohydrates, reducing alcohol, eating more omega-3 fats from oily fish, exercising regularly, and losing excess weight. If levels remain elevated, your GP may consider medication.

---

### `homocysteine` — Homocysteine
**Type:** Upper bound (high = concern)  
**Reference range:** ≤ 10 µmol/L  
**Unit:** µmol/L  
*(Optimal < 10 µmol/L; borderline 10–15; elevated > 15)*

> **Explanation:** Homocysteine is an amino acid produced naturally during the metabolism of another amino acid, methionine, which comes from dietary protein. Normally, B vitamins (particularly B6, B12, and folate) recycle homocysteine back into useful compounds. When these B vitamins are insufficient, or in certain genetic conditions, homocysteine accumulates in the blood. Elevated homocysteine is linked to increased cardiovascular risk, as well as to cognitive decline and bone health. It's both a nutritional and a cardiovascular risk marker.

> **Advice (High):** Elevated homocysteine is most commonly caused by low levels of folate, vitamin B12, or vitamin B6. The first step is to increase your intake of these vitamins through diet (dark leafy greens, legumes, whole grains, meat, fish, eggs, dairy) or targeted supplementation. Your GP may check your B vitamin levels alongside this result. If supplementation doesn't bring levels down, further investigation into absorption, genetic factors (such as the MTHFR gene variant), or other causes may be warranted. Staying active, not smoking, and limiting alcohol also help keep homocysteine in check.

---

## Group 2: Diabetes Markers addition

### `insulin` — Insulin (Fasting)
**Type:** Hilo (both high and low are noted)  
**Reference range:** 2.6 – 24.9 mIU/L  
**Unit:** mIU/L  
*(Fasting insulin; some labs report in pmol/L — multiply by 6.9 to convert mIU/L to pmol/L)*

> **Explanation:** Insulin is a hormone produced by the beta cells of the pancreas that acts as the key that unlocks your cells to allow glucose to enter and be used for energy. Fasting insulin (measured after at least 8–12 hours without food) reflects how much insulin your body needs to maintain normal blood sugar when no food is being digested. Persistently high fasting insulin is often a sign of insulin resistance, a state where cells don't respond well to insulin and the pancreas has to work harder to compensate. This is an early precursor to type 2 diabetes and is associated with weight gain, particularly around the abdomen.

> **Advice (High):** Elevated fasting insulin suggests your cells may be resistant to insulin's effects, meaning your pancreas is producing more than usual to keep blood sugar under control. This is strongly associated with excess body weight (especially abdominal fat), a sedentary lifestyle, and a diet high in refined carbohydrates and sugar. The most effective interventions are reducing refined carbohydrates and sugary foods, increasing fibre, exercising regularly (both aerobic and resistance training are helpful), losing excess weight, and improving sleep quality. Even moderate weight loss of 5–10% of body weight can significantly improve insulin sensitivity. Your GP may want to check your HbA1c and fasting glucose alongside this result.

> **Advice (Low):** A low fasting insulin level reflects good insulin sensitivity, meaning your cells respond well to insulin and your pancreas doesn't need to produce large amounts. This is generally a positive finding. Very low insulin, particularly alongside high blood glucose, could indicate type 1 diabetes or advanced pancreatic disease, but this would typically be identified through other results.

---

## Group 3: Iron Status additions

### `iron_binding_capacity` — Total Iron Binding Capacity (TIBC)
**Type:** Hilo  
**Reference range:** 45 – 81 µmol/L  
**Unit:** µmol/L

> **Explanation:** TIBC measures the total capacity of your blood to bind and transport iron using transferrin, the main iron-carrying protein. When iron stores are low, the liver produces more transferrin, raising the TIBC. When iron stores are plentiful, less transferrin is made, lowering TIBC. Think of it as the size of the transport fleet: a bigger fleet (high TIBC) means the body is trying harder to capture what little iron is available. TIBC is most useful when interpreted alongside serum iron and ferritin to build a complete picture of your iron status.

> **Advice (High):** A high TIBC usually indicates that your iron stores are depleted and your body is producing extra transferrin to maximise iron capture. This pattern is typical of iron deficiency. Focus on iron-rich foods, and your GP will likely recommend iron supplements if dietary changes are insufficient.

> **Advice (Low):** Low TIBC can occur when iron stores are high (the body produces less transferrin when it doesn't need more iron), in chronic inflammation, liver disease, or malnutrition. Your GP will interpret this alongside your ferritin and serum iron to determine the underlying cause.

---

### `transferrin_saturation` — Transferrin Saturation
**Type:** Hilo  
**Reference range:** 20 – 50%  
**Unit:** %

> **Explanation:** Transferrin saturation tells you what percentage of your available transferrin (iron transport protein) is actually loaded with iron. A low saturation means plenty of empty transport proteins, suggesting iron is scarce. A high saturation means most of the transport protein is already carrying iron, which can indicate iron overload.

> **Advice (High):** A high transferrin saturation means a large proportion of your iron transport capacity is occupied, suggesting more iron is circulating than usual. When combined with high ferritin, this pattern raises concern for iron overload conditions such as haemochromatosis. Your GP may want to check the full iron panel and consider genetic testing. If you are taking iron supplements, they may recommend stopping them.

> **Advice (Low):** A low transferrin saturation, particularly when accompanied by low ferritin and high TIBC, is a classic sign of iron deficiency. This often precedes the development of anaemia. Increasing dietary iron and potentially taking supplements (under GP guidance) will help replenish stores.

---

## Group 4: Bone Profile addition

### `calcium` — Calcium
**Type:** Hilo  
**Reference range:** 2.20 – 2.60 mmol/L  
**Unit:** mmol/L  
*(Adjusted/corrected calcium based on albumin should be noted if applicable)*

> **Explanation:** Calcium is the most abundant mineral in the body, making up around 99% of your bones and teeth. The remaining 1% circulates in your blood and plays critical roles in muscle contraction, nerve signalling, blood clotting, and heart rhythm. Your body tightly regulates blood calcium levels through a system involving parathyroid hormone (PTH), vitamin D, and the kidneys.

> **Advice (High):** Elevated blood calcium (hypercalcaemia) most commonly results from overactive parathyroid glands (primary hyperparathyroidism) or, less commonly, from certain cancers that release calcium from bones. Other causes include vitamin D toxicity from excess supplementation, sarcoidosis, or prolonged immobility. Mild hypercalcaemia may cause fatigue, constipation, increased thirst, and muscle weakness. Your GP will want to check your parathyroid hormone level and may arrange further investigations. Staying well hydrated is important as calcium can affect kidney function.

> **Advice (Low):** Low calcium (hypocalcaemia) can cause muscle cramps, tingling or numbness in the hands and feet, muscle spasms, and in severe cases, problems with heart rhythm. Common causes include vitamin D deficiency (which impairs calcium absorption), underactive parathyroid glands, low magnesium, or kidney problems. Your GP will likely check your vitamin D and PTH levels alongside this result.

---

## Group 5: Liver Function additions

### `total_protein` — Total Protein
**Type:** Hilo  
**Reference range:** 60 – 80 g/L  
**Unit:** g/L

> **Explanation:** Total protein measures the combined amount of all proteins in your blood plasma, primarily albumin and globulins. Proteins serve countless functions: transporting substances, fighting infections, clotting blood, maintaining fluid balance, and acting as enzymes and hormones. Total protein is a broad indicator of nutritional status and liver and kidney health.

> **Advice (High):** Elevated total protein can occur with dehydration or when the body produces excess immunoglobulins, as happens in some inflammatory conditions, chronic infections, or conditions like multiple myeloma. Your GP may arrange protein electrophoresis if a specific protein abnormality is suspected.

> **Advice (Low):** Low total protein can result from inadequate protein intake, conditions causing protein loss (kidney disease), liver disease, or excessive fluid retention. Make sure your diet includes adequate protein from varied sources.

---

### `globulin` — Globulin
**Type:** Hilo  
**Reference range:** 18 – 36 g/L  
**Unit:** g/L  
*(Calculated as Total Protein − Albumin)*

> **Explanation:** Globulins are a group of proteins in your blood that includes many important immune and transport proteins. The main types are alpha globulins (acute-phase proteins), beta globulins (lipid transport proteins), and gamma globulins (immunoglobulins/antibodies). An abnormally high or low globulin level can point to immune system disorders, chronic infections, liver disease, or inflammatory conditions.

> **Advice (High):** Elevated globulins can indicate chronic inflammation, ongoing infection, autoimmune disease, or conditions affecting immunoglobulin production. Your GP may arrange protein electrophoresis.

> **Advice (Low):** Low globulins can occur with immune deficiency conditions, certain liver diseases, or protein loss. Your GP will assess this alongside other markers.

---

## Group 6: Urine Analysis addition

### `urine_culture` — Urine Culture and Sensitivities
**Type:** Qualitative (presence/absence)  
**Expected result:** No significant growth  
**Unit:** n/a

> **Explanation:** A urine culture is a laboratory test where a urine sample is incubated to see whether bacteria grow, and if so, which species are present. The sensitivity part determines which antibiotics will kill the identified bacteria, guiding treatment choices.

> **Advice (Positive):** A positive urine culture means bacteria were detected, confirming a urinary tract infection. The sensitivity results tell your GP which antibiotic to prescribe. Complete the full course of antibiotics. Drink plenty of water. If you suffer from recurrent UTIs, your GP may investigate contributing factors.

> **Advice (Negative):** A negative culture means no significant bacterial growth was detected, indicating no active urinary tract infection. If you had symptoms, these may have another cause or the infection may have been resolving at the time of sampling.

---

## Group 7: Thyroid Function additions

### `tpo_antibodies` — Thyroid Peroxidase Antibodies (TPOAb)
**Type:** Upper bound (elevated = abnormal)  
**Reference range:** < 35 IU/mL  
**Unit:** IU/mL  
*(Reference ranges vary by assay — Roche Elecsys commonly uses < 34 IU/mL; please confirm against lab used)*

> **Explanation:** Thyroid peroxidase antibodies (TPOAb) are antibodies produced by the immune system that mistakenly target thyroid peroxidase, an enzyme essential for making thyroid hormones. Their presence indicates that the immune system is attacking the thyroid gland, which is the hallmark of autoimmune thyroid conditions, most commonly Hashimoto's thyroiditis and sometimes Graves' disease.

> **Advice (High):** Elevated TPO antibodies confirm autoimmune activity against your thyroid. This doesn't necessarily mean your thyroid function is abnormal right now, but it does mean you're at higher risk of developing thyroid dysfunction in the future. Your GP will monitor your TSH and FT4 over time, often annually.

---

### `thyroglobulin_antibody` — Thyroglobulin Antibody (TgAb)
**Type:** Upper bound (elevated = abnormal)  
**Reference range:** < 115 IU/mL  
**Unit:** IU/mL  
*(Reference range varies considerably by assay — please confirm: some use < 4 kIU/L, others < 60 IU/mL)*

> **Explanation:** Thyroglobulin antibodies (TgAb) target thyroglobulin, a protein made by the thyroid that serves as a precursor to thyroid hormones. Like TPO antibodies, elevated TgAb indicate autoimmune activity. TgAb are also important in monitoring people who have had thyroid cancer treatment, as they can interfere with thyroglobulin tumour marker measurements.

> **Advice (High):** Elevated thyroglobulin antibodies point to autoimmune activity against the thyroid, often seen alongside elevated TPO antibodies in Hashimoto's thyroiditis. If you've been treated for thyroid cancer, the presence of these antibodies is particularly significant.

---

## Group 8: Vitamins additions

### `vitamin_b12` — Vitamin B12 (Total Serum)
**Type:** Hilo  
**Reference range:** 148 – 900 pmol/L  
**Unit:** pmol/L  
*(Note: "ab12" already in system is Active B12 / holotranscobalamin, range 25.1–165 pmol/L. This is a separate test for total serum B12.)*

> **Explanation:** Total serum vitamin B12 measures the overall concentration of cobalamin in your blood, including both the active fraction (bound to transcobalamin II) and the inactive fraction (bound to haptocorrin). B12 is essential for red blood cell production, DNA synthesis, and nervous system function. Your body stores B12 in the liver for several years, so deficiency develops slowly.

> **Advice (High):** High serum B12 is most commonly due to supplementation or B12-rich foods. Significantly elevated levels without supplementation can sometimes be associated with liver conditions, certain blood disorders, or kidney disease.

> **Advice (Low):** Low serum B12 can cause megaloblastic anaemia, neurological symptoms (tingling or numbness), memory problems, and fatigue. Deficiency is more common in vegans, vegetarians, and older adults.

---

### `vitamin_a` — Vitamin A (Retinol)
**Type:** Hilo  
**Reference range:** 1.05 – 3.50 µmol/L  
**Unit:** µmol/L

> **Explanation:** Vitamin A (retinol) is a fat-soluble vitamin essential for vision (particularly night vision), immune function, skin health, and cell growth. Because vitamin A is fat-soluble, it's stored in the liver, which means toxicity from excessive intake is possible.

> **Advice (High):** Elevated serum vitamin A usually results from high supplement intake (preformed retinol). Toxicity can cause headaches, nausea, liver damage, and in pregnant women can be teratogenic. Review any supplements and discuss with your GP.

> **Advice (Low):** Low vitamin A can lead to night blindness, dry eyes, dry skin, and impaired immune function. Increase vitamin A-rich foods (liver, oily fish, eggs, dairy) alongside orange/yellow vegetables for beta-carotene.

---

### `vitamin_b1` — Vitamin B1 (Thiamine)
**Type:** Lower bound (low = concern; high is not clinically significant)  
**Reference range:** 70 – 180 nmol/L (whole blood)  
**Unit:** nmol/L

> **Explanation:** Thiamine (vitamin B1) plays a fundamental role in energy metabolism, helping cells convert carbohydrates into usable energy. It's particularly important for the nervous system. Deficiency can develop within weeks of inadequate intake. Most commonly associated with heavy alcohol consumption, which impairs absorption.

> **Advice (Low):** Low thiamine can cause Wernicke's encephalopathy and Korsakoff syndrome. Earlier deficiency causes fatigue, irritability, muscle weakness, and tingling sensations. If alcohol is involved, stopping drinking is the priority alongside supplementation.

---

### `vitamin_b2` — Vitamin B2 (Riboflavin)
**Type:** Lower bound  
**Reference range:** 106 – 638 nmol/L  
**Unit:** nmol/L  
*(Reference range is for serum riboflavin — please confirm whether lab reports whole blood or serum)*

> **Explanation:** Riboflavin (vitamin B2) acts as a building block for two important coenzymes involved in energy production. It's also needed to activate other B vitamins including B6 and folate. Good sources include dairy products, meat, fish, eggs, and fortified cereals.

> **Advice (Low):** Low riboflavin can cause angular cheilitis (cracks at corners of mouth), a sore/magenta-coloured tongue, skin rashes, and light sensitivity. A B-complex supplement provides balanced B vitamins.

---

### `vitamin_b6` — Vitamin B6 (Pyridoxine)
**Type:** Hilo (both high toxicity and low deficiency are clinically relevant)  
**Reference range:** 20 – 200 nmol/L (plasma PLP)  
**Unit:** nmol/L

> **Explanation:** Vitamin B6 is involved in over 100 enzymatic reactions, including protein and amino acid metabolism, neurotransmitter production (serotonin, dopamine), and haemoglobin synthesis. Unlike most water-soluble vitamins, B6 can cause neurological toxicity at very high supplemental doses.

> **Advice (High):** Chronically elevated B6 is almost always from high-dose supplementation (>50–100 mg/day). This can cause peripheral neuropathy — numbness, tingling, sensory changes in hands and feet. Reduce the dose and discuss with your GP.

> **Advice (Low):** Low B6 can cause anaemia, peripheral neuropathy, skin conditions, and mood disturbances. More common in older adults, heavy drinkers, and those on certain medications (e.g. isoniazid).

---

### `vitamin_c` — Vitamin C
**Type:** Hilo  
**Reference range:** 23 – 85 µmol/L  
**Unit:** µmol/L

> **Explanation:** Vitamin C (ascorbic acid) is a water-soluble antioxidant essential for collagen synthesis, immune function, wound healing, and non-haem iron absorption. Humans cannot synthesise it and must obtain it from the diet daily.

> **Advice (High):** High vitamin C from supplementation is generally harmless; excess is excreted. Very high doses (>1–2g/day) can cause digestive symptoms and may increase oxalate kidney stones in susceptible individuals.

> **Advice (Low):** Mild deficiency causes fatigue, poor wound healing, and frequent infections. Severe deficiency (scurvy) causes bleeding gums, bruising, and joint pain. A daily portion of fresh fruit or vegetables easily meets requirements.

---

### `vitamin_e` — Vitamin E (Alpha-Tocopherol)
**Type:** Hilo  
**Reference range:** 11.6 – 46.4 µmol/L  
**Unit:** µmol/L

> **Explanation:** Vitamin E is a fat-soluble antioxidant protecting cell membranes from oxidative damage. Alpha-tocopherol is the most active form. Good dietary sources include nuts, seeds, vegetable oils, avocados, and leafy greens.

> **Advice (High):** High levels from supplementation (>400 IU/day) may interfere with vitamin K's role in blood clotting. Particularly important to flag if patient is on anticoagulants.

> **Advice (Low):** Low vitamin E can impair antioxidant defences. Clinical deficiency is rare in healthy adults; more common with fat malabsorption conditions (cystic fibrosis, Crohn's, cholestatic liver disease). Symptoms include muscle weakness and neurological problems.

---

### `beta_carotene` — Beta-Carotene
**Type:** Hilo  
**Reference range:** 0.19 – 2.53 µmol/L  
**Unit:** µmol/L

> **Explanation:** Beta-carotene is a plant pigment and precursor to vitamin A. Your body converts it to retinol as needed. It also functions as a direct antioxidant. Serum beta-carotene reflects dietary fruit and vegetable intake and fat absorption capacity.

> **Advice (High):** Very high dietary beta-carotene causes carotenaemia — harmless yellowing of the skin. However, high-dose beta-carotene supplements are associated with increased lung cancer risk in smokers and should be avoided in that group.

> **Advice (Low):** Low beta-carotene reflects a diet low in fruits and vegetables, fat malabsorption, or heavy smoking. Increase colourful produce: carrots, sweet potatoes, butternut squash, spinach, kale.

---

## Group 9: Hormones (new group)

### `fsh` — Follicle Stimulating Hormone (FSH)
**Type:** Hilo  
**Reference range:** Female: 1.5 – 21.5 IU/L (non-postmenopausal) | Male: 1.5 – 12.4 IU/L  
**Unit:** IU/L  
*⚠️ Highly cycle-dependent in women — interpretation requires knowledge of cycle phase. Postmenopausal women will have FSH well above 25.8 IU/L (25.8–134.8 IU/L); the upper female bound used here covers premenopausal range only. Please advise whether a postmenopausal-specific range should be incorporated.*

> **Explanation:** FSH is produced by the pituitary gland and plays a central role in reproductive function. In women, it stimulates ovarian follicle growth and oestrogen production. In men, it stimulates sperm production. Levels fluctuate throughout the menstrual cycle.

> **Advice (High — premenopausal women):** May indicate reduced ovarian reserve or early transition towards menopause. Very high FSH with irregular/absent periods may indicate premature ovarian insufficiency.

> **Advice (High — men):** May point to impaired sperm production or testicular problems.

> **Advice (Low):** May indicate pituitary dysfunction, often associated with excessive exercise, significant underweight, high stress, or pituitary conditions.

---

### `lh` — Luteinising Hormone (LH)
**Type:** Hilo  
**Reference range:** Female: 1.0 – 12.6 IU/L (follicular/luteal; excludes mid-cycle surge) | Male: 1.7 – 8.6 IU/L  
**Unit:** IU/L  
*⚠️ Mid-cycle surge in women reaches 14–95.6 IU/L — a result in this range during the expected ovulation window is normal. Please advise on whether to incorporate cycle-phase logic.*

> **Explanation:** LH triggers ovulation in women and testosterone production in men. LH levels surge dramatically at mid-cycle in women.

> **Advice (High):** In women (outside mid-cycle), high LH with high LH:FSH ratio is associated with PCOS. High LH in postmenopausal women is normal. In men, elevated LH alongside low testosterone suggests primary hypogonadism.

> **Advice (Low):** May reflect hypothalamic-pituitary dysfunction from excessive exercise, low body weight, chronic stress.

---

### `testosterone` — Testosterone (Total)
**Type:** Hilo  
**Reference range:** Female: 0.3 – 2.8 nmol/L | Male: 9.0 – 29.0 nmol/L  
**Unit:** nmol/L  
*⚠️ Diurnal variation is significant — levels are highest in the morning. Testing time should ideally be standardised.*

> **Explanation:** Testosterone is the primary male sex hormone, present and important in both sexes. In men: libido, muscle/bone mass, mood, energy. In women: produced in smaller amounts, contributes to libido, energy, bone density.

> **Advice (High — women):** Associated with PCOS, adrenal conditions, or exogenous androgens. Symptoms include acne, hirsutism, irregular periods.

> **Advice (High — men):** May result from anabolic steroid use or, rarely, certain tumours.

> **Advice (Low — men):** Fatigue, reduced libido, erectile dysfunction, low mood, reduced muscle mass. Lifestyle changes (sleep, exercise, weight loss) help; GP may consider testosterone replacement.

> **Advice (Low — women):** May contribute to low energy, reduced libido, and mood changes.

---

### `free_testosterone` — Free Testosterone
**Type:** Hilo  
**Reference range:** Female: 1 – 12 pmol/L | Male: 150 – 500 pmol/L  
**Unit:** pmol/L  
*⚠️ Reference ranges for free testosterone are method-dependent and laboratory-specific. Equilibrium dialysis values used here. Please confirm against the assay used.*

> **Explanation:** Free testosterone is the biologically active unbound fraction (1–3% of total testosterone). It's most useful when SHBG levels are abnormal, which can make total testosterone misleading.

---

### `oestradiol` — Oestradiol (E2)
**Type:** Hilo  
**Reference range:** Female: 77 – 921 pmol/L (follicular phase reference) | Male: 28 – 156 pmol/L  
**Unit:** pmol/L  
*⚠️ Female range is extremely cycle-dependent. Follicular: 77–921, mid-cycle peak: 174–1161, luteal: 122–1094, postmenopausal: <130. The range used (77–921) covers the follicular phase as a clinical baseline. Please advise on how to handle this.*

> **Explanation:** Oestradiol is the most potent form of oestrogen, produced primarily by the ovaries in women. Levels fluctuate considerably across the menstrual cycle.

---

### `progesterone` — Progesterone
**Type:** Hilo  
**Reference range:** Female: 0.18 – 75.9 nmol/L (wide range spanning cycle phases) | Male: 0.15 – 1.40 nmol/L  
**Unit:** nmol/L  
*⚠️ The female range is intentionally broad to cover all cycle phases. Clinically, the most important reference is the mid-luteal (day 21) level, where > 16 nmol/L confirms ovulation. Please advise whether a narrower context-specific range would be preferable.*

> **Explanation:** Progesterone is produced mainly by the corpus luteum after ovulation and by the placenta during pregnancy. A day-21 progesterone test is used to confirm ovulation has occurred.

---

### `prolactin` — Prolactin
**Type:** Hilo  
**Reference range:** Female: 102 – 496 mIU/L | Male: 86 – 324 mIU/L  
**Unit:** mIU/L  
*(Non-pregnant, non-lactating females. Pregnancy/breastfeeding causes physiological elevation.)*

> **Explanation:** Prolactin is produced by the pituitary gland, best known for stimulating milk production after childbirth. A single mildly elevated result can be caused by stress, strenuous exercise, sexual activity, or recent eating.

> **Advice (High):** If persistently elevated on repeat fasting testing, investigate. Causes include prolactinoma (benign pituitary adenoma), certain medications (antipsychotics, antidepressants, metoclopramide), hypothyroidism, kidney or liver disease. In women: irregular/absent periods, infertility, galactorrhoea. In men: reduced libido, erectile dysfunction, gynaecomastia.

---

### `shbg` — Sex Hormone Binding Globulin (SHBG)
**Type:** Hilo  
**Reference range:** Female: 18 – 144 nmol/L | Male: 13 – 71 nmol/L  
**Unit:** nmol/L

> **Explanation:** SHBG binds tightly to sex hormones, making them inactive. Higher SHBG means less free (active) hormone; lower SHBG means more. Rises with oestrogen, ageing, hyperthyroidism, and liver disease; falls with obesity, insulin resistance, hypothyroidism, and androgenic steroids.

> **Advice (High):** May indicate functional hormone deficiency despite normal total levels. Causes include hyperthyroidism, liver conditions, anorexia, or high oestrogen states.

> **Advice (Low):** In women, associated with insulin resistance, obesity, PCOS — marker of metabolic risk. In men, associated with insulin resistance and cardiovascular risk.

---

### `free_androgen_index` — Free Androgen Index (FAI)
**Type:** Hilo  
**Reference range:** Female: 0.5 – 5.0% | Male: 30 – 80%  
**Unit:** % (dimensionless × 100)  
**Formula:** (Total Testosterone ÷ SHBG) × 100  
*⚠️ FAI is primarily validated and used clinically in women (especially PCOS investigation). The male reference range is not universally standardised. Please advise whether to include a male range or restrict to female use.*

> **Explanation:** FAI estimates biologically active (free) testosterone. In women, it's a clinically useful marker for assessing androgen status, particularly in PCOS investigation.

> **Advice (High — women):** Excess free androgen activity, hallmark finding in PCOS. Associated with irregular periods, acne, hirsutism, fertility difficulties.

> **Advice (Low):** Suggests low androgen bioavailability, contributing to fatigue, low libido, mood changes.

---

## Group 10: Minerals (new group)

### `magnesium` — Magnesium
**Type:** Hilo  
**Reference range:** 0.70 – 1.00 mmol/L  
**Unit:** mmol/L

> **Explanation:** Magnesium is involved in over 300 enzymatic reactions. About 60% is stored in bones; only ~1% circulates in blood, meaning serum levels don't always reflect total body stores. Good sources: nuts, seeds, dark chocolate, leafy greens, legumes, whole grains.

> **Advice (High):** Uncommon with normal kidney function. Most often from high-dose magnesium antacids/laxatives in patients with kidney disease. Higher levels can cause muscle weakness, slowed breathing, heart rhythm problems.

> **Advice (Low):** Can cause muscle cramps, twitching, fatigue, insomnia, anxiety, irregular heart rhythm, and headaches. More common with heavy alcohol use, proton pump inhibitors, or certain diuretics. Magnesium glycinate or citrate supplements are well absorbed.

---

### `copper` — Copper
**Type:** Hilo  
**Reference range:** Female: 12.6 – 24.4 µmol/L | Male: 11.0 – 22.0 µmol/L  
**Unit:** µmol/L  
*(Women typically have higher copper levels due to oestrogen)*

> **Explanation:** Copper is an essential trace mineral involved in red blood cell production, collagen formation, iron metabolism, and antioxidant enzyme function. Copper balance is closely linked to zinc intake — high zinc supplementation can deplete copper.

> **Advice (High):** Can occur with liver disease, oestrogen therapy, pregnancy, chronic inflammation, or Wilson's disease (genetic condition). Reducing high-dose zinc supplementation and limiting copper-rich foods may be advised.

> **Advice (Low):** Can cause anaemia (copper needed for iron absorption), fatigue, poor immune function, and neurological symptoms. Often due to excessive zinc supplementation or malabsorption conditions.

---

### `red_cell_magnesium` — Red Cell Magnesium
**Type:** Hilo  
**Reference range:** 1.65 – 2.65 mmol/L  
**Unit:** mmol/L  
*⚠️ Reference ranges vary considerably between laboratories for this test. Please confirm the range appropriate for the assay used.*

> **Explanation:** Red cell magnesium measures intracellular magnesium (inside red blood cells), which is considered a more sensitive marker of total body magnesium status than serum magnesium alone. Normal serum magnesium can coexist with depleted intracellular stores.

> **Advice (Low):** Low red cell magnesium indicates functional magnesium deficiency even if serum is normal. Associated with muscle cramps, fatigue, poor sleep, irritability, and heart palpitations. Increase magnesium-rich foods and consider a well-absorbed supplement (glycinate or citrate).

---

## Group 11: Digestive Enzymes (new group)

### `amylase` — Amylase
**Type:** Hilo  
**Reference range:** 30 – 110 U/L  
**Unit:** U/L  
*(Some labs reference: 25–125 U/L — please confirm against lab used)*

> **Explanation:** Amylase is produced primarily by the pancreas and salivary glands to break down starches. When the pancreas becomes inflamed, amylase leaks into the blood in larger quantities. Amylase rises and falls more quickly than lipase (returns to normal within 2–3 days), so lipase is preferred if there's been a delay between event and testing.

> **Advice (High):** Significantly elevated amylase most commonly indicates acute pancreatitis or blocked pancreatic duct. Also consider: salivary gland inflammation, bowel obstruction, kidney problems. Severe upper abdominal pain radiating to the back warrants prompt medical attention.

> **Advice (Low):** Can occur in chronic pancreatitis with loss of pancreatic tissue. May indicate exocrine pancreatic insufficiency if combined with fatty stools, bloating, or weight loss.

---

### `lipase` — Lipase
**Type:** Hilo  
**Reference range:** 13 – 60 U/L  
**Unit:** U/L  
*(Reference ranges vary by lab: some use 0–160 U/L, others 8–78 U/L — please confirm)*

> **Explanation:** Lipase is produced almost exclusively by the pancreas to break down fats during digestion. More specific for pancreatic injury than amylase. Importantly, lipase remains elevated for up to 2 weeks after an acute episode (vs 2–3 days for amylase).

> **Advice (High):** Very high lipase (>3× upper limit) is highly specific for acute pancreatitis. Other causes include pancreatic duct obstruction and chronic pancreatitis. Low-fat diet and alcohol avoidance are important during recovery.

> **Advice (Low):** Can occur in advanced chronic pancreatitis with reduced enzyme capacity. May be associated with fat malabsorption (fatty stools, weight loss). Consider pancreatic enzyme replacement.

---

## Group 12: Inflammatory Markers (new group)

### `esr` — Erythrocyte Sedimentation Rate (ESR)
**Type:** Upper bound (elevated = abnormal)  
**Reference range:** Female ≤ 20 mm/hr | Male ≤ 15 mm/hr  
**Unit:** mm/hr  
*(Westergren method; some labs apply age-adjusted formulae: Male: age ÷ 2; Female: (age + 10) ÷ 2)*

> **Explanation:** ESR measures how quickly red blood cells settle in a test tube over one hour. Inflammation causes proteins (fibrinogen, immunoglobulins) to make red cells clump and settle faster. ESR is a non-specific marker: elevated by infections, autoimmune diseases, malignancy, anaemia, and ageing. It rises and falls more slowly than CRP, making it useful for tracking chronic inflammation over time.

> **Advice (High):** An elevated ESR indicates inflammation somewhere but does not identify the source. In context, it can support diagnoses such as rheumatoid arthritis, other autoimmune conditions, infections, temporal arteritis (critical in older adults with headaches), or malignancy. A mildly elevated ESR with no symptoms often has a benign explanation. Very high ESR (>100 mm/hr) is more concerning and usually warrants further investigation.

---

## Summary table

| Key | Display Name | Range (F/M or unified) | Unit | Type |
|-----|-------------|------------------------|------|------|
| `apo_b_a1_ratio` | APO B/A1 Ratio | ≤0.8 / ≤0.9 | ratio | upper_bound |
| `non_hdl_cholesterol` | Non-HDL Cholesterol | ≤3.36 | mmol/L | upper_bound |
| `vldl` | VLDL Cholesterol | ≤1.65 | mmol/L | upper_bound |
| `homocysteine` | Homocysteine | ≤10 | µmol/L | upper_bound |
| `insulin` | Insulin (Fasting) | 2.6–24.9 | mIU/L | hilo |
| `iron_binding_capacity` | TIBC | 45–81 | µmol/L | hilo |
| `transferrin_saturation` | Transferrin Saturation | 20–50 | % | hilo |
| `calcium` | Calcium | 2.20–2.60 | mmol/L | hilo |
| `total_protein` | Total Protein | 60–80 | g/L | hilo |
| `globulin` | Globulin | 18–36 | g/L | hilo |
| `urine_culture` | Urine Culture & Sensitivities | n/a (qualitative) | — | presence |
| `tpo_antibodies` | TPO Antibodies | <35 | IU/mL | upper_bound |
| `thyroglobulin_antibody` | Thyroglobulin Antibody | <115 | IU/mL | upper_bound |
| `vitamin_b12` | Vitamin B12 (Total Serum) | 148–900 | pmol/L | hilo |
| `vitamin_a` | Vitamin A (Retinol) | 1.05–3.50 | µmol/L | hilo |
| `vitamin_b1` | Vitamin B1 (Thiamine) | 70–180 | nmol/L | lower_bound |
| `vitamin_b2` | Vitamin B2 (Riboflavin) | 106–638 | nmol/L | lower_bound |
| `vitamin_b6` | Vitamin B6 (Pyridoxine) | 20–200 | nmol/L | hilo |
| `vitamin_c` | Vitamin C | 23–85 | µmol/L | hilo |
| `vitamin_e` | Vitamin E (α-Tocopherol) | 11.6–46.4 | µmol/L | hilo |
| `beta_carotene` | Beta-Carotene | 0.19–2.53 | µmol/L | hilo |
| `fsh` | FSH | F: 1.5–21.5 / M: 1.5–12.4 | IU/L | hilo |
| `lh` | LH | F: 1.0–12.6 / M: 1.7–8.6 | IU/L | hilo |
| `testosterone` | Testosterone (Total) | F: 0.3–2.8 / M: 9.0–29.0 | nmol/L | hilo |
| `free_testosterone` | Free Testosterone | F: 1–12 / M: 150–500 | pmol/L | hilo |
| `oestradiol` | Oestradiol (E2) | F: 77–921 / M: 28–156 | pmol/L | hilo |
| `progesterone` | Progesterone | F: 0.18–75.9 / M: 0.15–1.40 | nmol/L | hilo |
| `prolactin` | Prolactin | F: 102–496 / M: 86–324 | mIU/L | hilo |
| `shbg` | SHBG | F: 18–144 / M: 13–71 | nmol/L | hilo |
| `free_androgen_index` | Free Androgen Index | F: 0.5–5.0 / M: 30–80 | % | hilo |
| `magnesium` | Magnesium | 0.70–1.00 | mmol/L | hilo |
| `copper` | Copper | F: 12.6–24.4 / M: 11.0–22.0 | µmol/L | hilo |
| `red_cell_magnesium` | Red Cell Magnesium | 1.65–2.65 | mmol/L | hilo |
| `amylase` | Amylase | 30–110 | U/L | hilo |
| `lipase` | Lipase | 13–60 | U/L | hilo |
| `esr` | ESR | F: ≤20 / M: ≤15 | mm/hr | upper_bound |

---

## Flagged items requiring clinical confirmation

1. **FSH / LH / Oestradiol / Progesterone** — The reference ranges are cycle-phase-dependent. We've used broad ranges; please advise whether context-specific ranges (follicular/luteal/postmenopausal) should be displayed or flagged differently.
2. **Thyroglobulin Antibody (TgAb)** — The reference range (< 115 IU/mL) varies significantly by assay. Please confirm against the specific lab/assay used.
3. **TPO Antibodies** — The reference range (< 35 IU/mL) varies by assay (some use < 34, < 60). Please confirm.
4. **Vitamin B2 (Riboflavin)** — Please confirm whether the lab reports serum or whole blood, as the reference range differs.
5. **Free Testosterone** — Reference range is method-dependent (equilibrium dialysis used here). Please confirm.
6. **Red Cell Magnesium** — Reference ranges vary considerably between laboratories. Please confirm.
7. **Free Androgen Index (FAI)** — The male reference range is not universally standardised. Please advise whether to restrict FAI to female patients or retain the male range.
8. **ESR** — Some labs apply age-adjusted formulae rather than fixed thresholds. Please advise on preferred approach.
9. **Lipase / Amylase** — Upper limits vary by laboratory. Please confirm against the lab used.
10. **Insulin** — Please confirm preferred units (mIU/L vs pmol/L) and reference range for your lab.
