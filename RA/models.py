import joblib


model_path = "models/score-model-rgn.joblib"
score_model = joblib.load(model_path)
personamodel_path = "models/personamdl.joblib"
persona_model = joblib.load(personamodel_path)