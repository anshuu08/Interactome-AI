"""
Interactome-AI Knowledge Base Generator
========================================
Generates a comprehensive drug interaction knowledge base with 200+ drugs
and 500+ interactions based on pharmacological rules.

Run: python generate_kb.py
Output: app/data/drug_interactions.json
"""
import json
import os
from itertools import combinations

# =============================================================================
# PART 1: COMPREHENSIVE DRUG DATABASE (200+ drugs)
# =============================================================================
# Each drug has: cid, name, smiles, formula, molecular_weight, class, subclass,
# cyp_enzymes (metabolized by), cyp_inhibits, cyp_induces, description,
# and pharmacodynamic tags for interaction detection.

DRUGS = {
    # ─── CARDIOVASCULAR: Statins ─────────────────────────────────────────
    "atorvastatin": {
        "cid": 60823, "name": "Atorvastatin", "formula": "C33H35FN2O5", "molecular_weight": 558.64,
        "class": "Statin", "subclass": "HMG-CoA Reductase Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["statin", "hepatotoxic"],
        "description": "HMG-CoA reductase inhibitor for cholesterol reduction."
    },
    "simvastatin": {
        "cid": 54454, "name": "Simvastatin", "formula": "C25H38O5", "molecular_weight": 418.57,
        "class": "Statin", "subclass": "HMG-CoA Reductase Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["statin", "hepatotoxic"],
        "description": "Statin with high CYP3A4 dependence. Higher rhabdomyolysis risk with CYP3A4 inhibitors."
    },
    "rosuvastatin": {
        "cid": 446157, "name": "Rosuvastatin", "formula": "C22H28FN3O6S", "molecular_weight": 481.54,
        "class": "Statin", "subclass": "HMG-CoA Reductase Inhibitor",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["statin", "hepatotoxic"],
        "description": "Potent statin with minimal CYP3A4 metabolism. Safer with azole antifungals."
    },
    "lovastatin": {
        "cid": 53232, "name": "Lovastatin", "formula": "C24H36O5", "molecular_weight": 404.54,
        "class": "Statin", "subclass": "HMG-CoA Reductase Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["statin", "hepatotoxic"],
        "description": "First commercially available statin. Extensively metabolized by CYP3A4."
    },
    "pravastatin": {
        "cid": 54687, "name": "Pravastatin", "formula": "C23H36O7", "molecular_weight": 424.53,
        "class": "Statin", "subclass": "HMG-CoA Reductase Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["statin"],
        "description": "Hydrophilic statin not metabolized by CYP enzymes. Fewest drug interactions among statins."
    },
    "fluvastatin": {
        "cid": 446155, "name": "Fluvastatin", "formula": "C24H26FNO4", "molecular_weight": 411.47,
        "class": "Statin", "subclass": "HMG-CoA Reductase Inhibitor",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["statin", "hepatotoxic"],
        "description": "Statin metabolized by CYP2C9. Interaction potential with warfarin."
    },
    "pitavastatin": {
        "cid": 5282452, "name": "Pitavastatin", "formula": "C25H24FNO4", "molecular_weight": 421.46,
        "class": "Statin", "subclass": "HMG-CoA Reductase Inhibitor",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["statin"],
        "description": "Minimal CYP metabolism. Low interaction potential."
    },

    # ─── CARDIOVASCULAR: ACE Inhibitors ──────────────────────────────────
    "lisinopril": {
        "cid": 5362119, "name": "Lisinopril", "formula": "C21H31N3O5", "molecular_weight": 405.49,
        "class": "ACE Inhibitor", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ace_inhibitor", "raas", "hyperkalemia_risk"],
        "description": "ACE inhibitor for hypertension and heart failure."
    },
    "enalapril": {
        "cid": 5388962, "name": "Enalapril", "formula": "C20H28N2O5", "molecular_weight": 376.45,
        "class": "ACE Inhibitor", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ace_inhibitor", "raas", "hyperkalemia_risk"],
        "description": "Prodrug ACE inhibitor converted to enalaprilat in the liver."
    },
    "ramipril": {
        "cid": 5362129, "name": "Ramipril", "formula": "C23H32N2O5", "molecular_weight": 416.51,
        "class": "ACE Inhibitor", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ace_inhibitor", "raas", "hyperkalemia_risk"],
        "description": "ACE inhibitor with cardiovascular protective benefits."
    },
    "benazepril": {
        "cid": 5362124, "name": "Benazepril", "formula": "C24H28N2O5", "molecular_weight": 424.49,
        "class": "ACE Inhibitor", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ace_inhibitor", "raas", "hyperkalemia_risk"],
        "description": "ACE inhibitor for hypertension."
    },
    "captopril": {
        "cid": 44093, "name": "Captopril", "formula": "C9H15NO3S", "molecular_weight": 217.29,
        "class": "ACE Inhibitor", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ace_inhibitor", "raas", "hyperkalemia_risk"],
        "description": "First oral ACE inhibitor. Short-acting, taken 2-3 times daily."
    },

    # ─── CARDIOVASCULAR: ARBs ────────────────────────────────────────────
    "losartan": {
        "cid": 3961, "name": "Losartan", "formula": "C22H23ClN6O", "molecular_weight": 422.91,
        "class": "ARB", "subclass": "Antihypertensive",
        "cyp_enzymes": ["CYP2C9", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["arb", "raas", "hyperkalemia_risk"],
        "description": "ARB for hypertension and diabetic nephropathy."
    },
    "valsartan": {
        "cid": 60846, "name": "Valsartan", "formula": "C24H29N5O3", "molecular_weight": 435.52,
        "class": "ARB", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["arb", "raas", "hyperkalemia_risk"],
        "description": "ARB with minimal CYP metabolism."
    },
    "irbesartan": {
        "cid": 3749, "name": "Irbesartan", "formula": "C25H28N6O", "molecular_weight": 428.53,
        "class": "ARB", "subclass": "Antihypertensive",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["arb", "raas", "hyperkalemia_risk"],
        "description": "ARB metabolized by CYP2C9."
    },
    "olmesartan": {
        "cid": 130881, "name": "Olmesartan", "formula": "C24H26N6O3", "molecular_weight": 446.52,
        "class": "ARB", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["arb", "raas", "hyperkalemia_risk"],
        "description": "ARB not metabolized by CYP enzymes."
    },
    "telmisartan": {
        "cid": 65999, "name": "Telmisartan", "formula": "C33H30N4O2", "molecular_weight": 514.62,
        "class": "ARB", "subclass": "Antihypertensive",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["arb", "raas", "hyperkalemia_risk"],
        "description": "Long-acting ARB with PPAR-gamma activity."
    },
    "candesartan": {
        "cid": 2541, "name": "Candesartan", "formula": "C24H20N6O3", "molecular_weight": 440.45,
        "class": "ARB", "subclass": "Antihypertensive",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["arb", "raas", "hyperkalemia_risk"],
        "description": "ARB prodrug for hypertension and heart failure."
    },

    # ─── CARDIOVASCULAR: Beta Blockers ───────────────────────────────────
    "metoprolol": {
        "cid": 4171, "name": "Metoprolol", "formula": "C15H25NO3", "molecular_weight": 267.36,
        "class": "Beta Blocker", "subclass": "Selective β1",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["beta_blocker", "bradycardia_risk", "hypotension_risk"],
        "description": "Selective beta-1 blocker for hypertension and heart failure."
    },
    "atenolol": {
        "cid": 2249, "name": "Atenolol", "formula": "C14H22N2O3", "molecular_weight": 266.34,
        "class": "Beta Blocker", "subclass": "Selective β1",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["beta_blocker", "bradycardia_risk", "hypotension_risk"],
        "description": "Hydrophilic beta-blocker eliminated renally. Fewer CNS side effects."
    },
    "propranolol": {
        "cid": 4946, "name": "Propranolol", "formula": "C16H21NO2", "molecular_weight": 259.34,
        "class": "Beta Blocker", "subclass": "Non-selective",
        "cyp_enzymes": ["CYP2D6", "CYP1A2", "CYP2C19"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["beta_blocker", "bradycardia_risk", "hypotension_risk", "cns_depressant"],
        "description": "Non-selective beta-blocker. Lipophilic with CNS effects."
    },
    "carvedilol": {
        "cid": 2585, "name": "Carvedilol", "formula": "C24H26N2O4", "molecular_weight": 406.47,
        "class": "Beta Blocker", "subclass": "Non-selective + Alpha",
        "cyp_enzymes": ["CYP2D6", "CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["beta_blocker", "bradycardia_risk", "hypotension_risk"],
        "description": "Combined alpha/beta blocker for heart failure. CYP2D6 substrate."
    },
    "bisoprolol": {
        "cid": 2405, "name": "Bisoprolol", "formula": "C18H31NO4", "molecular_weight": 325.44,
        "class": "Beta Blocker", "subclass": "Selective β1",
        "cyp_enzymes": ["CYP3A4", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["beta_blocker", "bradycardia_risk", "hypotension_risk"],
        "description": "Highly selective beta-1 blocker for heart failure."
    },
    "nebivolol": {
        "cid": 71301, "name": "Nebivolol", "formula": "C22H25F2NO4", "molecular_weight": 405.44,
        "class": "Beta Blocker", "subclass": "Selective β1",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["beta_blocker", "bradycardia_risk", "hypotension_risk"],
        "description": "Beta-blocker with nitric oxide-mediated vasodilation."
    },

    # ─── CARDIOVASCULAR: Calcium Channel Blockers ────────────────────────
    "amlodipine": {
        "cid": 2162, "name": "Amlodipine", "formula": "C20H25ClN2O5", "molecular_weight": 408.88,
        "class": "Calcium Channel Blocker", "subclass": "Dihydropyridine",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["ccb", "hypotension_risk"],
        "description": "Long-acting CCB for hypertension and angina."
    },
    "nifedipine": {
        "cid": 4485, "name": "Nifedipine", "formula": "C17H18N2O6", "molecular_weight": 346.34,
        "class": "Calcium Channel Blocker", "subclass": "Dihydropyridine",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ccb", "hypotension_risk"],
        "description": "Short-acting CCB for angina and hypertension."
    },
    "diltiazem": {
        "cid": 39186, "name": "Diltiazem", "formula": "C22H26N2O4S", "molecular_weight": 414.52,
        "class": "Calcium Channel Blocker", "subclass": "Benzothiazepine",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["ccb", "bradycardia_risk", "hypotension_risk"],
        "description": "Non-dihydropyridine CCB. Moderate CYP3A4 inhibitor. Affects heart rate."
    },
    "verapamil": {
        "cid": 2520, "name": "Verapamil", "formula": "C27H38N2O4", "molecular_weight": 454.60,
        "class": "Calcium Channel Blocker", "subclass": "Phenylalkylamine",
        "cyp_enzymes": ["CYP3A4", "CYP1A2"], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["ccb", "bradycardia_risk", "hypotension_risk"],
        "description": "Non-dihydropyridine CCB. Strong CYP3A4 inhibitor. Contraindicated with beta-blockers IV."
    },
    "felodipine": {
        "cid": 3333, "name": "Felodipine", "formula": "C18H19Cl2NO4", "molecular_weight": 384.25,
        "class": "Calcium Channel Blocker", "subclass": "Dihydropyridine",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ccb", "hypotension_risk"],
        "description": "Dihydropyridine CCB for hypertension."
    },

    # ─── CARDIOVASCULAR: Anticoagulants ──────────────────────────────────
    "warfarin": {
        "cid": 54678486, "name": "Warfarin", "formula": "C19H16O4", "molecular_weight": 308.33,
        "class": "Anticoagulant", "subclass": "Vitamin K Antagonist",
        "cyp_enzymes": ["CYP2C9", "CYP3A4", "CYP1A2"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["anticoagulant", "bleeding_risk", "narrow_ti"],
        "description": "Vitamin K antagonist anticoagulant. Narrow therapeutic index."
    },
    "apixaban": {
        "cid": 10182969, "name": "Apixaban", "formula": "C25H25N5O4", "molecular_weight": 459.50,
        "class": "Anticoagulant", "subclass": "Direct Factor Xa Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["anticoagulant", "bleeding_risk", "doac"],
        "description": "Direct oral anticoagulant (DOAC). Partially metabolized by CYP3A4."
    },
    "rivaroxaban": {
        "cid": 6433119, "name": "Rivaroxaban", "formula": "C19H18ClN3O5S", "molecular_weight": 435.88,
        "class": "Anticoagulant", "subclass": "Direct Factor Xa Inhibitor",
        "cyp_enzymes": ["CYP3A4", "CYP2J2"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["anticoagulant", "bleeding_risk", "doac"],
        "description": "DOAC metabolized by CYP3A4. Take with food for absorption."
    },
    "dabigatran": {
        "cid": 216210, "name": "Dabigatran", "formula": "C25H25N7O3", "molecular_weight": 471.51,
        "class": "Anticoagulant", "subclass": "Direct Thrombin Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["anticoagulant", "bleeding_risk", "doac"],
        "description": "DOAC not metabolized by CYP. Renally eliminated. Reversible with idarucizumab."
    },
    "edoxaban": {
        "cid": 10280735, "name": "Edoxaban", "formula": "C24H30ClN7O4S", "molecular_weight": 548.06,
        "class": "Anticoagulant", "subclass": "Direct Factor Xa Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["anticoagulant", "bleeding_risk", "doac"],
        "description": "Factor Xa inhibitor DOAC. Minimal CYP3A4 metabolism."
    },
    "heparin": {
        "cid": 772, "name": "Heparin", "formula": "C12H19NO20S3", "molecular_weight": 593.43,
        "class": "Anticoagulant", "subclass": "Indirect Thrombin Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["anticoagulant", "bleeding_risk"],
        "description": "Parenteral anticoagulant. Not orally bioavailable."
    },
    "enoxaparin": {
        "cid": 772, "name": "Enoxaparin", "formula": "Low Molecular Weight Heparin", "molecular_weight": 4500.0,
        "class": "Anticoagulant", "subclass": "LMWH",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["anticoagulant", "bleeding_risk"],
        "description": "Low molecular weight heparin for DVT/PE prevention and treatment."
    },

    # ─── CARDIOVASCULAR: Antiplatelets ───────────────────────────────────
    "aspirin": {
        "cid": 2244, "name": "Aspirin", "formula": "C9H8O4", "molecular_weight": 180.16,
        "class": "NSAID / Antiplatelet", "subclass": "COX Inhibitor",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["antiplatelet", "nsaid", "bleeding_risk", "gi_toxicity"],
        "description": "Antiplatelet and NSAID. Irreversible COX-1 inhibition."
    },
    "clopidogrel": {
        "cid": 60606, "name": "Clopidogrel", "formula": "C16H16ClNO2S", "molecular_weight": 321.82,
        "class": "Antiplatelet", "subclass": "P2Y12 Inhibitor",
        "cyp_enzymes": ["CYP2C19", "CYP3A4", "CYP2B6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["antiplatelet", "bleeding_risk", "prodrug"],
        "description": "Antiplatelet prodrug requiring CYP2C19 activation."
    },
    "prasugrel": {
        "cid": 11953817, "name": "Prasugrel", "formula": "C20H20FNO3S", "molecular_weight": 373.44,
        "class": "Antiplatelet", "subclass": "P2Y12 Inhibitor",
        "cyp_enzymes": ["CYP3A4", "CYP2B6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["antiplatelet", "bleeding_risk"],
        "description": "More potent P2Y12 inhibitor than clopidogrel. Less CYP2C19 dependent."
    },
    "ticagrelor": {
        "cid": 10188535, "name": "Ticagrelor", "formula": "C23H28F2N6O4S", "molecular_weight": 522.57,
        "class": "Antiplatelet", "subclass": "P2Y12 Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["antiplatelet", "bleeding_risk"],
        "description": "Reversible P2Y12 inhibitor. CYP3A4 substrate — avoid strong inhibitors/inducers."
    },

    # ─── CARDIOVASCULAR: Diuretics ───────────────────────────────────────
    "hydrochlorothiazide": {
        "cid": 3639, "name": "Hydrochlorothiazide", "formula": "C7H8ClN3O4S2", "molecular_weight": 297.74,
        "class": "Diuretic", "subclass": "Thiazide",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["diuretic", "hypokalemia_risk", "hyperglycemia_risk"],
        "description": "Thiazide diuretic for hypertension. Causes potassium and magnesium loss."
    },
    "furosemide": {
        "cid": 3440, "name": "Furosemide", "formula": "C12H11ClN2O5S", "molecular_weight": 330.74,
        "class": "Diuretic", "subclass": "Loop",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["diuretic", "hypokalemia_risk", "ototoxic"],
        "description": "Potent loop diuretic. Causes significant electrolyte loss."
    },
    "spironolactone": {
        "cid": 5833, "name": "Spironolactone", "formula": "C24H32O4S", "molecular_weight": 416.57,
        "class": "Diuretic", "subclass": "Potassium-sparing",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["diuretic", "hyperkalemia_risk", "raas"],
        "description": "Aldosterone antagonist. Potassium-sparing — dangerous with ACE inhibitors."
    },
    "chlorthalidone": {
        "cid": 2732, "name": "Chlorthalidone", "formula": "C14H11ClN2O4S", "molecular_weight": 338.77,
        "class": "Diuretic", "subclass": "Thiazide-like",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["diuretic", "hypokalemia_risk", "hyperglycemia_risk"],
        "description": "Long-acting thiazide-like diuretic."
    },
    "eplerenone": {
        "cid": 443872, "name": "Eplerenone", "formula": "C24H30O6", "molecular_weight": 414.49,
        "class": "Diuretic", "subclass": "Potassium-sparing",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["diuretic", "hyperkalemia_risk", "raas"],
        "description": "Selective aldosterone blocker. CYP3A4 substrate."
    },
    "triamterene": {
        "cid": 5546, "name": "Triamterene", "formula": "C12H11N7", "molecular_weight": 253.26,
        "class": "Diuretic", "subclass": "Potassium-sparing",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["diuretic", "hyperkalemia_risk"],
        "description": "Potassium-sparing diuretic. Risk of hyperkalemia with RAAS agents."
    },

    # ─── CARDIOVASCULAR: Antiarrhythmics ─────────────────────────────────
    "amiodarone": {
        "cid": 2157, "name": "Amiodarone", "formula": "C25H29I2NO3", "molecular_weight": 645.31,
        "class": "Antiarrhythmic", "subclass": "Class III",
        "cyp_enzymes": ["CYP3A4", "CYP2C8"], "cyp_inhibits": ["CYP3A4", "CYP2C9", "CYP2D6"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "bradycardia_risk", "hepatotoxic", "thyroid_toxic"],
        "description": "Potent antiarrhythmic with extremely long half-life. Major CYP inhibitor."
    },
    "dronedarone": {
        "cid": 208898, "name": "Dronedarone", "formula": "C31H44N2O5S", "molecular_weight": 556.76,
        "class": "Antiarrhythmic", "subclass": "Class III",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4", "CYP2D6"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "bradycardia_risk"],
        "description": "Amiodarone analogue without iodine. CYP3A4 inhibitor."
    },
    "flecainide": {
        "cid": 3356, "name": "Flecainide", "formula": "C17H20F6N2O3", "molecular_weight": 414.34,
        "class": "Antiarrhythmic", "subclass": "Class IC",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "narrow_ti"],
        "description": "Class IC antiarrhythmic. CYP2D6 substrate. Narrow therapeutic index."
    },
    "sotalol": {
        "cid": 5253, "name": "Sotalol", "formula": "C12H20N2O3S", "molecular_weight": 272.36,
        "class": "Antiarrhythmic", "subclass": "Class III + Beta Blocker",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "bradycardia_risk", "beta_blocker"],
        "description": "Combined class III antiarrhythmic and beta-blocker. QT prolongation risk."
    },
    "digoxin": {
        "cid": 2724385, "name": "Digoxin", "formula": "C41H64O14", "molecular_weight": 780.94,
        "class": "Cardiac Glycoside", "subclass": "Inotrope",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["narrow_ti", "bradycardia_risk", "arrhythmia_risk"],
        "description": "Cardiac glycoside for heart failure and atrial fibrillation. Narrow therapeutic index. Toxicity enhanced by hypokalemia."
    },

    # ─── NSAIDs ──────────────────────────────────────────────────────────
    "ibuprofen": {
        "cid": 3672, "name": "Ibuprofen", "formula": "C13H18O2", "molecular_weight": 206.28,
        "class": "NSAID", "subclass": "Propionic Acid",
        "cyp_enzymes": ["CYP2C9", "CYP2C8"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nsaid", "gi_toxicity", "bleeding_risk", "nephrotoxic"],
        "description": "Non-selective COX inhibitor for pain and inflammation."
    },
    "naproxen": {
        "cid": 156391, "name": "Naproxen", "formula": "C14H14O3", "molecular_weight": 230.26,
        "class": "NSAID", "subclass": "Propionic Acid",
        "cyp_enzymes": ["CYP2C9", "CYP1A2"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nsaid", "gi_toxicity", "bleeding_risk", "nephrotoxic"],
        "description": "Long-acting NSAID. Lower cardiovascular risk than some NSAIDs."
    },
    "diclofenac": {
        "cid": 3033, "name": "Diclofenac", "formula": "C14H11Cl2NO2", "molecular_weight": 296.15,
        "class": "NSAID", "subclass": "Acetic Acid",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nsaid", "gi_toxicity", "bleeding_risk", "nephrotoxic", "hepatotoxic"],
        "description": "Potent NSAID. Higher cardiovascular risk than ibuprofen/naproxen."
    },
    "celecoxib": {
        "cid": 2662, "name": "Celecoxib", "formula": "C17H14F3N3O2S", "molecular_weight": 381.37,
        "class": "NSAID", "subclass": "COX-2 Selective",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": ["CYP2D6"], "cyp_induces": [],
        "pd_tags": ["nsaid", "nephrotoxic"],
        "description": "COX-2 selective NSAID. Lower GI toxicity but cardiovascular concerns."
    },
    "meloxicam": {
        "cid": 54677470, "name": "Meloxicam", "formula": "C14H13N3O4S2", "molecular_weight": 351.40,
        "class": "NSAID", "subclass": "Oxicam",
        "cyp_enzymes": ["CYP2C9", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nsaid", "gi_toxicity", "bleeding_risk", "nephrotoxic"],
        "description": "Preferential COX-2 inhibitor. Long half-life."
    },
    "ketorolac": {
        "cid": 3826, "name": "Ketorolac", "formula": "C15H13NO3", "molecular_weight": 255.27,
        "class": "NSAID", "subclass": "Acetic Acid",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nsaid", "gi_toxicity", "bleeding_risk", "nephrotoxic"],
        "description": "Powerful NSAID analgesic. Max 5 days use due to GI/renal toxicity."
    },
    "indomethacin": {
        "cid": 3715, "name": "Indomethacin", "formula": "C19H16ClNO4", "molecular_weight": 357.79,
        "class": "NSAID", "subclass": "Acetic Acid",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nsaid", "gi_toxicity", "bleeding_risk", "nephrotoxic"],
        "description": "Potent non-selective NSAID. High GI toxicity. Used for gout."
    },
    "piroxicam": {
        "cid": 54676228, "name": "Piroxicam", "formula": "C15H13N3O4S", "molecular_weight": 331.35,
        "class": "NSAID", "subclass": "Oxicam",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nsaid", "gi_toxicity", "bleeding_risk", "nephrotoxic"],
        "description": "Long-acting NSAID with high GI risk."
    },

    # ─── ANALGESICS ──────────────────────────────────────────────────────
    "acetaminophen": {
        "cid": 1983, "name": "Acetaminophen", "formula": "C8H9NO2", "molecular_weight": 151.16,
        "class": "Analgesic", "subclass": "Antipyretic",
        "cyp_enzymes": ["CYP2E1", "CYP1A2", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hepatotoxic"],
        "description": "Common analgesic. Hepatotoxic metabolite NAPQI formed by CYP2E1."
    },
    "tramadol": {
        "cid": 33741, "name": "Tramadol", "formula": "C16H25NO2", "molecular_weight": 263.38,
        "class": "Opioid", "subclass": "Weak Opioid Agonist + SNRI",
        "cyp_enzymes": ["CYP2D6", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant", "serotonergic", "seizure_risk"],
        "description": "Atypical opioid with serotonin/norepinephrine activity. Seizure risk."
    },
    "codeine": {
        "cid": 2703, "name": "Codeine", "formula": "C18H21NO3", "molecular_weight": 299.36,
        "class": "Opioid", "subclass": "Weak Opioid Agonist",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant", "respiratory_depression"],
        "description": "Prodrug converted to morphine by CYP2D6. Ultra-rapid metabolizers at risk."
    },
    "oxycodone": {
        "cid": 5284603, "name": "Oxycodone", "formula": "C18H21NO4", "molecular_weight": 315.36,
        "class": "Opioid", "subclass": "Strong Opioid Agonist",
        "cyp_enzymes": ["CYP3A4", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant", "respiratory_depression"],
        "description": "Strong opioid agonist. CYP3A4 inhibitors increase levels dangerously."
    },
    "hydrocodone": {
        "cid": 5284569, "name": "Hydrocodone", "formula": "C18H21NO3", "molecular_weight": 299.36,
        "class": "Opioid", "subclass": "Opioid Agonist",
        "cyp_enzymes": ["CYP3A4", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant", "respiratory_depression"],
        "description": "Opioid analgesic metabolized to hydromorphone by CYP2D6."
    },
    "morphine": {
        "cid": 5288826, "name": "Morphine", "formula": "C17H19NO3", "molecular_weight": 285.34,
        "class": "Opioid", "subclass": "Strong Opioid Agonist",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant", "respiratory_depression"],
        "description": "Prototype opioid. Glucuronidated, not CYP-dependent."
    },
    "fentanyl": {
        "cid": 3345, "name": "Fentanyl", "formula": "C22H28N2O", "molecular_weight": 336.47,
        "class": "Opioid", "subclass": "Strong Opioid Agonist",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant", "respiratory_depression"],
        "description": "Potent synthetic opioid. CYP3A4 inhibitors cause fatal overdose."
    },
    "buprenorphine": {
        "cid": 644073, "name": "Buprenorphine", "formula": "C29H41NO4", "molecular_weight": 467.64,
        "class": "Opioid", "subclass": "Partial Agonist",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant"],
        "description": "Partial opioid agonist for pain and opioid use disorder."
    },
    "methadone": {
        "cid": 4095, "name": "Methadone", "formula": "C21H27NO", "molecular_weight": 309.44,
        "class": "Opioid", "subclass": "Full Agonist",
        "cyp_enzymes": ["CYP3A4", "CYP2B6", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["opioid", "cns_depressant", "qt_prolongation", "respiratory_depression"],
        "description": "Long-acting opioid. QT prolongation risk. Complex CYP metabolism."
    },

    # ─── CNS: Antidepressants — SSRIs ────────────────────────────────────
    "fluoxetine": {
        "cid": 3386, "name": "Fluoxetine", "formula": "C17H18F3NO", "molecular_weight": 309.33,
        "class": "Antidepressant", "subclass": "SSRI",
        "cyp_enzymes": ["CYP2D6", "CYP2C9"], "cyp_inhibits": ["CYP2D6", "CYP2C19"], "cyp_induces": [],
        "pd_tags": ["ssri", "serotonergic", "bleeding_risk"],
        "description": "SSRI with potent CYP2D6 inhibition. Long half-life (fluoxetine + norfluoxetine)."
    },
    "sertraline": {
        "cid": 68617, "name": "Sertraline", "formula": "C17H17Cl2N", "molecular_weight": 306.23,
        "class": "Antidepressant", "subclass": "SSRI",
        "cyp_enzymes": ["CYP2B6", "CYP2C19", "CYP3A4"], "cyp_inhibits": ["CYP2D6"], "cyp_induces": [],
        "pd_tags": ["ssri", "serotonergic", "bleeding_risk"],
        "description": "SSRI with mild CYP2D6 inhibition."
    },
    "paroxetine": {
        "cid": 43815, "name": "Paroxetine", "formula": "C19H20FNO3", "molecular_weight": 329.37,
        "class": "Antidepressant", "subclass": "SSRI",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": ["CYP2D6"], "cyp_induces": [],
        "pd_tags": ["ssri", "serotonergic", "bleeding_risk"],
        "description": "SSRI with strongest CYP2D6 inhibition. Avoid with tamoxifen."
    },
    "citalopram": {
        "cid": 2771, "name": "Citalopram", "formula": "C20H21FN2O", "molecular_weight": 324.39,
        "class": "Antidepressant", "subclass": "SSRI",
        "cyp_enzymes": ["CYP2C19", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ssri", "serotonergic", "qt_prolongation", "bleeding_risk"],
        "description": "SSRI with dose-dependent QT prolongation. Max 40mg (20mg in elderly)."
    },
    "escitalopram": {
        "cid": 146570, "name": "Escitalopram", "formula": "C20H21FN2O", "molecular_weight": 324.39,
        "class": "Antidepressant", "subclass": "SSRI",
        "cyp_enzymes": ["CYP2C19", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["ssri", "serotonergic", "bleeding_risk"],
        "description": "S-enantiomer of citalopram. Generally fewer drug interactions."
    },
    "fluvoxamine": {
        "cid": 5324346, "name": "Fluvoxamine", "formula": "C15H21F3N2O2", "molecular_weight": 318.33,
        "class": "Antidepressant", "subclass": "SSRI",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": ["CYP1A2", "CYP2C19", "CYP3A4"], "cyp_induces": [],
        "pd_tags": ["ssri", "serotonergic", "bleeding_risk"],
        "description": "SSRI and potent CYP1A2 inhibitor. Major interaction with theophylline and warfarin."
    },

    # ─── CNS: Antidepressants — SNRIs ────────────────────────────────────
    "venlafaxine": {
        "cid": 5656, "name": "Venlafaxine", "formula": "C17H27NO2", "molecular_weight": 277.40,
        "class": "Antidepressant", "subclass": "SNRI",
        "cyp_enzymes": ["CYP2D6", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["snri", "serotonergic", "hypertension_risk"],
        "description": "SNRI for depression and anxiety. Dose-dependent hypertension."
    },
    "duloxetine": {
        "cid": 60835, "name": "Duloxetine", "formula": "C18H19NOS", "molecular_weight": 297.41,
        "class": "Antidepressant", "subclass": "SNRI",
        "cyp_enzymes": ["CYP1A2", "CYP2D6"], "cyp_inhibits": ["CYP2D6"], "cyp_induces": [],
        "pd_tags": ["snri", "serotonergic", "hepatotoxic"],
        "description": "SNRI metabolized by CYP1A2. Moderate CYP2D6 inhibitor."
    },
    "desvenlafaxine": {
        "cid": 125017, "name": "Desvenlafaxine", "formula": "C16H25NO2", "molecular_weight": 263.38,
        "class": "Antidepressant", "subclass": "SNRI",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["snri", "serotonergic"],
        "description": "Active metabolite of venlafaxine. Fewer CYP interactions."
    },
    "milnacipran": {
        "cid": 65833, "name": "Milnacipran", "formula": "C15H22N2O", "molecular_weight": 246.35,
        "class": "Antidepressant", "subclass": "SNRI",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["snri", "serotonergic"],
        "description": "SNRI for fibromyalgia. Minimal CYP metabolism."
    },

    # ─── CNS: Other Antidepressants ──────────────────────────────────────
    "bupropion": {
        "cid": 444, "name": "Bupropion", "formula": "C13H18ClNO", "molecular_weight": 239.74,
        "class": "Antidepressant", "subclass": "NDRI",
        "cyp_enzymes": ["CYP2B6"], "cyp_inhibits": ["CYP2D6"], "cyp_induces": [],
        "pd_tags": ["seizure_risk"],
        "description": "NDRI antidepressant and smoking cessation aid. Lowers seizure threshold."
    },
    "mirtazapine": {
        "cid": 4205, "name": "Mirtazapine", "formula": "C17H19N3", "molecular_weight": 265.36,
        "class": "Antidepressant", "subclass": "NaSSA",
        "cyp_enzymes": ["CYP3A4", "CYP1A2", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "serotonergic"],
        "description": "Noradrenergic and specific serotonergic antidepressant. Sedating."
    },
    "trazodone": {
        "cid": 5533, "name": "Trazodone", "formula": "C19H22ClN5O", "molecular_weight": 371.86,
        "class": "Antidepressant", "subclass": "SARI",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "serotonergic", "qt_prolongation"],
        "description": "Serotonin antagonist/reuptake inhibitor. Commonly used as sleep aid."
    },
    "amitriptyline": {
        "cid": 2160, "name": "Amitriptyline", "formula": "C20H23N", "molecular_weight": 277.40,
        "class": "Antidepressant", "subclass": "TCA",
        "cyp_enzymes": ["CYP2D6", "CYP2C19", "CYP1A2"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["tca", "cns_depressant", "serotonergic", "anticholinergic", "qt_prolongation", "narrow_ti"],
        "description": "Tricyclic antidepressant. Multiple CYP pathways. Cardiotoxic in overdose."
    },
    "nortriptyline": {
        "cid": 4543, "name": "Nortriptyline", "formula": "C19H21N", "molecular_weight": 263.38,
        "class": "Antidepressant", "subclass": "TCA",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["tca", "cns_depressant", "serotonergic", "anticholinergic", "qt_prolongation", "narrow_ti"],
        "description": "Active metabolite of amitriptyline. CYP2D6 substrate."
    },
    "doxepin": {
        "cid": 5284550, "name": "Doxepin", "formula": "C19H21NO", "molecular_weight": 279.38,
        "class": "Antidepressant", "subclass": "TCA",
        "cyp_enzymes": ["CYP2D6", "CYP2C19"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["tca", "cns_depressant", "serotonergic", "anticholinergic", "qt_prolongation"],
        "description": "Tricyclic with potent antihistamine effects. Used for insomnia at low doses."
    },

    # ─── CNS: Benzodiazepines ────────────────────────────────────────────
    "alprazolam": {
        "cid": 2118, "name": "Alprazolam", "formula": "C17H13ClN4", "molecular_weight": 308.76,
        "class": "Benzodiazepine", "subclass": "Anxiolytic",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "respiratory_depression", "benzodiazepine"],
        "description": "Short-acting benzodiazepine. CYP3A4 inhibitors increase levels dangerously."
    },
    "diazepam": {
        "cid": 3016, "name": "Diazepam", "formula": "C16H13ClN2O", "molecular_weight": 284.74,
        "class": "Benzodiazepine", "subclass": "Anxiolytic",
        "cyp_enzymes": ["CYP3A4", "CYP2C19"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "respiratory_depression", "benzodiazepine"],
        "description": "Long-acting benzodiazepine with active metabolites."
    },
    "lorazepam": {
        "cid": 3958, "name": "Lorazepam", "formula": "C15H10Cl2N2O2", "molecular_weight": 321.16,
        "class": "Benzodiazepine", "subclass": "Anxiolytic",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "respiratory_depression", "benzodiazepine"],
        "description": "Intermediate-acting benzodiazepine. Glucuronidated — no CYP interactions."
    },
    "clonazepam": {
        "cid": 2802, "name": "Clonazepam", "formula": "C15H10ClN3O3", "molecular_weight": 315.71,
        "class": "Benzodiazepine", "subclass": "Anticonvulsant",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "respiratory_depression", "benzodiazepine"],
        "description": "Long-acting benzodiazepine for seizures and panic disorder."
    },
    "midazolam": {
        "cid": 4192, "name": "Midazolam", "formula": "C18H13ClFN3", "molecular_weight": 325.77,
        "class": "Benzodiazepine", "subclass": "Sedative",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "respiratory_depression", "benzodiazepine"],
        "description": "Ultra-short acting benzodiazepine. CYP3A4 probe substrate."
    },

    # ─── CNS: Antipsychotics ─────────────────────────────────────────────
    "quetiapine": {
        "cid": 5002, "name": "Quetiapine", "formula": "C21H25N3O2S", "molecular_weight": 383.51,
        "class": "Antipsychotic", "subclass": "Atypical (SGA)",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "qt_prolongation", "metabolic_syndrome"],
        "description": "Atypical antipsychotic. CYP3A4 substrate."
    },
    "risperidone": {
        "cid": 5073, "name": "Risperidone", "formula": "C23H27FN4O2", "molecular_weight": 410.48,
        "class": "Antipsychotic", "subclass": "Atypical (SGA)",
        "cyp_enzymes": ["CYP2D6", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "metabolic_syndrome"],
        "description": "Atypical antipsychotic metabolized by CYP2D6."
    },
    "olanzapine": {
        "cid": 135398745, "name": "Olanzapine", "formula": "C17H20N4S", "molecular_weight": 312.43,
        "class": "Antipsychotic", "subclass": "Atypical (SGA)",
        "cyp_enzymes": ["CYP1A2", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "metabolic_syndrome"],
        "description": "Atypical antipsychotic. CYP1A2 substrate — smoking induces metabolism."
    },
    "aripiprazole": {
        "cid": 60795, "name": "Aripiprazole", "formula": "C23H27Cl2N3O2", "molecular_weight": 448.39,
        "class": "Antipsychotic", "subclass": "Atypical (SGA)",
        "cyp_enzymes": ["CYP2D6", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Partial dopamine agonist. CYP2D6 and CYP3A4 substrate."
    },
    "haloperidol": {
        "cid": 3559, "name": "Haloperidol", "formula": "C21H23ClFNO2", "molecular_weight": 375.86,
        "class": "Antipsychotic", "subclass": "Typical (FGA)",
        "cyp_enzymes": ["CYP3A4", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "eps_risk"],
        "description": "Typical antipsychotic. QT prolongation and extrapyramidal effects."
    },
    "clozapine": {
        "cid": 2818, "name": "Clozapine", "formula": "C18H19ClN4", "molecular_weight": 326.82,
        "class": "Antipsychotic", "subclass": "Atypical (SGA)",
        "cyp_enzymes": ["CYP1A2", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "seizure_risk", "metabolic_syndrome", "narrow_ti"],
        "description": "Atypical antipsychotic for treatment-resistant schizophrenia. CYP1A2 substrate. Agranulocytosis risk."
    },
    "ziprasidone": {
        "cid": 60854, "name": "Ziprasidone", "formula": "C21H21ClN4OS", "molecular_weight": 412.94,
        "class": "Antipsychotic", "subclass": "Atypical (SGA)",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation"],
        "description": "Atypical antipsychotic with significant QT prolongation risk."
    },
    "lurasidone": {
        "cid": 213046, "name": "Lurasidone", "formula": "C28H36N4O2S", "molecular_weight": 492.68,
        "class": "Antipsychotic", "subclass": "Atypical (SGA)",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Atypical antipsychotic. CYP3A4 substrate — contraindicated with strong CYP3A4 inhibitors."
    },

    # ─── CNS: Anticonvulsants ────────────────────────────────────────────
    "gabapentin": {
        "cid": 3446, "name": "Gabapentin", "formula": "C9H17NO2", "molecular_weight": 171.24,
        "class": "Anticonvulsant", "subclass": "Gabapentinoid",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant"],
        "description": "Used for neuropathic pain and seizures. Not CYP-metabolized."
    },
    "pregabalin": {
        "cid": 5486971, "name": "Pregabalin", "formula": "C8H17NO2", "molecular_weight": 159.23,
        "class": "Anticonvulsant", "subclass": "Gabapentinoid",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant"],
        "description": "Gabapentinoid for neuropathic pain, fibromyalgia, seizures."
    },
    "carbamazepine": {
        "cid": 2554, "name": "Carbamazepine", "formula": "C15H12N2O", "molecular_weight": 236.27,
        "class": "Anticonvulsant", "subclass": "Sodium Channel Blocker",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": ["CYP3A4", "CYP2C9", "CYP1A2"],
        "pd_tags": ["narrow_ti", "serotonergic"],
        "description": "Potent CYP3A4 inducer — reduces levels of many drugs. Autoinduction."
    },
    "phenytoin": {
        "cid": 1775, "name": "Phenytoin", "formula": "C15H12N2O2", "molecular_weight": 252.27,
        "class": "Anticonvulsant", "subclass": "Hydantoin",
        "cyp_enzymes": ["CYP2C9", "CYP2C19"], "cyp_inhibits": [], "cyp_induces": ["CYP3A4", "CYP2C9"],
        "pd_tags": ["narrow_ti"],
        "description": "Anticonvulsant with complex nonlinear pharmacokinetics. CYP inducer."
    },
    "valproic acid": {
        "cid": 3121, "name": "Valproic Acid", "formula": "C8H16O2", "molecular_weight": 144.21,
        "class": "Anticonvulsant", "subclass": "Broad Spectrum",
        "cyp_enzymes": ["CYP2C9", "CYP2A6"], "cyp_inhibits": ["CYP2C9"], "cyp_induces": [],
        "pd_tags": ["hepatotoxic", "teratogenic", "narrow_ti", "bleeding_risk"],
        "description": "Broad-spectrum anticonvulsant. CYP2C9 inhibitor. Hepatotoxic and teratogenic."
    },
    "lamotrigine": {
        "cid": 3878, "name": "Lamotrigine", "formula": "C9H7Cl2N5", "molecular_weight": 256.09,
        "class": "Anticonvulsant", "subclass": "Sodium Channel Blocker",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Anticonvulsant and mood stabilizer. Glucuronidated — valproic acid doubles levels."
    },
    "levetiracetam": {
        "cid": 441341, "name": "Levetiracetam", "formula": "C8H14N2O2", "molecular_weight": 170.21,
        "class": "Anticonvulsant", "subclass": "SV2A Ligand",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Anticonvulsant with no significant CYP interactions. Renally eliminated."
    },
    "topiramate": {
        "cid": 5284627, "name": "Topiramate", "formula": "C12H21NO8S", "molecular_weight": 339.36,
        "class": "Anticonvulsant", "subclass": "GABAergic + Glutamate blocker",
        "cyp_enzymes": ["CYP2C19"], "cyp_inhibits": ["CYP2C19"], "cyp_induces": ["CYP3A4"],
        "pd_tags": ["nephrotoxic"],
        "description": "Anticonvulsant for epilepsy and migraines. Mild CYP3A4 inducer."
    },
    "oxcarbazepine": {
        "cid": 34312, "name": "Oxcarbazepine", "formula": "C15H12N2O2", "molecular_weight": 252.27,
        "class": "Anticonvulsant", "subclass": "Sodium Channel Blocker",
        "cyp_enzymes": [], "cyp_inhibits": ["CYP2C19"], "cyp_induces": ["CYP3A4"],
        "pd_tags": [],
        "description": "Carbamazepine analogue with fewer interactions. Mild CYP3A4 inducer."
    },

    # ─── CNS: Mood Stabilizers / ADHD ────────────────────────────────────
    "lithium": {
        "cid": 3028194, "name": "Lithium", "formula": "Li2CO3", "molecular_weight": 73.89,
        "class": "Mood Stabilizer", "subclass": "Alkali Metal Salt",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["narrow_ti", "nephrotoxic", "thyroid_toxic"],
        "description": "Mood stabilizer with very narrow therapeutic index. NSAIDs and diuretics increase levels."
    },
    "methylphenidate": {
        "cid": 4158, "name": "Methylphenidate", "formula": "C14H19NO2", "molecular_weight": 233.31,
        "class": "Stimulant", "subclass": "ADHD Medication",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hypertension_risk"],
        "description": "CNS stimulant for ADHD. Not significantly CYP-metabolized."
    },
    "amphetamine": {
        "cid": 3007, "name": "Amphetamine", "formula": "C9H13N", "molecular_weight": 135.21,
        "class": "Stimulant", "subclass": "ADHD Medication",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hypertension_risk", "serotonergic"],
        "description": "CNS stimulant for ADHD. Avoid with MAOIs."
    },

    # ─── CNS: Sleep / Sedatives ──────────────────────────────────────────
    "zolpidem": {
        "cid": 5732, "name": "Zolpidem", "formula": "C19H21N3O", "molecular_weight": 307.39,
        "class": "Sedative-Hypnotic", "subclass": "Z-drug",
        "cyp_enzymes": ["CYP3A4", "CYP1A2"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant"],
        "description": "Non-benzodiazepine sleep aid. CYP3A4 substrate."
    },
    "suvorexant": {
        "cid": 53340666, "name": "Suvorexant", "formula": "C23H23ClN6O2", "molecular_weight": 450.92,
        "class": "Sedative-Hypnotic", "subclass": "Orexin Receptor Antagonist",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant"],
        "description": "Orexin receptor antagonist for insomnia. CYP3A4 substrate."
    },

    # ─── ANTIBIOTICS ─────────────────────────────────────────────────────
    "ciprofloxacin": {
        "cid": 2764, "name": "Ciprofloxacin", "formula": "C17H18FN3O3", "molecular_weight": 331.34,
        "class": "Antibiotic", "subclass": "Fluoroquinolone",
        "cyp_enzymes": [], "cyp_inhibits": ["CYP1A2"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "tendon_risk"],
        "description": "Fluoroquinolone antibiotic. Potent CYP1A2 inhibitor."
    },
    "levofloxacin": {
        "cid": 149096, "name": "Levofloxacin", "formula": "C18H20FN3O4", "molecular_weight": 361.37,
        "class": "Antibiotic", "subclass": "Fluoroquinolone",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "tendon_risk"],
        "description": "Fluoroquinolone with less CYP inhibition than ciprofloxacin."
    },
    "moxifloxacin": {
        "cid": 152946, "name": "Moxifloxacin", "formula": "C21H24FN3O4", "molecular_weight": 401.43,
        "class": "Antibiotic", "subclass": "Fluoroquinolone",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "tendon_risk"],
        "description": "Fluoroquinolone with highest QT prolongation risk among FQs."
    },
    "azithromycin": {
        "cid": 447043, "name": "Azithromycin", "formula": "C38H72N2O12", "molecular_weight": 748.98,
        "class": "Antibiotic", "subclass": "Macrolide",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation"],
        "description": "Macrolide antibiotic with minimal CYP interactions. QT prolongation risk."
    },
    "erythromycin": {
        "cid": 12560, "name": "Erythromycin", "formula": "C37H67NO13", "molecular_weight": 733.93,
        "class": "Antibiotic", "subclass": "Macrolide",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation"],
        "description": "Macrolide antibiotic. Strong CYP3A4 inhibitor. QT prolongation."
    },
    "clarithromycin": {
        "cid": 84029, "name": "Clarithromycin", "formula": "C38H69NO13", "molecular_weight": 747.95,
        "class": "Antibiotic", "subclass": "Macrolide",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation"],
        "description": "Macrolide and potent CYP3A4 inhibitor. Many drug interactions."
    },
    "amoxicillin": {
        "cid": 33613, "name": "Amoxicillin", "formula": "C16H19N3O5S", "molecular_weight": 365.40,
        "class": "Antibiotic", "subclass": "Penicillin",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Broad-spectrum penicillin. Minimal drug interactions."
    },
    "doxycycline": {
        "cid": 54671203, "name": "Doxycycline", "formula": "C22H24N2O8", "molecular_weight": 444.43,
        "class": "Antibiotic", "subclass": "Tetracycline",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Tetracycline antibiotic. Chelates with divalent cations."
    },
    "metronidazole": {
        "cid": 4173, "name": "Metronidazole", "formula": "C6H9N3O3", "molecular_weight": 171.15,
        "class": "Antibiotic", "subclass": "Nitroimidazole",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP2C9"], "cyp_induces": [],
        "pd_tags": ["disulfiram_reaction"],
        "description": "Antibiotic/antiprotozoal. CYP2C9 inhibitor. Disulfiram reaction with alcohol."
    },
    "trimethoprim": {
        "cid": 5578, "name": "Trimethoprim", "formula": "C14H18N4O3", "molecular_weight": 290.32,
        "class": "Antibiotic", "subclass": "Folate Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hyperkalemia_risk"],
        "description": "Antibiotic causing hyperkalemia. Dangerous with RAAS inhibitors."
    },
    "sulfamethoxazole": {
        "cid": 5329, "name": "Sulfamethoxazole", "formula": "C10H11N3O3S", "molecular_weight": 253.28,
        "class": "Antibiotic", "subclass": "Sulfonamide",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": ["CYP2C9"], "cyp_induces": [],
        "pd_tags": ["hyperkalemia_risk"],
        "description": "Sulfonamide antibiotic. CYP2C9 inhibitor. Increases warfarin levels."
    },
    "rifampin": {
        "cid": 5381226, "name": "Rifampin", "formula": "C43H58N4O12", "molecular_weight": 822.94,
        "class": "Antibiotic", "subclass": "Rifamycin",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": ["CYP3A4", "CYP2C9", "CYP2C19", "CYP1A2", "CYP2B6"],
        "pd_tags": ["hepatotoxic"],
        "description": "Most potent CYP inducer known. Reduces levels of almost every CYP-metabolized drug."
    },
    "isoniazid": {
        "cid": 3767, "name": "Isoniazid", "formula": "C6H7N3O", "molecular_weight": 137.14,
        "class": "Antibiotic", "subclass": "Antimycobacterial",
        "cyp_enzymes": [], "cyp_inhibits": ["CYP2C19", "CYP3A4"], "cyp_induces": ["CYP2E1"],
        "pd_tags": ["hepatotoxic"],
        "description": "Anti-tuberculosis drug. CYP inhibitor and CYP2E1 inducer. Hepatotoxic."
    },
    "linezolid": {
        "cid": 441401, "name": "Linezolid", "formula": "C16H20FN3O4", "molecular_weight": 337.35,
        "class": "Antibiotic", "subclass": "Oxazolidinone",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["maoi", "serotonergic"],
        "description": "Oxazolidinone antibiotic with weak MAOI activity. Serotonin syndrome risk with SSRIs."
    },
    "nitrofurantoin": {
        "cid": 6604200, "name": "Nitrofurantoin", "formula": "C8H6N4O5", "molecular_weight": 238.16,
        "class": "Antibiotic", "subclass": "Nitrofuran",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Urinary tract antibiotic. Minimal systemic interactions."
    },

    # ─── ANTIFUNGALS ─────────────────────────────────────────────────────
    "fluconazole": {
        "cid": 3365, "name": "Fluconazole", "formula": "C13H12F2N6O", "molecular_weight": 306.27,
        "class": "Antifungal", "subclass": "Azole",
        "cyp_enzymes": [], "cyp_inhibits": ["CYP2C9", "CYP2C19", "CYP3A4"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "hepatotoxic"],
        "description": "Azole antifungal. Potent CYP2C9 and CYP3A4 inhibitor."
    },
    "itraconazole": {
        "cid": 55283, "name": "Itraconazole", "formula": "C35H38Cl2N8O4", "molecular_weight": 705.63,
        "class": "Antifungal", "subclass": "Azole",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "hepatotoxic"],
        "description": "Potent CYP3A4 inhibitor. Contraindicated with many drugs."
    },
    "ketoconazole": {
        "cid": 456201, "name": "Ketoconazole", "formula": "C26H28Cl2N4O4", "molecular_weight": 531.43,
        "class": "Antifungal", "subclass": "Azole",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4", "CYP2C9"], "cyp_induces": [],
        "pd_tags": ["hepatotoxic", "qt_prolongation"],
        "description": "Strongest CYP3A4 inhibitor among azoles. Restricted use due to hepatotoxicity."
    },
    "voriconazole": {
        "cid": 71616, "name": "Voriconazole", "formula": "C16H14F3N5O", "molecular_weight": 349.31,
        "class": "Antifungal", "subclass": "Azole",
        "cyp_enzymes": ["CYP2C19", "CYP2C9", "CYP3A4"], "cyp_inhibits": ["CYP3A4", "CYP2C9", "CYP2C19"], "cyp_induces": [],
        "pd_tags": ["hepatotoxic", "qt_prolongation"],
        "description": "Broad-spectrum azole. Potent multi-CYP inhibitor. Nonlinear pharmacokinetics."
    },
    "posaconazole": {
        "cid": 468595, "name": "Posaconazole", "formula": "C37H42F2N8O4", "molecular_weight": 700.77,
        "class": "Antifungal", "subclass": "Azole",
        "cyp_enzymes": [], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["hepatotoxic"],
        "description": "Extended-spectrum azole. Strong CYP3A4 inhibitor."
    },

    # ─── DIABETES / ENDOCRINE ────────────────────────────────────────────
    "metformin": {
        "cid": 4091, "name": "Metformin", "formula": "C4H11N5", "molecular_weight": 129.16,
        "class": "Antidiabetic", "subclass": "Biguanide",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["lactic_acidosis_risk"],
        "description": "First-line diabetes drug. Renally eliminated. Lactic acidosis risk with renal impairment."
    },
    "glipizide": {
        "cid": 3478, "name": "Glipizide", "formula": "C21H27N5O4S", "molecular_weight": 445.54,
        "class": "Antidiabetic", "subclass": "Sulfonylurea",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hypoglycemia_risk"],
        "description": "Sulfonylurea metabolized by CYP2C9. Hypoglycemia risk with CYP2C9 inhibitors."
    },
    "glyburide": {
        "cid": 3488, "name": "Glyburide", "formula": "C23H28ClN3O5S", "molecular_weight": 493.99,
        "class": "Antidiabetic", "subclass": "Sulfonylurea",
        "cyp_enzymes": ["CYP2C9", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hypoglycemia_risk"],
        "description": "Sulfonylurea with higher hypoglycemia risk than glipizide."
    },
    "glimepiride": {
        "cid": 3476, "name": "Glimepiride", "formula": "C24H34N4O5S", "molecular_weight": 490.62,
        "class": "Antidiabetic", "subclass": "Sulfonylurea",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hypoglycemia_risk"],
        "description": "Third-generation sulfonylurea."
    },
    "sitagliptin": {
        "cid": 4369359, "name": "Sitagliptin", "formula": "C16H15F6N5O", "molecular_weight": 407.31,
        "class": "Antidiabetic", "subclass": "DPP-4 Inhibitor",
        "cyp_enzymes": ["CYP3A4", "CYP2C8"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "DPP-4 inhibitor for type 2 diabetes. Few significant interactions."
    },
    "empagliflozin": {
        "cid": 11949646, "name": "Empagliflozin", "formula": "C23H27ClO7", "molecular_weight": 450.91,
        "class": "Antidiabetic", "subclass": "SGLT2 Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["dehydration_risk"],
        "description": "SGLT2 inhibitor with cardiovascular benefits. Minimal CYP interactions."
    },
    "dapagliflozin": {
        "cid": 9887712, "name": "Dapagliflozin", "formula": "C21H25ClO6", "molecular_weight": 408.87,
        "class": "Antidiabetic", "subclass": "SGLT2 Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["dehydration_risk"],
        "description": "SGLT2 inhibitor for diabetes and heart failure."
    },
    "canagliflozin": {
        "cid": 24812758, "name": "Canagliflozin", "formula": "C24H25FO5S", "molecular_weight": 444.52,
        "class": "Antidiabetic", "subclass": "SGLT2 Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["dehydration_risk"],
        "description": "SGLT2 inhibitor. Associated with toe amputation risk."
    },
    "pioglitazone": {
        "cid": 4829, "name": "Pioglitazone", "formula": "C19H20N2O3S", "molecular_weight": 356.44,
        "class": "Antidiabetic", "subclass": "Thiazolidinedione",
        "cyp_enzymes": ["CYP2C8", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["heart_failure_risk"],
        "description": "PPAR-gamma agonist for diabetes. CYP2C8 substrate."
    },
    "liraglutide": {
        "cid": 16134956, "name": "Liraglutide", "formula": "GLP-1 RA", "molecular_weight": 3751.20,
        "class": "Antidiabetic", "subclass": "GLP-1 Receptor Agonist",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "GLP-1 receptor agonist for diabetes and obesity. Peptide — no CYP interactions."
    },
    "semaglutide": {
        "cid": 56843331, "name": "Semaglutide", "formula": "GLP-1 RA", "molecular_weight": 4113.58,
        "class": "Antidiabetic", "subclass": "GLP-1 Receptor Agonist",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "GLP-1 RA for diabetes and obesity (Ozempic/Wegovy). Delays gastric emptying."
    },
    "levothyroxine": {
        "cid": 5819, "name": "Levothyroxine", "formula": "C15H11I4NO4", "molecular_weight": 776.87,
        "class": "Thyroid Hormone", "subclass": "T4 Replacement",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["narrow_ti"],
        "description": "Thyroid hormone replacement. Narrow therapeutic index. Absorption affected by many drugs."
    },

    # ─── GI MEDICATIONS ──────────────────────────────────────────────────
    "omeprazole": {
        "cid": 4594, "name": "Omeprazole", "formula": "C17H19N3O3S", "molecular_weight": 345.42,
        "class": "PPI", "subclass": "Proton Pump Inhibitor",
        "cyp_enzymes": ["CYP2C19", "CYP3A4"], "cyp_inhibits": ["CYP2C19"], "cyp_induces": [],
        "pd_tags": [],
        "description": "PPI. CYP2C19 inhibitor — reduces clopidogrel activation."
    },
    "pantoprazole": {
        "cid": 4679, "name": "Pantoprazole", "formula": "C16H15F2N3O4S", "molecular_weight": 383.37,
        "class": "PPI", "subclass": "Proton Pump Inhibitor",
        "cyp_enzymes": ["CYP2C19"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "PPI with less CYP2C19 inhibition than omeprazole. Preferred with clopidogrel."
    },
    "esomeprazole": {
        "cid": 9579578, "name": "Esomeprazole", "formula": "C17H19N3O3S", "molecular_weight": 345.42,
        "class": "PPI", "subclass": "Proton Pump Inhibitor",
        "cyp_enzymes": ["CYP2C19", "CYP3A4"], "cyp_inhibits": ["CYP2C19"], "cyp_induces": [],
        "pd_tags": [],
        "description": "S-isomer of omeprazole. Similar CYP2C19 inhibition profile."
    },
    "lansoprazole": {
        "cid": 3883, "name": "Lansoprazole", "formula": "C16H14F3N3O2S", "molecular_weight": 369.36,
        "class": "PPI", "subclass": "Proton Pump Inhibitor",
        "cyp_enzymes": ["CYP2C19", "CYP3A4"], "cyp_inhibits": ["CYP2C19"], "cyp_induces": ["CYP1A2"],
        "pd_tags": [],
        "description": "PPI metabolized by CYP2C19 and CYP3A4."
    },
    "ranitidine": {
        "cid": 3033332, "name": "Ranitidine", "formula": "C13H22N4O3S", "molecular_weight": 314.40,
        "class": "H2 Blocker", "subclass": "Histamine H2 Antagonist",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "H2 blocker (withdrawn in many markets due to NDMA contamination)."
    },
    "famotidine": {
        "cid": 5702160, "name": "Famotidine", "formula": "C8H15N7O2S3", "molecular_weight": 337.45,
        "class": "H2 Blocker", "subclass": "Histamine H2 Antagonist",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "H2 blocker with no significant CYP interactions."
    },
    "ondansetron": {
        "cid": 4595, "name": "Ondansetron", "formula": "C18H19N3O", "molecular_weight": 293.36,
        "class": "Antiemetic", "subclass": "5-HT3 Antagonist",
        "cyp_enzymes": ["CYP3A4", "CYP1A2", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation"],
        "description": "5-HT3 antagonist antiemetic. QT prolongation risk."
    },
    "metoclopramide": {
        "cid": 4168, "name": "Metoclopramide", "formula": "C14H22ClN3O2", "molecular_weight": 299.80,
        "class": "Antiemetic", "subclass": "Dopamine Antagonist",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["eps_risk"],
        "description": "Prokinetic antiemetic. Extrapyramidal effects. Avoid with antipsychotics."
    },

    # ─── CORTICOSTEROIDS ─────────────────────────────────────────────────
    "prednisone": {
        "cid": 5865, "name": "Prednisone", "formula": "C21H26O5", "molecular_weight": 358.43,
        "class": "Corticosteroid", "subclass": "Glucocorticoid",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hyperglycemia_risk", "gi_toxicity", "immunosuppressant"],
        "description": "Synthetic corticosteroid for inflammation and immune suppression."
    },
    "prednisolone": {
        "cid": 5755, "name": "Prednisolone", "formula": "C21H28O5", "molecular_weight": 360.44,
        "class": "Corticosteroid", "subclass": "Glucocorticoid",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hyperglycemia_risk", "gi_toxicity", "immunosuppressant"],
        "description": "Active metabolite of prednisone."
    },
    "dexamethasone": {
        "cid": 5743, "name": "Dexamethasone", "formula": "C22H29FO5", "molecular_weight": 392.46,
        "class": "Corticosteroid", "subclass": "Glucocorticoid",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": ["CYP3A4"],
        "pd_tags": ["hyperglycemia_risk", "immunosuppressant"],
        "description": "Potent corticosteroid. CYP3A4 inducer at high doses."
    },
    "methylprednisolone": {
        "cid": 6741, "name": "Methylprednisolone", "formula": "C22H30O5", "molecular_weight": 374.47,
        "class": "Corticosteroid", "subclass": "Glucocorticoid",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hyperglycemia_risk", "gi_toxicity", "immunosuppressant"],
        "description": "Corticosteroid used IV for acute inflammation."
    },

    # ─── IMMUNOSUPPRESSANTS ──────────────────────────────────────────────
    "cyclosporine": {
        "cid": 5284373, "name": "Cyclosporine", "formula": "C62H111N11O12", "molecular_weight": 1202.61,
        "class": "Immunosuppressant", "subclass": "Calcineurin Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": ["nephrotoxic", "narrow_ti", "hyperkalemia_risk"],
        "description": "Calcineurin inhibitor. CYP3A4 substrate and inhibitor. Nephrotoxic. Narrow TI."
    },
    "tacrolimus": {
        "cid": 445643, "name": "Tacrolimus", "formula": "C44H69NO12", "molecular_weight": 804.02,
        "class": "Immunosuppressant", "subclass": "Calcineurin Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nephrotoxic", "narrow_ti", "hyperkalemia_risk", "qt_prolongation"],
        "description": "Calcineurin inhibitor. CYP3A4 substrate. Narrower TI than cyclosporine."
    },
    "mycophenolate": {
        "cid": 5281078, "name": "Mycophenolate", "formula": "C23H31NO7", "molecular_weight": 433.49,
        "class": "Immunosuppressant", "subclass": "IMPDH Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["immunosuppressant", "teratogenic"],
        "description": "Inosine monophosphate dehydrogenase inhibitor. Glucuronidated."
    },
    "methotrexate": {
        "cid": 126941, "name": "Methotrexate", "formula": "C20H22N8O5", "molecular_weight": 454.44,
        "class": "Immunosuppressant", "subclass": "Antimetabolite / DMARD",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hepatotoxic", "nephrotoxic", "teratogenic", "narrow_ti"],
        "description": "Folate antagonist for autoimmune disease and cancer. NSAIDs increase toxicity by reducing renal clearance."
    },
    "azathioprine": {
        "cid": 2265, "name": "Azathioprine", "formula": "C9H7N7O2S", "molecular_weight": 277.26,
        "class": "Immunosuppressant", "subclass": "Purine Antagonist",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["immunosuppressant", "hepatotoxic", "narrow_ti"],
        "description": "Purine antimetabolite. Metabolized by xanthine oxidase — contraindicated with allopurinol."
    },

    # ─── RESPIRATORY ─────────────────────────────────────────────────────
    "montelukast": {
        "cid": 5281040, "name": "Montelukast", "formula": "C35H36ClNO3S", "molecular_weight": 586.18,
        "class": "Respiratory", "subclass": "Leukotriene Receptor Antagonist",
        "cyp_enzymes": ["CYP2C8", "CYP3A4", "CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Leukotriene antagonist for asthma. CYP2C8 substrate."
    },
    "theophylline": {
        "cid": 2153, "name": "Theophylline", "formula": "C7H8N4O2", "molecular_weight": 180.16,
        "class": "Respiratory", "subclass": "Methylxanthine",
        "cyp_enzymes": ["CYP1A2", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["narrow_ti", "seizure_risk", "arrhythmia_risk"],
        "description": "Bronchodilator with narrow TI. CYP1A2 substrate — ciprofloxacin causes toxicity."
    },
    "cetirizine": {
        "cid": 2678, "name": "Cetirizine", "formula": "C21H25ClN2O3", "molecular_weight": 388.89,
        "class": "Antihistamine", "subclass": "2nd Generation",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Non-sedating antihistamine. Minimal drug interactions."
    },
    "loratadine": {
        "cid": 3957, "name": "Loratadine", "formula": "C22H23ClN2O2", "molecular_weight": 382.88,
        "class": "Antihistamine", "subclass": "2nd Generation",
        "cyp_enzymes": ["CYP3A4", "CYP2D6"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Non-sedating antihistamine metabolized by CYP3A4."
    },
    "diphenhydramine": {
        "cid": 3100, "name": "Diphenhydramine", "formula": "C17H21NO", "molecular_weight": 255.36,
        "class": "Antihistamine", "subclass": "1st Generation",
        "cyp_enzymes": ["CYP2D6"], "cyp_inhibits": ["CYP2D6"], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "anticholinergic"],
        "description": "First-gen antihistamine. Sedating. Anticholinergic effects."
    },

    # ─── MUSCLE RELAXANTS ────────────────────────────────────────────────
    "cyclobenzaprine": {
        "cid": 2895, "name": "Cyclobenzaprine", "formula": "C20H21N", "molecular_weight": 275.39,
        "class": "Muscle Relaxant", "subclass": "Central Acting",
        "cyp_enzymes": ["CYP1A2", "CYP2D6", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "anticholinergic", "serotonergic"],
        "description": "Structurally related to TCAs. Serotonin syndrome risk with SSRIs."
    },
    "tizanidine": {
        "cid": 5487, "name": "Tizanidine", "formula": "C9H8ClN5S", "molecular_weight": 253.71,
        "class": "Muscle Relaxant", "subclass": "Alpha-2 Agonist",
        "cyp_enzymes": ["CYP1A2"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant", "hypotension_risk"],
        "description": "Alpha-2 agonist muscle relaxant. CYP1A2 substrate — CONTRAINDICATED with ciprofloxacin/fluvoxamine."
    },
    "baclofen": {
        "cid": 2284, "name": "Baclofen", "formula": "C10H12ClNO2", "molecular_weight": 213.66,
        "class": "Muscle Relaxant", "subclass": "GABA-B Agonist",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["cns_depressant"],
        "description": "GABA-B agonist for spasticity. Renally eliminated."
    },

    # ─── GOUT ────────────────────────────────────────────────────────────
    "allopurinol": {
        "cid": 135401907, "name": "Allopurinol", "formula": "C5H4N4O", "molecular_weight": 136.11,
        "class": "Antigout", "subclass": "Xanthine Oxidase Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Xanthine oxidase inhibitor. Contraindicated with azathioprine/6-MP — fatal myelosuppression."
    },
    "colchicine": {
        "cid": 6167, "name": "Colchicine", "formula": "C22H25NO6", "molecular_weight": 399.44,
        "class": "Antigout", "subclass": "Anti-inflammatory",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["narrow_ti"],
        "description": "Anti-gout agent with narrow TI. CYP3A4 substrate — fatal toxicity with strong CYP3A4 inhibitors."
    },
    "febuxostat": {
        "cid": 134018, "name": "Febuxostat", "formula": "C16H16N2O3S", "molecular_weight": 316.37,
        "class": "Antigout", "subclass": "Xanthine Oxidase Inhibitor",
        "cyp_enzymes": ["CYP2C9"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "Non-purine xanthine oxidase inhibitor for gout."
    },

    # ─── ONCOLOGY (commonly interacting) ─────────────────────────────────
    "tamoxifen": {
        "cid": 2733526, "name": "Tamoxifen", "formula": "C26H29NO", "molecular_weight": 371.51,
        "class": "Antineoplastic", "subclass": "SERM",
        "cyp_enzymes": ["CYP2D6", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "prodrug"],
        "description": "SERM for breast cancer. Prodrug activated by CYP2D6 — avoid paroxetine/fluoxetine."
    },
    "imatinib": {
        "cid": 5291, "name": "Imatinib", "formula": "C29H31N7O", "molecular_weight": 493.60,
        "class": "Antineoplastic", "subclass": "Tyrosine Kinase Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": ["CYP3A4", "CYP2D6", "CYP2C9"], "cyp_induces": [],
        "pd_tags": ["hepatotoxic", "qt_prolongation"],
        "description": "TKI for CML. CYP3A4 substrate and CYP inhibitor."
    },
    "erlotinib": {
        "cid": 176870, "name": "Erlotinib", "formula": "C22H23N3O4", "molecular_weight": 393.44,
        "class": "Antineoplastic", "subclass": "EGFR Inhibitor",
        "cyp_enzymes": ["CYP3A4", "CYP1A2"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["hepatotoxic"],
        "description": "EGFR inhibitor. CYP3A4 and CYP1A2 substrate."
    },
    "cyclophosphamide": {
        "cid": 2907, "name": "Cyclophosphamide", "formula": "C7H15Cl2N2O2P", "molecular_weight": 261.08,
        "class": "Antineoplastic", "subclass": "Alkylating Agent",
        "cyp_enzymes": ["CYP2B6", "CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["immunosuppressant", "nephrotoxic", "hepatotoxic"],
        "description": "Alkylating agent prodrug activated by CYP2B6. CYP3A4 inducers increase toxicity."
    },

    # ─── ANTIVIRALS ──────────────────────────────────────────────────────
    "ritonavir": {
        "cid": 392622, "name": "Ritonavir", "formula": "C37H48N6O5S2", "molecular_weight": 720.94,
        "class": "Antiviral", "subclass": "HIV Protease Inhibitor",
        "cyp_enzymes": ["CYP3A4", "CYP2D6"], "cyp_inhibits": ["CYP3A4", "CYP2D6"], "cyp_induces": [],
        "pd_tags": ["qt_prolongation", "hepatotoxic"],
        "description": "Most potent CYP3A4 inhibitor. Used as pharmacokinetic booster."
    },
    "nirmatrelvir": {
        "cid": 155903259, "name": "Nirmatrelvir", "formula": "C23H32F3N5O4", "molecular_weight": 499.53,
        "class": "Antiviral", "subclass": "SARS-CoV-2 Protease Inhibitor",
        "cyp_enzymes": ["CYP3A4"], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": [],
        "description": "COVID-19 antiviral (Paxlovid component). Given with ritonavir booster."
    },
    "acyclovir": {
        "cid": 135398513, "name": "Acyclovir", "formula": "C8H11N5O3", "molecular_weight": 225.20,
        "class": "Antiviral", "subclass": "Nucleoside Analogue",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nephrotoxic"],
        "description": "Antiviral for herpes. Renally eliminated. Nephrotoxic at high doses."
    },
    "valacyclovir": {
        "cid": 135398740, "name": "Valacyclovir", "formula": "C13H20N6O4", "molecular_weight": 324.33,
        "class": "Antiviral", "subclass": "Nucleoside Analogue",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": [],
        "pd_tags": ["nephrotoxic"],
        "description": "Prodrug of acyclovir with better oral bioavailability."
    },

    # ─── SUPPLEMENTS / OTC with interactions ─────────────────────────────
    "st_johns_wort": {
        "cid": 122724, "name": "St. John's Wort", "formula": "Hypericum perforatum", "molecular_weight": 504.44,
        "class": "Supplement", "subclass": "Herbal",
        "cyp_enzymes": [], "cyp_inhibits": [], "cyp_induces": ["CYP3A4", "CYP2C9", "CYP1A2"],
        "pd_tags": ["serotonergic"],
        "description": "Herbal supplement. POTENT CYP3A4 inducer — reduces levels of many drugs including oral contraceptives, warfarin, statins."
    },
    "grapefruit": {
        "cid": 159278, "name": "Grapefruit Juice", "formula": "Furanocoumarins", "molecular_weight": 216.19,
        "class": "Food Interaction", "subclass": "CYP3A4 Inhibitor",
        "cyp_enzymes": [], "cyp_inhibits": ["CYP3A4"], "cyp_induces": [],
        "pd_tags": [],
        "description": "Grapefruit juice irreversibly inhibits intestinal CYP3A4. Affects 85+ drugs."
    },
}


# =============================================================================
# PART 2: CYP ENZYME DATABASE
# =============================================================================

CYP_ENZYMES = {
    "CYP3A4": {
        "name": "CYP3A4",
        "description": "Most abundant CYP enzyme, metabolizes ~50% of all drugs. Located primarily in liver and intestine.",
        "risk_note": "When multiple CYP3A4 substrates are combined with an inhibitor, drug levels can rise dangerously, increasing toxicity risk."
    },
    "CYP2D6": {
        "name": "CYP2D6",
        "description": "Metabolizes ~25% of drugs including beta-blockers, antidepressants, opioids, and antipsychotics.",
        "risk_note": "CYP2D6 poor metabolizers accumulate substrates. Inhibitors (e.g., fluoxetine, paroxetine) create phenocopy of poor metabolizer status."
    },
    "CYP2C9": {
        "name": "CYP2C9",
        "description": "Metabolizes ~15% of drugs including warfarin, NSAIDs, and sulfonylureas. Genetic polymorphisms common.",
        "risk_note": "CYP2C9 inhibition can cause warfarin toxicity leading to severe bleeding, and sulfonylurea hypoglycemia."
    },
    "CYP2C19": {
        "name": "CYP2C19",
        "description": "Metabolizes PPIs, clopidogrel, and some antidepressants. Highly polymorphic.",
        "risk_note": "CYP2C19 inhibition reduces clopidogrel activation, increasing cardiovascular event risk."
    },
    "CYP1A2": {
        "name": "CYP1A2",
        "description": "Metabolizes caffeine, theophylline, clozapine, olanzapine. Induced by smoking, cruciferous vegetables.",
        "risk_note": "CYP1A2 inhibition (by ciprofloxacin, fluvoxamine) causes dangerous accumulation of theophylline, clozapine, tizanidine."
    },
    "CYP2E1": {
        "name": "CYP2E1",
        "description": "Metabolizes acetaminophen to toxic NAPQI. Induced by chronic alcohol use and isoniazid.",
        "risk_note": "CYP2E1 induction increases NAPQI production, raising hepatotoxicity risk from acetaminophen."
    },
    "CYP2B6": {
        "name": "CYP2B6",
        "description": "Metabolizes bupropion, methadone, cyclophosphamide, and efavirenz.",
        "risk_note": "CYP2B6 polymorphisms affect methadone and bupropion metabolism significantly."
    },
    "CYP2C8": {
        "name": "CYP2C8",
        "description": "Metabolizes paclitaxel, pioglitazone, repaglinide. Less commonly involved in drug interactions.",
        "risk_note": "CYP2C8 inhibition increases pioglitazone and repaglinide levels."
    },
}

# =============================================================================
# PART 3: SIDE EFFECT CATALOG
# =============================================================================

SIDE_EFFECT_CATALOG = {
    "Gastrointestinal bleeding": {"organ": "gastrointestinal", "severity": "HIGH"},
    "GI ulceration": {"organ": "gastrointestinal", "severity": "HIGH"},
    "GI perforation": {"organ": "gastrointestinal", "severity": "HIGH"},
    "Nausea and vomiting": {"organ": "gastrointestinal", "severity": "LOW"},
    "Liver toxicity": {"organ": "liver", "severity": "HIGH"},
    "Hepatotoxicity": {"organ": "liver", "severity": "HIGH"},
    "Elevated liver enzymes": {"organ": "liver", "severity": "MEDIUM"},
    "Liver failure": {"organ": "liver", "severity": "HIGH"},
    "Rhabdomyolysis": {"organ": "muscle", "severity": "HIGH"},
    "Myopathy": {"organ": "muscle", "severity": "MEDIUM"},
    "Muscle weakness": {"organ": "muscle", "severity": "LOW"},
    "Acute kidney injury": {"organ": "kidney", "severity": "HIGH"},
    "Nephrotoxicity": {"organ": "kidney", "severity": "HIGH"},
    "Hyperkalemia": {"organ": "kidney", "severity": "HIGH"},
    "Hypokalemia": {"organ": "kidney", "severity": "MEDIUM"},
    "Hematuria": {"organ": "kidney", "severity": "MEDIUM"},
    "Electrolyte imbalance": {"organ": "kidney", "severity": "MEDIUM"},
    "Elevated INR": {"organ": "cardiovascular", "severity": "MEDIUM"},
    "Severe bleeding": {"organ": "cardiovascular", "severity": "HIGH"},
    "Hemorrhage": {"organ": "cardiovascular", "severity": "HIGH"},
    "Life-threatening hemorrhage": {"organ": "cardiovascular", "severity": "HIGH"},
    "Intracranial hemorrhage": {"organ": "neurological", "severity": "HIGH"},
    "Hemorrhagic stroke": {"organ": "neurological", "severity": "HIGH"},
    "Reduced antiplatelet effect": {"organ": "cardiovascular", "severity": "HIGH"},
    "Increased cardiovascular events": {"organ": "cardiovascular", "severity": "HIGH"},
    "Stent thrombosis": {"organ": "cardiovascular", "severity": "HIGH"},
    "Severe hypotension": {"organ": "cardiovascular", "severity": "HIGH"},
    "Hypotension": {"organ": "cardiovascular", "severity": "MEDIUM"},
    "Severe bradycardia": {"organ": "cardiovascular", "severity": "HIGH"},
    "Bradycardia": {"organ": "cardiovascular", "severity": "MEDIUM"},
    "Heart block": {"organ": "cardiovascular", "severity": "HIGH"},
    "QT prolongation": {"organ": "cardiovascular", "severity": "HIGH"},
    "Torsades de pointes": {"organ": "cardiovascular", "severity": "HIGH"},
    "Cardiac arrest": {"organ": "cardiovascular", "severity": "HIGH"},
    "Cardiac arrhythmia": {"organ": "cardiovascular", "severity": "HIGH"},
    "Bruising": {"organ": "skin", "severity": "LOW"},
    "Skin rash": {"organ": "skin", "severity": "LOW"},
    "Stevens-Johnson syndrome": {"organ": "skin", "severity": "HIGH"},
    "Hyperglycemia": {"organ": "metabolic", "severity": "MEDIUM"},
    "Severe hyperglycemia": {"organ": "metabolic", "severity": "HIGH"},
    "Hypoglycemia": {"organ": "metabolic", "severity": "MEDIUM"},
    "Severe hypoglycemia": {"organ": "metabolic", "severity": "HIGH"},
    "Lactic acidosis": {"organ": "metabolic", "severity": "HIGH"},
    "Metabolic acidosis": {"organ": "metabolic", "severity": "HIGH"},
    "Serotonin syndrome": {"organ": "neurological", "severity": "HIGH"},
    "Seizures": {"organ": "neurological", "severity": "HIGH"},
    "Respiratory depression": {"organ": "respiratory", "severity": "HIGH"},
    "CNS depression": {"organ": "neurological", "severity": "MEDIUM"},
    "Excessive sedation": {"organ": "neurological", "severity": "MEDIUM"},
    "Dizziness": {"organ": "neurological", "severity": "LOW"},
    "Fatigue": {"organ": "neurological", "severity": "LOW"},
    "Syncope": {"organ": "cardiovascular", "severity": "MEDIUM"},
    "Reduced drug efficacy": {"organ": "systemic", "severity": "HIGH"},
    "Therapeutic failure": {"organ": "systemic", "severity": "HIGH"},
    "Immunosuppression": {"organ": "immune", "severity": "MEDIUM"},
    "Myelosuppression": {"organ": "hematological", "severity": "HIGH"},
    "Agranulocytosis": {"organ": "hematological", "severity": "HIGH"},
    "Extrapyramidal symptoms": {"organ": "neurological", "severity": "MEDIUM"},
    "Tardive dyskinesia": {"organ": "neurological", "severity": "HIGH"},
    "Neuroleptic malignant syndrome": {"organ": "neurological", "severity": "HIGH"},
}

# =============================================================================
# PART 4: CURATED HIGH-CONFIDENCE INTERACTIONS
# =============================================================================
# These are well-documented, clinically significant interactions that override
# any programmatic generation.

CURATED_PAIRWISE = {
    # ─── Anticoagulant + NSAID (always HIGH) ─────────────────────────────
    "aspirin+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Gastrointestinal bleeding", "Intracranial hemorrhage", "Bruising"],
        "mechanism": "Both drugs inhibit hemostasis. Aspirin inhibits platelet aggregation via COX-1 while warfarin inhibits vitamin K-dependent clotting factors. Combined use synergistically increases bleeding risk.",
        "gap_hours": 12
    },
    "aspirin+ibuprofen": {
        "risk": "HIGH",
        "side_effects": ["GI ulceration", "Gastrointestinal bleeding", "Reduced antiplatelet effect"],
        "mechanism": "Ibuprofen competitively inhibits COX-1 binding, blocking aspirin's irreversible antiplatelet effect. Concurrent NSAID use dramatically increases GI bleeding risk.",
        "gap_hours": 8
    },
    "ibuprofen+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Severe bleeding", "Elevated INR", "Hematuria"],
        "mechanism": "Ibuprofen displaces warfarin from plasma protein binding and inhibits CYP2C9-mediated warfarin metabolism, increasing free warfarin concentration.",
        "gap_hours": 24
    },
    "diclofenac+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Gastrointestinal bleeding", "Elevated INR", "Hemorrhage"],
        "mechanism": "Diclofenac competes with warfarin for CYP2C9 metabolism. Combined with NSAID GI toxicity, creates severe bleeding risk.",
        "gap_hours": 24
    },
    "naproxen+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Gastrointestinal bleeding", "Elevated INR", "Hemorrhage"],
        "mechanism": "Naproxen inhibits platelet function and competes for CYP2C9 metabolism with warfarin. Long half-life prolongs interaction.",
        "gap_hours": 24
    },
    "ketorolac+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Life-threatening hemorrhage", "Gastrointestinal bleeding"],
        "mechanism": "Ketorolac is a potent COX inhibitor that dramatically increases bleeding risk with anticoagulants. Contraindicated combination.",
        "gap_hours": 48
    },
    "aspirin+apixaban": {
        "risk": "HIGH",
        "side_effects": ["Severe bleeding", "Gastrointestinal bleeding", "Intracranial hemorrhage"],
        "mechanism": "Aspirin adds antiplatelet effect to apixaban's anticoagulation. Increases major bleeding risk by 60-70% compared to apixaban alone.",
        "gap_hours": 12
    },
    "aspirin+rivaroxaban": {
        "risk": "HIGH",
        "side_effects": ["Severe bleeding", "Gastrointestinal bleeding"],
        "mechanism": "Dual anticoagulant/antiplatelet increases bleeding risk significantly. Only justified in specific high-thrombotic-risk scenarios.",
        "gap_hours": 12
    },
    "ibuprofen+apixaban": {
        "risk": "HIGH",
        "side_effects": ["Gastrointestinal bleeding", "Severe bleeding"],
        "mechanism": "NSAIDs increase GI bleeding risk and reduce renal function, affecting apixaban clearance.",
        "gap_hours": 12
    },
    "ibuprofen+rivaroxaban": {
        "risk": "HIGH",
        "side_effects": ["Gastrointestinal bleeding", "Severe bleeding"],
        "mechanism": "NSAIDs increase GI bleeding risk and reduce renal function, affecting rivaroxaban clearance.",
        "gap_hours": 12
    },

    # ─── Warfarin + CYP inhibitors ───────────────────────────────────────
    "fluconazole+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Elevated INR", "Severe bleeding", "Hemorrhage"],
        "mechanism": "Fluconazole potently inhibits CYP2C9, dramatically reducing warfarin clearance. Can cause 2-3x increase in warfarin levels.",
        "gap_hours": 48
    },
    "ciprofloxacin+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Elevated INR", "Severe bleeding", "Hemorrhage"],
        "mechanism": "Ciprofloxacin inhibits CYP1A2-mediated warfarin metabolism AND kills vitamin K-producing gut flora, amplifying anticoagulant effect.",
        "gap_hours": 12
    },
    "metronidazole+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Elevated INR", "Severe bleeding"],
        "mechanism": "Metronidazole inhibits CYP2C9, reducing warfarin clearance. Well-documented cause of supratherapeutic INR.",
        "gap_hours": 12
    },
    "sulfamethoxazole+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Elevated INR", "Severe bleeding", "Hemorrhage"],
        "mechanism": "Sulfamethoxazole inhibits CYP2C9 and displaces warfarin from protein binding. One of the most common causes of warfarin toxicity.",
        "gap_hours": 12
    },
    "fluvoxamine+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Elevated INR", "Severe bleeding"],
        "mechanism": "Fluvoxamine potently inhibits CYP1A2 and CYP2C19, both involved in warfarin metabolism. Also SSRIs impair platelet function.",
        "gap_hours": 24
    },
    "amiodarone+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Elevated INR", "Hemorrhage", "Life-threatening hemorrhage"],
        "mechanism": "Amiodarone inhibits CYP2C9 and CYP3A4, reducing warfarin metabolism. Effect persists for weeks after amiodarone discontinuation due to extremely long half-life.",
        "gap_hours": 24
    },

    # ─── Statin + CYP3A4 inhibitors (rhabdomyolysis risk) ───────────────
    "simvastatin+fluconazole": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury", "Liver failure"],
        "mechanism": "Fluconazole potently inhibits CYP3A4 causing massive simvastatin accumulation. CONTRAINDICATED combination.",
        "gap_hours": 48
    },
    "simvastatin+itraconazole": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury", "Liver failure"],
        "mechanism": "Itraconazole is a potent CYP3A4 inhibitor. Simvastatin levels increase 10-20x. CONTRAINDICATED.",
        "gap_hours": 72
    },
    "simvastatin+ketoconazole": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury"],
        "mechanism": "Ketoconazole is the strongest CYP3A4 inhibitor. CONTRAINDICATED with simvastatin.",
        "gap_hours": 72
    },
    "simvastatin+erythromycin": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Myopathy"],
        "mechanism": "Erythromycin inhibits CYP3A4, increasing simvastatin levels. Use pravastatin or rosuvastatin instead.",
        "gap_hours": 24
    },
    "simvastatin+clarithromycin": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Myopathy", "Acute kidney injury"],
        "mechanism": "Clarithromycin strongly inhibits CYP3A4. CONTRAINDICATED with simvastatin/lovastatin.",
        "gap_hours": 48
    },
    "simvastatin+verapamil": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Myopathy"],
        "mechanism": "Verapamil inhibits CYP3A4. FDA limits simvastatin to 10mg with verapamil.",
        "gap_hours": 12
    },
    "simvastatin+diltiazem": {
        "risk": "MEDIUM",
        "side_effects": ["Myopathy", "Rhabdomyolysis"],
        "mechanism": "Diltiazem moderately inhibits CYP3A4. FDA limits simvastatin to 10mg with diltiazem.",
        "gap_hours": 12
    },
    "simvastatin+amlodipine": {
        "risk": "MEDIUM",
        "side_effects": ["Myopathy", "Rhabdomyolysis"],
        "mechanism": "Amlodipine weakly inhibits CYP3A4. FDA limits simvastatin to 20mg with amlodipine.",
        "gap_hours": 12
    },
    "simvastatin+ritonavir": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury", "Liver failure"],
        "mechanism": "Ritonavir is the most potent CYP3A4 inhibitor known. CONTRAINDICATED with simvastatin/lovastatin.",
        "gap_hours": 72
    },
    "lovastatin+itraconazole": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury"],
        "mechanism": "Lovastatin extensively CYP3A4-metabolized. CONTRAINDICATED with strong CYP3A4 inhibitors.",
        "gap_hours": 72
    },
    "lovastatin+erythromycin": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Myopathy"],
        "mechanism": "Erythromycin inhibits CYP3A4, increasing lovastatin exposure dangerously.",
        "gap_hours": 24
    },
    "atorvastatin+fluconazole": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Myopathy", "Liver toxicity"],
        "mechanism": "Fluconazole inhibits CYP3A4 which metabolizes atorvastatin, causing statin accumulation and risk of severe muscle breakdown.",
        "gap_hours": 24
    },
    "atorvastatin+clarithromycin": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Myopathy"],
        "mechanism": "Clarithromycin inhibits CYP3A4, increasing atorvastatin levels. Use azithromycin or pravastatin instead.",
        "gap_hours": 24
    },
    "atorvastatin+ritonavir": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury"],
        "mechanism": "Ritonavir massively inhibits CYP3A4. Use lowest dose atorvastatin or switch to pravastatin/rosuvastatin.",
        "gap_hours": 48
    },

    # ─── Clopidogrel + PPI (reduced efficacy) ────────────────────────────
    "clopidogrel+omeprazole": {
        "risk": "HIGH",
        "side_effects": ["Reduced antiplatelet effect", "Increased cardiovascular events", "Stent thrombosis"],
        "mechanism": "Omeprazole inhibits CYP2C19 required to convert clopidogrel (prodrug) to active metabolite. Reduces antiplatelet efficacy by 40-50%.",
        "gap_hours": 12
    },
    "clopidogrel+esomeprazole": {
        "risk": "HIGH",
        "side_effects": ["Reduced antiplatelet effect", "Increased cardiovascular events"],
        "mechanism": "Esomeprazole inhibits CYP2C19 similarly to omeprazole, reducing clopidogrel activation.",
        "gap_hours": 12
    },

    # ─── Dual RAAS Blockade ──────────────────────────────────────────────
    "lisinopril+losartan": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Acute kidney injury", "Severe hypotension"],
        "mechanism": "Dual RAAS blockade (ACE inhibitor + ARB) causes excessive aldosterone suppression, leading to dangerous potassium elevation and renal failure.",
        "gap_hours": 24
    },
    "enalapril+valsartan": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Acute kidney injury", "Severe hypotension"],
        "mechanism": "Dual RAAS blockade with ACE inhibitor + ARB is generally contraindicated. Risk of hyperkalemia and renal failure.",
        "gap_hours": 24
    },
    "lisinopril+valsartan": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Acute kidney injury", "Severe hypotension"],
        "mechanism": "Dual RAAS blockade generally contraindicated. Additive hyperkalemia and hypotension.",
        "gap_hours": 24
    },
    "ramipril+losartan": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Acute kidney injury"],
        "mechanism": "Dual RAAS blockade with ACE inhibitor + ARB.",
        "gap_hours": 24
    },

    # ─── ACE/ARB + K-sparing diuretic (hyperkalemia) ────────────────────
    "lisinopril+spironolactone": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Cardiac arrhythmia"],
        "mechanism": "Both increase serum potassium. ACE inhibitor reduces aldosterone, spironolactone blocks aldosterone receptor. Combined hyperkalemia risk, especially with renal impairment.",
        "gap_hours": 12
    },
    "enalapril+spironolactone": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Cardiac arrhythmia"],
        "mechanism": "ACE inhibitor + aldosterone antagonist = additive hyperkalemia risk.",
        "gap_hours": 12
    },
    "losartan+spironolactone": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Cardiac arrhythmia"],
        "mechanism": "ARB + aldosterone antagonist = additive hyperkalemia, especially in renal impairment.",
        "gap_hours": 12
    },
    "lisinopril+trimethoprim": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Cardiac arrest"],
        "mechanism": "Trimethoprim blocks renal potassium excretion. Combined with ACE inhibitor's potassium-sparing effect, can cause fatal hyperkalemia.",
        "gap_hours": 12
    },

    # ─── NSAID + ACE/ARB + Diuretic (triple whammy) ─────────────────────
    "ibuprofen+lisinopril": {
        "risk": "MEDIUM",
        "side_effects": ["Acute kidney injury", "Reduced drug efficacy", "Hyperkalemia"],
        "mechanism": "NSAIDs reduce renal prostaglandin-mediated blood flow, opposing ACE inhibitor effect and increasing nephrotoxicity risk.",
        "gap_hours": 8
    },
    "diclofenac+lisinopril": {
        "risk": "MEDIUM",
        "side_effects": ["Acute kidney injury", "Reduced drug efficacy"],
        "mechanism": "NSAID opposes ACE inhibitor's renal protective effect and reduces antihypertensive efficacy.",
        "gap_hours": 8
    },
    "ibuprofen+losartan": {
        "risk": "MEDIUM",
        "side_effects": ["Acute kidney injury", "Reduced drug efficacy"],
        "mechanism": "NSAIDs reduce renal blood flow, opposing ARB renoprotective effect.",
        "gap_hours": 8
    },

    # ─── NSAID + Lithium ─────────────────────────────────────────────────
    "ibuprofen+lithium": {
        "risk": "HIGH",
        "side_effects": ["Lithium toxicity", "Seizures", "Cardiac arrhythmia"],
        "mechanism": "NSAIDs reduce renal lithium clearance by 15-25%, causing accumulation to toxic levels. All NSAIDs except aspirin increase lithium levels.",
        "gap_hours": 24
    },
    "naproxen+lithium": {
        "risk": "HIGH",
        "side_effects": ["Lithium toxicity", "Seizures"],
        "mechanism": "Naproxen reduces renal lithium clearance. Monitor lithium levels if NSAID unavoidable.",
        "gap_hours": 24
    },
    "diclofenac+lithium": {
        "risk": "HIGH",
        "side_effects": ["Lithium toxicity", "Seizures"],
        "mechanism": "Diclofenac reduces renal elimination of lithium.",
        "gap_hours": 24
    },

    # ─── Serotonin Syndrome combos ───────────────────────────────────────
    "fluoxetine+tramadol": {
        "risk": "HIGH",
        "side_effects": ["Serotonin syndrome", "Seizures"],
        "mechanism": "Both drugs increase serotonin. Fluoxetine inhibits CYP2D6 (increasing tramadol levels) AND both have serotonergic activity. Dual risk of serotonin syndrome.",
        "gap_hours": 24
    },
    "sertraline+tramadol": {
        "risk": "HIGH",
        "side_effects": ["Serotonin syndrome", "Seizures"],
        "mechanism": "SSRI + tramadol = serotonin syndrome risk from combined serotonergic activity.",
        "gap_hours": 24
    },
    "fluoxetine+linezolid": {
        "risk": "HIGH",
        "side_effects": ["Serotonin syndrome"],
        "mechanism": "Linezolid has weak MAOI activity. Combined with SSRI creates severe serotonin syndrome risk. CONTRAINDICATED.",
        "gap_hours": 48
    },
    "sertraline+linezolid": {
        "risk": "HIGH",
        "side_effects": ["Serotonin syndrome"],
        "mechanism": "Linezolid MAOI activity + SSRI = serotonin syndrome. CONTRAINDICATED.",
        "gap_hours": 48
    },

    # ─── Opioid + Benzodiazepine (FDA Black Box) ────────────────────────
    "oxycodone+alprazolam": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "CNS depression", "Cardiac arrest"],
        "mechanism": "FDA Black Box Warning: Combined opioid + benzodiazepine causes profound CNS and respiratory depression. Leading cause of overdose death.",
        "gap_hours": 24
    },
    "fentanyl+alprazolam": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "CNS depression", "Cardiac arrest"],
        "mechanism": "Fentanyl + benzodiazepine is extremely dangerous. Potent synergistic respiratory depression.",
        "gap_hours": 24
    },
    "oxycodone+diazepam": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "CNS depression"],
        "mechanism": "Opioid + benzodiazepine combination causes additive CNS/respiratory depression. FDA Black Box.",
        "gap_hours": 24
    },
    "hydrocodone+alprazolam": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "CNS depression"],
        "mechanism": "Opioid + benzodiazepine = FDA Black Box for respiratory depression risk.",
        "gap_hours": 24
    },
    "methadone+diazepam": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "QT prolongation", "Cardiac arrest"],
        "mechanism": "Methadone + benzodiazepine: additive respiratory depression AND both prolong QT interval.",
        "gap_hours": 24
    },
    "morphine+midazolam": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "Excessive sedation"],
        "mechanism": "Potent opioid + short-acting benzodiazepine. Rapid-onset respiratory depression.",
        "gap_hours": 12
    },
    "tramadol+alprazolam": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "Seizures", "Serotonin syndrome"],
        "mechanism": "Tramadol + benzodiazepine: CNS depression + tramadol lowers seizure threshold.",
        "gap_hours": 12
    },

    # ─── CYP3A4 inhibitors + fentanyl/oxycodone (fatal) ─────────────────
    "fentanyl+ritonavir": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "Cardiac arrest"],
        "mechanism": "Ritonavir potently inhibits CYP3A4, causing massive fentanyl accumulation. POTENTIALLY FATAL.",
        "gap_hours": 72
    },
    "fentanyl+itraconazole": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "Excessive sedation"],
        "mechanism": "Itraconazole inhibits CYP3A4, increasing fentanyl levels dangerously.",
        "gap_hours": 48
    },
    "fentanyl+ketoconazole": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "Cardiac arrest"],
        "mechanism": "Ketoconazole strongly inhibits CYP3A4, causing fentanyl accumulation.",
        "gap_hours": 48
    },
    "fentanyl+clarithromycin": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "CNS depression"],
        "mechanism": "Clarithromycin inhibits CYP3A4, increasing fentanyl exposure.",
        "gap_hours": 24
    },
    "oxycodone+itraconazole": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "CNS depression"],
        "mechanism": "Itraconazole inhibits CYP3A4, increasing oxycodone exposure 2-3x.",
        "gap_hours": 24
    },

    # ─── QT Prolongation combinations ────────────────────────────────────
    "amiodarone+moxifloxacin": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes", "Cardiac arrest"],
        "mechanism": "Both drugs independently prolong QT. Combined effect is additive/synergistic. Risk of fatal torsades de pointes.",
        "gap_hours": 48
    },
    "amiodarone+haloperidol": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes"],
        "mechanism": "Dual QT-prolonging agents. Amiodarone also inhibits CYP2D6, increasing haloperidol levels.",
        "gap_hours": 24
    },
    "sotalol+moxifloxacin": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes", "Cardiac arrest"],
        "mechanism": "Both prolong QT interval. Sotalol's beta-blocking causes bradycardia which further increases TdP risk.",
        "gap_hours": 48
    },
    "citalopram+moxifloxacin": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes"],
        "mechanism": "Both drugs prolong QT interval dose-dependently. Combined use significantly increases arrhythmia risk.",
        "gap_hours": 24
    },
    "methadone+moxifloxacin": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes", "Cardiac arrest"],
        "mechanism": "Both prolong QT. Methadone is one of the most common drug causes of TdP.",
        "gap_hours": 24
    },
    "ziprasidone+amiodarone": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes"],
        "mechanism": "Ziprasidone has highest QT risk among atypical antipsychotics. CONTRAINDICATED with amiodarone.",
        "gap_hours": 48
    },
    "ondansetron+amiodarone": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes"],
        "mechanism": "Both prolong QT interval. Use metoclopramide or granisetron as alternative antiemetic.",
        "gap_hours": 24
    },

    # ─── CYP1A2 substrate + inhibitor (dangerous) ──────────────────────
    "tizanidine+ciprofloxacin": {
        "risk": "HIGH",
        "side_effects": ["Severe hypotension", "Excessive sedation", "Bradycardia"],
        "mechanism": "Ciprofloxacin potently inhibits CYP1A2, increasing tizanidine levels 10x. CONTRAINDICATED.",
        "gap_hours": 48
    },
    "tizanidine+fluvoxamine": {
        "risk": "HIGH",
        "side_effects": ["Severe hypotension", "Excessive sedation"],
        "mechanism": "Fluvoxamine potently inhibits CYP1A2, increasing tizanidine levels 33x. CONTRAINDICATED.",
        "gap_hours": 48
    },
    "theophylline+ciprofloxacin": {
        "risk": "HIGH",
        "side_effects": ["Seizures", "Cardiac arrhythmia", "Nausea and vomiting"],
        "mechanism": "Ciprofloxacin inhibits CYP1A2, increasing theophylline levels 20-100%. Narrow TI drug — can cause seizures.",
        "gap_hours": 24
    },
    "theophylline+fluvoxamine": {
        "risk": "HIGH",
        "side_effects": ["Seizures", "Cardiac arrhythmia"],
        "mechanism": "Fluvoxamine potently inhibits CYP1A2, increasing theophylline levels 3x. CONTRAINDICATED.",
        "gap_hours": 48
    },
    "clozapine+ciprofloxacin": {
        "risk": "HIGH",
        "side_effects": ["Seizures", "Excessive sedation", "Agranulocytosis"],
        "mechanism": "Ciprofloxacin inhibits CYP1A2, increasing clozapine levels significantly. Monitor clozapine levels closely.",
        "gap_hours": 24
    },
    "clozapine+fluvoxamine": {
        "risk": "HIGH",
        "side_effects": ["Seizures", "Excessive sedation", "Neuroleptic malignant syndrome"],
        "mechanism": "Fluvoxamine potently inhibits CYP1A2, increasing clozapine levels 5-10x. Dose reduction required.",
        "gap_hours": 48
    },

    # ─── Tamoxifen + CYP2D6 inhibitors (reduced efficacy) ───────────────
    "tamoxifen+fluoxetine": {
        "risk": "HIGH",
        "side_effects": ["Reduced drug efficacy", "Therapeutic failure"],
        "mechanism": "Fluoxetine potently inhibits CYP2D6, preventing tamoxifen conversion to active endoxifen. Reduces breast cancer treatment efficacy by 50-75%.",
        "gap_hours": 48
    },
    "tamoxifen+paroxetine": {
        "risk": "HIGH",
        "side_effects": ["Reduced drug efficacy", "Therapeutic failure"],
        "mechanism": "Paroxetine is the strongest CYP2D6 inhibitor. Reduces tamoxifen activation to endoxifen. CONTRAINDICATED.",
        "gap_hours": 48
    },
    "tamoxifen+bupropion": {
        "risk": "MEDIUM",
        "side_effects": ["Reduced drug efficacy"],
        "mechanism": "Bupropion moderately inhibits CYP2D6, partially reducing tamoxifen activation.",
        "gap_hours": 12
    },

    # ─── Colchicine + CYP3A4 inhibitors (fatal) ─────────────────────────
    "colchicine+clarithromycin": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Acute kidney injury", "Liver failure"],
        "mechanism": "Clarithromycin inhibits CYP3A4 + P-glycoprotein, causing fatal colchicine accumulation. Multiple documented deaths.",
        "gap_hours": 72
    },
    "colchicine+itraconazole": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Acute kidney injury"],
        "mechanism": "Dual CYP3A4 and P-gp inhibition causes colchicine toxicity. CONTRAINDICATED in renal/hepatic impairment.",
        "gap_hours": 72
    },
    "colchicine+ritonavir": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Acute kidney injury", "Liver failure"],
        "mechanism": "Ritonavir potently inhibits CYP3A4, causing fatal colchicine accumulation. CONTRAINDICATED.",
        "gap_hours": 72
    },

    # ─── Azathioprine + Allopurinol (fatal myelosuppression) ─────────────
    "azathioprine+allopurinol": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Agranulocytosis", "Life-threatening hemorrhage"],
        "mechanism": "Allopurinol inhibits xanthine oxidase, blocking azathioprine metabolism. Causes 3-5x increase in active metabolite. Requires 75% dose reduction if unavoidable.",
        "gap_hours": 24
    },

    # ─── Methotrexate + NSAIDs (nephrotoxicity) ──────────────────────────
    "methotrexate+ibuprofen": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Nephrotoxicity", "Liver toxicity"],
        "mechanism": "NSAIDs reduce renal clearance of methotrexate, causing toxic accumulation. Particularly dangerous with high-dose methotrexate.",
        "gap_hours": 24
    },
    "methotrexate+naproxen": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Nephrotoxicity"],
        "mechanism": "Naproxen reduces renal methotrexate clearance. Long NSAID half-life prolongs interaction.",
        "gap_hours": 24
    },
    "methotrexate+diclofenac": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Nephrotoxicity"],
        "mechanism": "Diclofenac reduces renal methotrexate clearance.",
        "gap_hours": 24
    },
    "methotrexate+trimethoprim": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Agranulocytosis"],
        "mechanism": "Both are folate antagonists. Combined antifolate effect causes severe bone marrow suppression.",
        "gap_hours": 48
    },

    # ─── Rifampin (inducer) interactions ─────────────────────────────────
    "rifampin+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Reduced drug efficacy"],
        "mechanism": "Rifampin is the most potent CYP inducer, increasing warfarin metabolism 3-5x. INR drops dramatically. Requires 2-3x warfarin dose increase.",
        "gap_hours": 24
    },
    "rifampin+simvastatin": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Reduced drug efficacy"],
        "mechanism": "Rifampin induces CYP3A4, reducing simvastatin levels by 87%. Statin therapy becomes ineffective.",
        "gap_hours": 24
    },
    "rifampin+clopidogrel": {
        "risk": "MEDIUM",
        "side_effects": ["Increased bleeding risk"],
        "mechanism": "Rifampin induces CYP2C19, increasing clopidogrel activation. Paradoxically increases antiplatelet effect.",
        "gap_hours": 12
    },
    "rifampin+apixaban": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Increased cardiovascular events"],
        "mechanism": "Rifampin induces CYP3A4, reducing apixaban levels by 54%. Anticoagulation becomes inadequate.",
        "gap_hours": 24
    },
    "rifampin+rivaroxaban": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Increased cardiovascular events"],
        "mechanism": "Rifampin induces CYP3A4, reducing rivaroxaban levels by 50%.",
        "gap_hours": 24
    },
    "rifampin+tacrolimus": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Organ rejection"],
        "mechanism": "Rifampin induces CYP3A4, reducing tacrolimus levels dramatically. Risk of transplant rejection.",
        "gap_hours": 24
    },
    "rifampin+cyclosporine": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Organ rejection"],
        "mechanism": "Rifampin reduces cyclosporine levels by 70-80%. CONTRAINDICATED in transplant patients.",
        "gap_hours": 24
    },

    # ─── St. John's Wort (inducer) ──────────────────────────────────────
    "st_johns_wort+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Reduced drug efficacy"],
        "mechanism": "St. John's Wort induces CYP3A4 and CYP2C9, increasing warfarin metabolism. Documented cases of sub-therapeutic INR.",
        "gap_hours": 24
    },
    "st_johns_wort+cyclosporine": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Organ rejection"],
        "mechanism": "St. John's Wort potently induces CYP3A4, reducing cyclosporine levels. Documented transplant rejections.",
        "gap_hours": 24
    },
    "st_johns_wort+simvastatin": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure"],
        "mechanism": "St. John's Wort induces CYP3A4, reducing statin efficacy.",
        "gap_hours": 24
    },

    # ─── Digoxin interactions ────────────────────────────────────────────
    "digoxin+amiodarone": {
        "risk": "HIGH",
        "side_effects": ["Cardiac arrhythmia", "Bradycardia", "Cardiac arrest"],
        "mechanism": "Amiodarone increases digoxin levels by 70-100% via P-gp inhibition. Also additive bradycardia. Reduce digoxin dose by 50%.",
        "gap_hours": 24
    },
    "digoxin+verapamil": {
        "risk": "HIGH",
        "side_effects": ["Cardiac arrhythmia", "Severe bradycardia", "Heart block"],
        "mechanism": "Verapamil inhibits P-gp, increasing digoxin levels 50-75%. Combined AV nodal depression causes heart block.",
        "gap_hours": 12
    },
    "digoxin+furosemide": {
        "risk": "HIGH",
        "side_effects": ["Cardiac arrhythmia", "Cardiac arrest"],
        "mechanism": "Furosemide causes hypokalemia/hypomagnesemia, dramatically increasing digoxin toxicity risk. Must monitor electrolytes.",
        "gap_hours": 4
    },
    "digoxin+hydrochlorothiazide": {
        "risk": "MEDIUM",
        "side_effects": ["Cardiac arrhythmia", "Hypokalemia"],
        "mechanism": "Thiazide diuretics cause potassium loss, increasing digoxin toxicity risk.",
        "gap_hours": 4
    },

    # ─── Beta-blocker + Non-DHP CCB (heart block) ────────────────────────
    "metoprolol+verapamil": {
        "risk": "HIGH",
        "side_effects": ["Severe bradycardia", "Heart block", "Cardiac arrest"],
        "mechanism": "Both drugs slow AV conduction and heart rate. Combined use can cause complete heart block. IV combination is CONTRAINDICATED.",
        "gap_hours": 12
    },
    "metoprolol+diltiazem": {
        "risk": "HIGH",
        "side_effects": ["Severe bradycardia", "Heart block", "Severe hypotension"],
        "mechanism": "Additive negative chronotropic and dromotropic effects. Risk of heart block, especially in elderly.",
        "gap_hours": 12
    },
    "atenolol+verapamil": {
        "risk": "HIGH",
        "side_effects": ["Severe bradycardia", "Heart block"],
        "mechanism": "Beta-blocker + non-DHP CCB = additive AV nodal depression.",
        "gap_hours": 12
    },
    "propranolol+verapamil": {
        "risk": "HIGH",
        "side_effects": ["Severe bradycardia", "Heart block", "Cardiac arrest"],
        "mechanism": "Non-selective beta-blocker + verapamil = highest risk of complete heart block.",
        "gap_hours": 12
    },

    # ─── SSRI + NSAID (bleeding) ─────────────────────────────────────────
    "fluoxetine+ibuprofen": {
        "risk": "MEDIUM",
        "side_effects": ["Gastrointestinal bleeding", "Bruising"],
        "mechanism": "SSRIs impair platelet serotonin uptake. Combined with NSAID COX inhibition, GI bleeding risk increases 6-15x.",
        "gap_hours": 4
    },
    "sertraline+naproxen": {
        "risk": "MEDIUM",
        "side_effects": ["Gastrointestinal bleeding", "Bruising"],
        "mechanism": "SSRI + NSAID combination significantly increases GI bleeding risk.",
        "gap_hours": 4
    },
    "fluoxetine+aspirin": {
        "risk": "MEDIUM",
        "side_effects": ["Gastrointestinal bleeding", "Bruising"],
        "mechanism": "SSRI impairs platelet function, adding to aspirin's antiplatelet effect.",
        "gap_hours": 4
    },

    # ─── Miscellaneous important interactions ────────────────────────────
    "metformin+furosemide": {
        "risk": "MEDIUM",
        "side_effects": ["Lactic acidosis", "Hyperglycemia"],
        "mechanism": "Loop diuretics can cause dehydration and renal impairment, increasing metformin accumulation and lactic acidosis risk.",
        "gap_hours": 4
    },
    "prednisone+aspirin": {
        "risk": "MEDIUM",
        "side_effects": ["GI ulceration", "Gastrointestinal bleeding"],
        "mechanism": "Corticosteroids reduce gastric mucosal protection while aspirin inhibits COX-mediated prostaglandin synthesis. Synergistic GI toxicity.",
        "gap_hours": 4
    },
    "prednisone+metformin": {
        "risk": "MEDIUM",
        "side_effects": ["Severe hyperglycemia"],
        "mechanism": "Corticosteroids increase hepatic gluconeogenesis and induce insulin resistance, directly opposing metformin.",
        "gap_hours": 4
    },
    "acetaminophen+warfarin": {
        "risk": "MEDIUM",
        "side_effects": ["Elevated INR", "Increased bleeding risk"],
        "mechanism": "Acetaminophen metabolite interferes with vitamin K cycle. Risk increases above 2g/day for 3+ days.",
        "gap_hours": 6
    },
    "metoprolol+amlodipine": {
        "risk": "MEDIUM",
        "side_effects": ["Severe bradycardia", "Hypotension"],
        "mechanism": "Both reduce heart rate and blood pressure. Additive cardiodepressant effect.",
        "gap_hours": 6
    },
    "metformin+hydrochlorothiazide": {
        "risk": "MEDIUM",
        "side_effects": ["Hyperglycemia", "Lactic acidosis"],
        "mechanism": "Thiazides increase blood glucose, opposing metformin. Dehydration increases lactic acidosis risk.",
        "gap_hours": 4
    },
    "lisinopril+hydrochlorothiazide": {
        "risk": "LOW",
        "side_effects": ["Electrolyte imbalance", "Dizziness"],
        "mechanism": "Common safe combination. HCTZ offsets hyperkalemia from lisinopril. Monitor electrolytes.",
        "gap_hours": 0
    },
    "aspirin+clopidogrel": {
        "risk": "MEDIUM",
        "side_effects": ["Severe bleeding", "Bruising"],
        "mechanism": "Dual antiplatelet therapy — synergistic bleeding risk. Therapeutic benefit in ACS but increases major bleeding.",
        "gap_hours": 0
    },
    "gabapentin+metoprolol": {
        "risk": "LOW",
        "side_effects": ["Dizziness", "Fatigue"],
        "mechanism": "Additive CNS depression. Both can cause dizziness. No significant pharmacokinetic interaction.",
        "gap_hours": 0
    },
    "atorvastatin+omeprazole": {
        "risk": "LOW",
        "side_effects": ["Elevated liver enzymes"],
        "mechanism": "Omeprazole weakly inhibits CYP3A4. Usually clinically insignificant.",
        "gap_hours": 2
    },
    "atorvastatin+amlodipine": {
        "risk": "LOW",
        "side_effects": ["Elevated liver enzymes"],
        "mechanism": "Amlodipine weakly inhibits CYP3A4. FDA allows full-dose atorvastatin with amlodipine.",
        "gap_hours": 0
    },
    "metformin+lisinopril": {
        "risk": "LOW",
        "side_effects": ["Hypoglycemia", "Dizziness"],
        "mechanism": "ACE inhibitors may enhance insulin sensitivity. Generally safe combination.",
        "gap_hours": 0
    },
    "ciprofloxacin+acetaminophen": {
        "risk": "LOW",
        "side_effects": ["Elevated liver enzymes"],
        "mechanism": "Ciprofloxacin inhibits CYP1A2, slightly reducing acetaminophen metabolism.",
        "gap_hours": 2
    },
}


