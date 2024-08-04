import pandas as pd
import logging

def load_csv_with_separator(file_path, separators):
    """
    Esta função tenta carregar um arquivo CSV usando uma lista de separadores fornecida. 
    Se o arquivo for carregado com sucesso e contiver mais de uma coluna, retorna o DataFrame.
    Caso contrário, tenta o próximo separador da lista. Se nenhum separador funcionar, retorna None.

    Args:
        file_path (str): O caminho para o arquivo CSV.
        separators (list): Uma lista de strings, onde cada string é um separador a ser tentado.

    Returns:
        pd.DataFrame or None: Um DataFrame pandas se o arquivo for carregado com sucesso 
                              usando um dos separadores; caso contrário, retorna None.
    """
    for sep in separators:
        try:
            df = pd.read_csv(file_path, sep=sep)
            if df.shape[1] > 1:  # Verificar se temos mais de uma coluna
                return df
        except Exception as e:
            logging.warning(f"Erro ao tentar ler o arquivo com o separador '{sep}': {e}")
    return None