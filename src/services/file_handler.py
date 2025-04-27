# src/services/file_handler.py
import pandas as pd
import json
import os,sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def load_excel(file_path, sheet_name):    
    
    return pd.read_excel(file_path, sheet_name=sheet_name)

def save_json(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Garante que o diretório exista
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)