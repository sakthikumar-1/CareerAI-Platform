import pandas as pd

def get_top_skills():
    df = pd.read_csv(r"C:\Users\sakth\OneDrive\Desktop\AI_Career_App\phase1_top_market_skills.xls")
    return df.head(20).to_dict(orient="records")

