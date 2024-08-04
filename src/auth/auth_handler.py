import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    """
    Cria uma resposta de token contendo o token de acesso.

    Args:
        token (str): O token JWT gerado.

    Returns:
        dict: Dicionário com o token de acesso.
    """
    return {
        "access_token": token
    }


def sign_jwt(user_id: str) -> Dict[str, str]:
    """
    Gera um token JWT para o usuário especificado.

    Cria um payload com o ID do usuário e um tempo de expiração. Codifica o payload em um token JWT.

    Args:
        user_id (str): ID do usuário para incluir no token.

    Returns:
        dict: Dicionário contendo o token JWT gerado.
    
    Example:
        >>> sign_jwt("user_id_here")
        {"access_token": "jwt_token_here"}
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    """
    Decodifica um token JWT e verifica sua validade.

    Tenta decodificar o token JWT e verifica se não expirou. Retorna o payload decodificado ou um dicionário vazio se inválido.

    Args:
        token (str): O token JWT a ser decodificado.

    Returns:
        dict: Payload decodificado se o token for válido, ou um dicionário vazio caso contrário.
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}