# =============================================================================
# PART 5: CURATED HIGHER-ORDER INTERACTIONS
# =============================================================================

CURATED_HIGHER_ORDER = {
    "aspirin+ibuprofen+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Life-threatening hemorrhage", "Intracranial hemorrhage", "Hemorrhagic stroke"],
        "mechanism": "Triple threat: aspirin + ibuprofen provide dual COX inhibition destroying GI mucosal protection, while warfarin prevents clot formation. All three compete for CYP2C9 metabolism. This combination has caused documented fatalities.",
        "confidence": 0.95
    },
    "aspirin+fluconazole+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Life-threatening hemorrhage", "Hemorrhagic stroke"],
        "mechanism": "Fluconazole potently inhibits CYP2C9, causing 2-3x warfarin accumulation. Aspirin adds antiplatelet effect. Triple combination creates extreme uncontrollable bleeding risk.",
        "confidence": 0.97
    },
    "amlodipine+fluconazole+simvastatin": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury", "Hepatotoxicity"],
        "mechanism": "Both amlodipine and fluconazole inhibit CYP3A4. Dual CYP3A4 inhibition causes massive simvastatin accumulation leading to muscle breakdown and kidney damage.",
        "confidence": 0.93
    },
    "aspirin+clopidogrel+omeprazole": {
        "risk": "HIGH",
        "side_effects": ["Increased cardiovascular events", "Stent thrombosis"],
        "mechanism": "Omeprazole inhibits CYP2C19-mediated clopidogrel activation. With reduced antiplatelet protection, patients on DAPT face increased cardiovascular event risk.",
        "confidence": 0.88
    },
    "hydrochlorothiazide+lisinopril+losartan": {
        "risk": "HIGH",
        "side_effects": ["Hyperkalemia", "Cardiac arrest", "Acute kidney injury"],
        "mechanism": "Dual RAAS blockade (ACE + ARB) with diuretic causes unpredictable electrolyte shifts. Severe hyperkalemia can cause fatal cardiac arrhythmias.",
        "confidence": 0.90
    },
    "aspirin+ibuprofen+prednisone": {
        "risk": "HIGH",
        "side_effects": ["GI perforation", "Life-threatening hemorrhage"],
        "mechanism": "Triple assault on GI mucosa: prednisone reduces mucosal defense, aspirin and ibuprofen inhibit protective prostaglandins. GI perforation risk dramatically elevated.",
        "confidence": 0.92
    },
    "aspirin+ciprofloxacin+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Life-threatening hemorrhage", "Gastrointestinal bleeding"],
        "mechanism": "Ciprofloxacin inhibits CYP1A2-mediated warfarin metabolism AND kills vitamin K gut bacteria. Combined with aspirin's antiplatelet effect, extreme bleeding risk.",
        "confidence": 0.91
    },
    "hydrochlorothiazide+metformin+prednisone": {
        "risk": "MEDIUM",
        "side_effects": ["Severe hyperglycemia", "Lactic acidosis"],
        "mechanism": "Both prednisone and HCTZ oppose metformin. Triple combination can cause loss of glycemic control.",
        "confidence": 0.85
    },
    "acetaminophen+ciprofloxacin+warfarin": {
        "risk": "HIGH",
        "side_effects": ["Elevated INR", "Hemorrhage", "Hepatotoxicity"],
        "mechanism": "Ciprofloxacin inhibits CYP1A2, acetaminophen interferes with vitamin K cycle. Triple hepatic stress with anticoagulation amplification.",
        "confidence": 0.88
    },
    "amlodipine+atorvastatin+omeprazole": {
        "risk": "MEDIUM",
        "side_effects": ["Myopathy", "Elevated liver enzymes"],
        "mechanism": "Multiple weak CYP3A4 inhibitors combined can have additive effect on atorvastatin metabolism.",
        "confidence": 0.75
    },
    "amlodipine+lisinopril+metoprolol": {
        "risk": "MEDIUM",
        "side_effects": ["Severe hypotension", "Syncope", "Bradycardia"],
        "mechanism": "Triple antihypertensive therapy: CCB + ACE inhibitor + beta-blocker. Additive hypotensive effect.",
        "confidence": 0.80
    },
    "diclofenac+lisinopril+metformin": {
        "risk": "MEDIUM",
        "side_effects": ["Acute kidney injury", "Hyperkalemia"],
        "mechanism": "NSAID reduces renal blood flow, impairing lisinopril efficacy and metformin clearance.",
        "confidence": 0.82
    },
    # ── Opioid + Benzo + SSRI (triple CNS) ───────────────────────────
    "alprazolam+fluoxetine+oxycodone": {
        "risk": "HIGH",
        "side_effects": ["Respiratory depression", "Serotonin syndrome", "Cardiac arrest"],
        "mechanism": "Opioid + benzodiazepine = respiratory depression (FDA Black Box). Fluoxetine inhibits CYP2D6, increasing oxycodone levels. Also serotonergic effects compound risk.",
        "confidence": 0.94
    },
    # ── Multiple QT prolongers ───────────────────────────────────────
    "amiodarone+haloperidol+moxifloxacin": {
        "risk": "HIGH",
        "side_effects": ["QT prolongation", "Torsades de pointes", "Cardiac arrest"],
        "mechanism": "Three drugs that all prolong QT interval. Synergistic QT prolongation creates extreme risk of fatal torsades de pointes.",
        "confidence": 0.96
    },
    # ── NSAID + ACE + Diuretic (triple whammy) ───────────────────────
    "furosemide+ibuprofen+lisinopril": {
        "risk": "HIGH",
        "side_effects": ["Acute kidney injury", "Hyperkalemia", "Severe hypotension"],
        "mechanism": "'Triple whammy': NSAID + ACE inhibitor + diuretic. NSAIDs block renal prostaglandins, ACE inhibitor reduces efferent arteriolar tone, diuretic reduces volume. Synergistic nephrotoxicity.",
        "confidence": 0.92
    },
    "furosemide+diclofenac+losartan": {
        "risk": "HIGH",
        "side_effects": ["Acute kidney injury", "Hyperkalemia"],
        "mechanism": "NSAID + ARB + diuretic is the classic 'triple whammy' for acute kidney injury.",
        "confidence": 0.90
    },
    # ── Rifampin destroyer combos ────────────────────────────────────
    "cyclosporine+rifampin+tacrolimus": {
        "risk": "HIGH",
        "side_effects": ["Therapeutic failure", "Organ rejection"],
        "mechanism": "Rifampin massively induces CYP3A4, destroying levels of both calcineurin inhibitors. Transplant patients face imminent organ rejection.",
        "confidence": 0.98
    },
    # ── Multiple statins + CYP inhibitor ─────────────────────────────
    "clarithromycin+simvastatin+verapamil": {
        "risk": "HIGH",
        "side_effects": ["Rhabdomyolysis", "Acute kidney injury", "Liver failure"],
        "mechanism": "Clarithromycin + verapamil both inhibit CYP3A4. Dual inhibition causes extreme simvastatin accumulation.",
        "confidence": 0.95
    },
    # ── SSRI + TCA (serotonin syndrome + toxicity) ───────────────────
    "amitriptyline+fluoxetine+tramadol": {
        "risk": "HIGH",
        "side_effects": ["Serotonin syndrome", "Seizures", "Cardiac arrhythmia"],
        "mechanism": "Triple serotonergic threat. Fluoxetine inhibits CYP2D6, increasing both amitriptyline and tramadol levels. All three have serotonergic activity.",
        "confidence": 0.93
    },
    # ── Methotrexate + NSAID + Trimethoprim ──────────────────────────
    "ibuprofen+methotrexate+trimethoprim": {
        "risk": "HIGH",
        "side_effects": ["Myelosuppression", "Acute kidney injury", "Agranulocytosis"],
        "mechanism": "NSAID reduces methotrexate's renal clearance. Trimethoprim adds antifolate effect. Triple myelosuppressive risk.",
        "confidence": 0.91
    },
}


