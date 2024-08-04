from src.utils.model import PostSchema, UserSchema, UserLoginSchema
import pandas as pd
import os


base_dir = os.path.dirname(os.path.dirname(__file__))
df = pd.read_csv(base_dir + '/auth/users.csv')
users = df.to_dict(orient='records')

def check_user(data: UserLoginSchema):
    """
    Verifica se as credenciais fornecidas correspondem a um usuário válido.

    Compara o email e a senha fornecidos com a lista de usuários registrados. Retorna `True` se as credenciais forem válidas e `False` caso contrário.

    Args:
        data (UserLoginSchema): Dados de login do usuário, incluindo email e senha.

    Returns:
        bool: `True` se o usuário for encontrado e as credenciais forem válidas, `False` caso contrário.
    """
    for user in users:
        if user['email'] == data.email and user['password'] == data.password:
            return True
    return False


