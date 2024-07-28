import pandas as pd
import logging

def load_csv_with_separator(file_path, separators):
    for sep in separators:
        try:
            df = pd.read_csv(file_path, sep=sep)
            if df.shape[1] > 1:  # Verificar se temos mais de uma coluna
                return df
        except Exception as e:
            logging.warning(f"Erro ao tentar ler o arquivo com o separador '{sep}': {e}")
    return None