# =============================================================================
# PART 6: TIMING RECOMMENDATIONS
# =============================================================================

TIMING_RECOMMENDATIONS = {
    "aspirin": {"suggested_time": "Morning with food", "notes": "Take with food to reduce GI irritation. If on anticoagulants, max 8-hour gap."},
    "ibuprofen": {"suggested_time": "With food, spaced from aspirin", "notes": "Take at least 8 hours apart from aspirin."},
    "naproxen": {"suggested_time": "With food, twice daily", "notes": "Take every 12 hours with food."},
    "diclofenac": {"suggested_time": "With food, 2-3 times daily", "notes": "Take with food. Avoid concurrent aspirin or other NSAIDs."},
    "celecoxib": {"suggested_time": "With or without food", "notes": "Can take without food. Once or twice daily."},
    "meloxicam": {"suggested_time": "Once daily with food", "notes": "Long half-life allows once-daily dosing."},
    "warfarin": {"suggested_time": "Evening, consistent time daily", "notes": "Take at same time every day. Avoid major dietary vitamin K changes."},
    "apixaban": {"suggested_time": "Twice daily with or without food", "notes": "Take consistently every 12 hours."},
    "rivaroxaban": {"suggested_time": "Evening with food", "notes": "Must take with food for optimal absorption (15mg and 20mg doses)."},
    "dabigatran": {"suggested_time": "Twice daily with food", "notes": "Take with a full glass of water. Do not crush capsules."},
    "clopidogrel": {"suggested_time": "Morning", "notes": "Take 12+ hours apart from omeprazole if both needed. Pantoprazole preferred."},
    "metformin": {"suggested_time": "With meals (morning and evening)", "notes": "Take with food to reduce GI side effects. Extended-release: once daily with evening meal."},
    "glipizide": {"suggested_time": "30 minutes before meals", "notes": "Take 30 min before breakfast (and dinner if twice daily)."},
    "lisinopril": {"suggested_time": "Morning", "notes": "Once daily, consistent time. May cause dizziness initially."},
    "losartan": {"suggested_time": "Morning", "notes": "Once or twice daily. Do not combine with ACE inhibitors."},
    "atorvastatin": {"suggested_time": "Evening/bedtime", "notes": "Cholesterol synthesis peaks at night. Avoid grapefruit."},
    "simvastatin": {"suggested_time": "Evening/bedtime", "notes": "Must be taken in evening. Avoid grapefruit juice."},
    "rosuvastatin": {"suggested_time": "Any time of day", "notes": "Can take at any time. Long half-life."},
    "amlodipine": {"suggested_time": "Morning or evening", "notes": "Long half-life. Avoid grapefruit."},
    "metoprolol": {"suggested_time": "Morning and evening with food", "notes": "Take with food. Never stop abruptly — taper over 1-2 weeks."},
    "omeprazole": {"suggested_time": "30 minutes before breakfast", "notes": "Most effective before first meal. Take 12+ hours before clopidogrel."},
    "pantoprazole": {"suggested_time": "30 minutes before breakfast", "notes": "Preferred PPI with clopidogrel."},
    "gabapentin": {"suggested_time": "Three times daily", "notes": "Space evenly ~8 hours apart."},
    "pregabalin": {"suggested_time": "Two to three times daily", "notes": "Space doses evenly throughout the day."},
    "fluoxetine": {"suggested_time": "Morning", "notes": "Take in morning to avoid insomnia. Long half-life."},
    "sertraline": {"suggested_time": "Morning or evening with food", "notes": "Take with food to improve absorption."},
    "alprazolam": {"suggested_time": "As prescribed, 2-3 times daily", "notes": "Do not stop abruptly. Short-acting — evenly space doses."},
    "prednisone": {"suggested_time": "Morning with food", "notes": "Morning dosing mimics cortisol rhythm."},
    "tramadol": {"suggested_time": "Every 4-6 hours as needed", "notes": "Max 400mg/day. Avoid with SSRIs/MAOIs."},
    "acetaminophen": {"suggested_time": "As needed, max 3g/day", "notes": "Limit to 2g/day with warfarin. Space 4-6 hours."},
    "fluconazole": {"suggested_time": "Morning", "notes": "Space from statins by 12+ hours."},
    "ciprofloxacin": {"suggested_time": "Morning and evening, 12h apart", "notes": "Avoid antacids/dairy within 2 hours."},
    "amoxicillin": {"suggested_time": "Every 8 hours", "notes": "Can take with or without food."},
    "hydrochlorothiazide": {"suggested_time": "Morning", "notes": "Morning to avoid nocturia. Monitor potassium."},
    "furosemide": {"suggested_time": "Morning", "notes": "Take in morning. Monitor potassium and magnesium."},
    "spironolactone": {"suggested_time": "Morning with food", "notes": "Take with food. Monitor potassium closely with ACE/ARB."},
    "levothyroxine": {"suggested_time": "Morning on empty stomach", "notes": "Take 30-60 min before food. 4 hours before calcium/iron."},
    "amiodarone": {"suggested_time": "With food", "notes": "Take with food. Long half-life (40-55 days)."},
    "digoxin": {"suggested_time": "Morning, consistent time", "notes": "Monitor levels. Maintain normal potassium."},
    "lithium": {"suggested_time": "Twice daily with food", "notes": "Consistent salt/water intake. Monitor levels regularly."},
    "carbamazepine": {"suggested_time": "Twice daily with food", "notes": "Gradual dose titration. Monitor blood levels."},
    "phenytoin": {"suggested_time": "Twice daily, consistent time", "notes": "Monitor levels. Nonlinear kinetics — small dose changes cause large level changes."},
    "valproic acid": {"suggested_time": "Twice daily with food", "notes": "Take with food to reduce GI effects. Monitor liver function and levels."},
    "quetiapine": {"suggested_time": "Evening/bedtime", "notes": "Sedating — best taken at bedtime."},
    "clozapine": {"suggested_time": "Twice daily", "notes": "Monitor WBC/ANC. Smoking affects levels."},
    "cyclosporine": {"suggested_time": "Twice daily, consistent time", "notes": "Consistent timing with food. Monitor levels and renal function."},
    "tacrolimus": {"suggested_time": "Twice daily on empty stomach", "notes": "Take 1 hour before or 2 hours after meals. Monitor levels."},
    "methotrexate": {"suggested_time": "Once weekly", "notes": "ONCE WEEKLY — never daily. Take folic acid on non-methotrexate days."},
    "colchicine": {"suggested_time": "As prescribed", "notes": "Narrow therapeutic index. Never exceed prescribed dose."},
    "semaglutide": {"suggested_time": "Once weekly (injection)", "notes": "Same day each week. Can take at any time of day."},
    "theophylline": {"suggested_time": "Twice daily, consistent time", "notes": "Monitor levels. Smoking and CYP1A2 inhibitors affect levels dramatically."},
    "rifampin": {"suggested_time": "Morning on empty stomach", "notes": "Take 1 hour before or 2 hours after meals. All other drug doses may need adjustment."},
    "tizanidine": {"suggested_time": "As needed, up to 3 times daily", "notes": "NEVER combine with ciprofloxacin or fluvoxamine."},
}

