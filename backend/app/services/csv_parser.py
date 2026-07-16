import pandas as pd

def extract_csv(file_path):
    df = pd.read_csv(file_path)

    text = df.to_string(index=False)

    return {
        "rows": len(df),
        "words": len(text.split()),
        "text": text
    }