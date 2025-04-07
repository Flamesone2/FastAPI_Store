from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID

from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


keycloak_openid = KeycloakOpenID(
    server_url="http://192.168.49.2:30001/",
    client_id="fastapi-app",
    realm_name="myrealm",
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