# =============================================================================
# PART 7: PROGRAMMATIC INTERACTION GENERATION
# =============================================================================
# For drug pairs NOT in the curated list, generate interactions based on rules.

def _make_pair_key(a, b):
    return "+".join(sorted([a.lower().strip(), b.lower().strip()]))


def _make_triple_key(drugs):
    return "+".join(sorted([d.lower().strip() for d in drugs]))


def _has_pd_tag(drug_name, tag):
    drug = DRUGS.get(drug_name, {})
    return tag in drug.get("pd_tags", [])


def _get_cyp_substrates(drug_name):
    return set(DRUGS.get(drug_name, {}).get("cyp_enzymes", []))


def _get_cyp_inhibits(drug_name):
    return set(DRUGS.get(drug_name, {}).get("cyp_inhibits", []))


def _get_cyp_induces(drug_name):
    return set(DRUGS.get(drug_name, {}).get("cyp_induces", []))


def generate_programmatic_interactions():
    """Generate interactions for drug pairs not in the curated database."""
    generated = {}
    drug_names = list(DRUGS.keys())

    for a, b in combinations(drug_names, 2):
        pair_key = _make_pair_key(a, b)
        if pair_key in CURATED_PAIRWISE:
            continue  # Use curated version

        drug_a = DRUGS[a]
        drug_b = DRUGS[b]
        a_name = drug_a["name"]
        b_name = drug_b["name"]

        # Check CYP substrate-inhibitor interactions
        a_substrates = _get_cyp_substrates(a)
        b_substrates = _get_cyp_substrates(b)
        a_inhibits = _get_cyp_inhibits(a)
        b_inhibits = _get_cyp_inhibits(b)
        a_induces = _get_cyp_induces(a)
        b_induces = _get_cyp_induces(b)

        # Drug A is substrate, Drug B inhibits that enzyme
        inhibited_a = a_substrates & b_inhibits
        # Drug B is substrate, Drug A inhibits that enzyme
        inhibited_b = b_substrates & a_inhibits
        # Drug A substrate, Drug B induces that enzyme
        induced_a = a_substrates & b_induces
        # Drug B substrate, Drug A induces that enzyme
        induced_b = b_substrates & a_induces

        side_effects = []
        mechanisms = []
        risk = None

        # ── CYP Inhibition interactions ──────────────────────────────
        if inhibited_a or inhibited_b:
            affected_drug = a_name if inhibited_a else b_name
            inhibitor_drug = b_name if inhibited_a else a_name
            enzymes = inhibited_a or inhibited_b

            # Determine severity based on affected drug's properties
            affected_key = a if inhibited_a else b
            if _has_pd_tag(affected_key, "narrow_ti"):
                risk = "HIGH"
                side_effects.extend(["Elevated drug levels", "Drug toxicity"])
                mechanisms.append(
                    f"{inhibitor_drug} inhibits {', '.join(enzymes)}, increasing {affected_drug} levels. "
                    f"{affected_drug} has a narrow therapeutic index — toxicity likely."
                )
            elif _has_pd_tag(affected_key, "statin"):
                risk = "HIGH" if any(e in ["CYP3A4"] for e in enzymes) else "MEDIUM"
                side_effects.extend(["Myopathy", "Rhabdomyolysis"])
                mechanisms.append(
                    f"{inhibitor_drug} inhibits {', '.join(enzymes)}, increasing {affected_drug} levels "
                    f"and risk of muscle toxicity."
                )
            elif _has_pd_tag(affected_key, "opioid"):
                risk = "HIGH"
                side_effects.extend(["Respiratory depression", "Excessive sedation"])
                mechanisms.append(
                    f"{inhibitor_drug} inhibits {', '.join(enzymes)}, increasing {affected_drug} levels "
                    f"and risk of respiratory depression."
                )
            elif _has_pd_tag(affected_key, "benzodiazepine"):
                risk = "HIGH" if "CYP3A4" in enzymes else "MEDIUM"
                side_effects.extend(["Excessive sedation", "Respiratory depression"])
                mechanisms.append(
                    f"{inhibitor_drug} inhibits {', '.join(enzymes)}, increasing {affected_drug} levels."
                )
            elif _has_pd_tag(affected_key, "anticoagulant"):
                risk = "HIGH"
                side_effects.extend(["Elevated INR", "Severe bleeding"])
                mechanisms.append(
                    f"{inhibitor_drug} inhibits {', '.join(enzymes)}, reducing {affected_drug} clearance "
                    f"and increasing bleeding risk."
                )
            else:
                risk = "MEDIUM"
                side_effects.extend(["Elevated drug levels"])
                mechanisms.append(
                    f"{inhibitor_drug} inhibits {', '.join(enzymes)}, which metabolizes {affected_drug}. "
                    f"May increase {affected_drug} levels and toxicity risk."
                )

        # ── CYP Induction interactions ───────────────────────────────
        if induced_a or induced_b:
            affected_drug = a_name if induced_a else b_name
            inducer_drug = b_name if induced_a else a_name
            enzymes = induced_a or induced_b

            if risk is None or risk == "LOW":
                risk = "HIGH" if _has_pd_tag(a if induced_a else b, "narrow_ti") else "MEDIUM"
            side_effects.extend(["Reduced drug efficacy", "Therapeutic failure"])
            mechanisms.append(
                f"{inducer_drug} induces {', '.join(enzymes)}, increasing {affected_drug} metabolism "
                f"and potentially reducing its therapeutic effect."
            )

        # ── Pharmacodynamic interactions ─────────────────────────────

        # QT prolongation
        if _has_pd_tag(a, "qt_prolongation") and _has_pd_tag(b, "qt_prolongation"):
            risk = "HIGH"
            side_effects.extend(["QT prolongation", "Torsades de pointes"])
            mechanisms.append(
                f"Both {a_name} and {b_name} prolong the QT interval. "
                f"Combined use creates additive/synergistic QT prolongation risk."
            )

        # CNS depression
        if _has_pd_tag(a, "cns_depressant") and _has_pd_tag(b, "cns_depressant"):
            if risk is None or risk == "LOW":
                risk = "MEDIUM"
            if _has_pd_tag(a, "opioid") or _has_pd_tag(b, "opioid"):
                risk = "HIGH"
                side_effects.extend(["Respiratory depression", "CNS depression"])
            else:
                side_effects.extend(["Excessive sedation", "CNS depression"])
            mechanisms.append(
                f"Both {a_name} and {b_name} cause CNS depression. Additive sedation risk."
            )

        # Serotonin syndrome
        if _has_pd_tag(a, "serotonergic") and _has_pd_tag(b, "serotonergic"):
            risk = "HIGH"
            side_effects.extend(["Serotonin syndrome"])
            mechanisms.append(
                f"Both {a_name} and {b_name} have serotonergic activity. "
                f"Combined use increases risk of serotonin syndrome."
            )

        # MAOI + serotonergic
        if (_has_pd_tag(a, "maoi") and _has_pd_tag(b, "serotonergic")) or \
           (_has_pd_tag(b, "maoi") and _has_pd_tag(a, "serotonergic")):
            risk = "HIGH"
            side_effects.extend(["Serotonin syndrome"])
            mechanisms.append("MAOI + serotonergic agent creates severe serotonin syndrome risk. CONTRAINDICATED.")

        # Opioid + benzodiazepine
        if (_has_pd_tag(a, "opioid") and _has_pd_tag(b, "benzodiazepine")) or \
           (_has_pd_tag(b, "opioid") and _has_pd_tag(a, "benzodiazepine")):
            risk = "HIGH"
            side_effects.extend(["Respiratory depression", "Cardiac arrest"])
            mechanisms.append(
                f"FDA Black Box: Combined opioid ({a_name if _has_pd_tag(a, 'opioid') else b_name}) + "
                f"benzodiazepine ({b_name if _has_pd_tag(b, 'benzodiazepine') else a_name}) causes "
                f"profound respiratory depression."
            )

        # Anticoagulant + antiplatelet
        if (_has_pd_tag(a, "anticoagulant") and _has_pd_tag(b, "antiplatelet")) or \
           (_has_pd_tag(b, "anticoagulant") and _has_pd_tag(a, "antiplatelet")):
            if risk is None or risk != "HIGH":
                risk = "HIGH"
            side_effects.extend(["Severe bleeding", "Hemorrhage"])
            mechanisms.append(
                f"Anticoagulant + antiplatelet combination increases major bleeding risk significantly."
            )

        # Anticoagulant + NSAID
        if (_has_pd_tag(a, "anticoagulant") and _has_pd_tag(b, "nsaid")) or \
           (_has_pd_tag(b, "anticoagulant") and _has_pd_tag(a, "nsaid")):
            risk = "HIGH"
            side_effects.extend(["Gastrointestinal bleeding", "Severe bleeding"])
            mechanisms.append(
                f"Anticoagulant + NSAID: NSAIDs cause GI mucosal injury while anticoagulant impairs hemostasis. "
                f"High risk of GI hemorrhage."
            )

        # NSAID + NSAID
        if _has_pd_tag(a, "nsaid") and _has_pd_tag(b, "nsaid"):
            risk = "HIGH"
            side_effects.extend(["GI ulceration", "Gastrointestinal bleeding", "Acute kidney injury"])
            mechanisms.append(
                f"Duplicate NSAID therapy ({a_name} + {b_name}). No additional efficacy but dramatically "
                f"increased GI and renal toxicity."
            )

        # Dual antiplatelet
        if _has_pd_tag(a, "antiplatelet") and _has_pd_tag(b, "antiplatelet"):
            if risk is None:
                risk = "MEDIUM"
            side_effects.extend(["Severe bleeding", "Bruising"])
            mechanisms.append(
                f"Dual antiplatelet therapy increases bleeding risk."
            )

        # Hyperkalemia risk combinations
        if _has_pd_tag(a, "hyperkalemia_risk") and _has_pd_tag(b, "hyperkalemia_risk"):
            if risk is None or risk == "LOW":
                risk = "HIGH"
            side_effects.extend(["Hyperkalemia", "Cardiac arrhythmia"])
            mechanisms.append(
                f"Both {a_name} and {b_name} increase serum potassium. Additive hyperkalemia risk."
            )

        # Bradycardia risk combinations
        if _has_pd_tag(a, "bradycardia_risk") and _has_pd_tag(b, "bradycardia_risk"):
            if risk is None or risk == "LOW":
                risk = "MEDIUM"
            side_effects.extend(["Severe bradycardia", "Hypotension"])
            mechanisms.append(
                f"Both {a_name} and {b_name} reduce heart rate. Additive bradycardia risk."
            )

        # Nephrotoxic combinations
        if _has_pd_tag(a, "nephrotoxic") and _has_pd_tag(b, "nephrotoxic"):
            if risk is None or risk == "LOW":
                risk = "MEDIUM"
            side_effects.extend(["Acute kidney injury", "Nephrotoxicity"])
            mechanisms.append(
                f"Both {a_name} and {b_name} have nephrotoxic potential. Additive renal risk."
            )

        # Hepatotoxic combinations
        if _has_pd_tag(a, "hepatotoxic") and _has_pd_tag(b, "hepatotoxic"):
            if risk is None or risk == "LOW":
                risk = "MEDIUM"
            side_effects.extend(["Hepatotoxicity", "Elevated liver enzymes"])
            mechanisms.append(
                f"Both {a_name} and {b_name} have hepatotoxic potential. Monitor liver function."
            )

        # Anticholinergic burden
        if _has_pd_tag(a, "anticholinergic") and _has_pd_tag(b, "anticholinergic"):
            if risk is None or risk == "LOW":
                risk = "MEDIUM"
            side_effects.extend(["Excessive sedation", "Dizziness"])
            mechanisms.append(
                f"Both {a_name} and {b_name} have anticholinergic effects. Additive anticholinergic burden."
            )

        # NSAID + ACE/ARB (renal)
        if (_has_pd_tag(a, "nsaid") and (_has_pd_tag(b, "ace_inhibitor") or _has_pd_tag(b, "arb"))) or \
           (_has_pd_tag(b, "nsaid") and (_has_pd_tag(a, "ace_inhibitor") or _has_pd_tag(a, "arb"))):
            if risk is None or risk == "LOW":
                risk = "MEDIUM"
            side_effects.extend(["Acute kidney injury", "Reduced drug efficacy"])
            mechanisms.append(
                "NSAIDs reduce renal prostaglandin-mediated blood flow, opposing ACE/ARB renoprotective effect."
            )

        # If we found any interaction
        if risk and side_effects:
            # Deduplicate side effects
            seen = set()
            unique_se = []
            for se in side_effects:
                if se not in seen:
                    seen.add(se)
                    unique_se.append(se)

            generated[pair_key] = {
                "risk": risk,
                "side_effects": unique_se[:5],  # Top 5
                "mechanism": " ".join(mechanisms),
                "gap_hours": 12 if risk == "HIGH" else 6 if risk == "MEDIUM" else 0,
            }

    return generated


