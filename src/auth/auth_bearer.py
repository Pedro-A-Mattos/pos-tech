from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    """
    Classe de autenticação personalizada que usa tokens JWT para verificar credenciais.

    Herda de `HTTPBearer` e é responsável por validar tokens JWT em requisições HTTP.

    Methods:
        __call__(self, request: Request) -> str:
            Valida o token JWT na requisição e retorna o token se for válido.
        
        verify_jwt(self, jwtoken: str) -> bool:
            Verifica se o token JWT é válido.

    Raises:
        HTTPException: Se o esquema de autenticação for inválido ou o token for inválido ou expirado.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        """
        Verifica se o token JWT fornecido é válido.

        Args:
            jwtoken (str): O token JWT a ser verificado.

        Returns:
            bool: `True` se o token for válido, `False` caso contrário.
        """
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid