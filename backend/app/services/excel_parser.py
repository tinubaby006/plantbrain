import pandas as pd

def extract_excel(file_path):
    sheets = pd.read_excel(file_path, sheet_name=None)

    text = ""

    for name, sheet in sheets.items():
        text += f"\nSheet: {name}\n"
        text += sheet.to_string(index=False)

    return {
        "sheets": len(sheets),
        "words": len(text.split()),
        "text": text
    }