# =============================================================================
# PART 8: BUILD AND WRITE THE KNOWLEDGE BASE
# =============================================================================

def build_knowledge_base():
    """Build the complete knowledge base JSON."""

    print("Building Interactome-AI Knowledge Base...")

    # Build the drugs section (simplified for JSON — drop pd_tags/cyp_inhibits/cyp_induces)
    drugs_section = {}
    for drug_id, data in DRUGS.items():
        drugs_section[drug_id] = {
            "cid": data["cid"],
            "name": data["name"],
            "formula": data["formula"],
            "molecular_weight": data["molecular_weight"],
            "class": data["class"],
            "cyp_enzymes": data["cyp_enzymes"] + data.get("cyp_inhibits", []) + data.get("cyp_induces", []),
            "description": data["description"],
        }
        # Deduplicate CYP enzymes
        drugs_section[drug_id]["cyp_enzymes"] = list(set(drugs_section[drug_id]["cyp_enzymes"]))

    print(f"  → {len(drugs_section)} drugs")

    # Build CYP enzymes section (with substrates/inhibitors from drug data)
    cyp_section = {}
    for ename, edata in CYP_ENZYMES.items():
        substrates = [d for d, ddata in DRUGS.items() if ename in ddata.get("cyp_enzymes", [])]
        inhibitors = [d for d, ddata in DRUGS.items() if ename in ddata.get("cyp_inhibits", [])]
        inducers = [d for d, ddata in DRUGS.items() if ename in ddata.get("cyp_induces", [])]
        cyp_section[ename] = {
            "name": edata["name"],
            "description": edata["description"],
            "substrates": substrates,
            "inhibitors": inhibitors,
            "inducers": inducers,
            "risk_note": edata["risk_note"],
        }

    # Build pairwise interactions
    pairwise_section = dict(CURATED_PAIRWISE)
    programmatic = generate_programmatic_interactions()
    pairwise_section.update(programmatic)
    print(f"  → {len(CURATED_PAIRWISE)} curated + {len(programmatic)} generated = {len(pairwise_section)} pairwise interactions")

    # Build higher-order interactions
    ho_section = dict(CURATED_HIGHER_ORDER)
    print(f"  → {len(ho_section)} higher-order interactions")

    # Timing
    print(f"  → {len(TIMING_RECOMMENDATIONS)} timing recommendations")

    # Side effect catalog
    print(f"  → {len(SIDE_EFFECT_CATALOG)} side effects cataloged")

    kb = {
        "drugs": drugs_section,
        "cyp_enzymes": cyp_section,
        "pairwise_interactions": pairwise_section,
        "higher_order_interactions": ho_section,
        "timing_recommendations": TIMING_RECOMMENDATIONS,
        "side_effect_catalog": SIDE_EFFECT_CATALOG,
    }

    # Write output
    output_path = os.path.join(os.path.dirname(__file__), "app", "data", "drug_interactions.json")
    with open(output_path, "w") as f:
        json.dump(kb, f, indent=2)

    file_size = os.path.getsize(output_path)
    print(f"\n✅ Knowledge base written to {output_path}")
    print(f"   File size: {file_size / 1024:.1f} KB")
    print(f"   Total drugs: {len(drugs_section)}")
    print(f"   Total pairwise interactions: {len(pairwise_section)}")
    print(f"   Total higher-order interactions: {len(ho_section)}")


if __name__ == "__main__":
    build_knowledge_base()
