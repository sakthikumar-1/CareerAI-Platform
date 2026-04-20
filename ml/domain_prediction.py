import joblib
import pandas as pd

model = joblib.load("models/domain_model.pkl")
le = joblib.load("models/label_encoder.pkl")

def predict_domain(skill_list, columns):

    input_data = {col: 0 for col in columns}

    for skill in skill_list:
        if skill in input_data:
            input_data[skill] = 1

    new_user_df = pd.DataFrame([input_data])

    prediction = model.predict(new_user_df)

    return le.classes_[prediction[0]]
