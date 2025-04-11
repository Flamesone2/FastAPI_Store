from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
import base64
import json


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://192.168.49.2:30001/realms/myrealm/protocol/openid-connect/token"
)


keycloak_openid = KeycloakOpenID(
    server_url="http://192.168.49.2:30001/",
    client_id="fastapi-app",
    realm_name="myrealm",
)


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         userinfo = keycloak_openid.userinfo(token)
#         return userinfo["sub"]
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        header, payload, signature = token.split(".")

        decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
        payload_data = json.loads(decoded_payload)

        if payload_data.get("aud") != "fastapi-app":
            raise HTTPException(status_code=401, detail="Invalid audience")

        userinfo = keycloak_openid.userinfo(token)
        return userinfo["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
