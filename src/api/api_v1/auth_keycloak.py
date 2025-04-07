from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
from starlette.responses import RedirectResponse
import httpx
from core.config import settings

router = APIRouter(prefix=settings.api.v1.auth, tags=["Auth"])

keycloak_openid = KeycloakOpenID(
    server_url="http://192.168.49.2:30001/",
    client_id="fastapi-app",
    realm_name="myrealm",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        # Проверка токена
        userinfo = keycloak_openid.userinfo(token)
        return {"message": "You are authenticated", "user": userinfo}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.get("/login")
async def login():
    keycloak_login_url = (
        "http://192.168.49.2:30001/realms/myrealm/protocol/openid-connect/auth?"
        "response_type=code&"
        "client_id=fastapi-app&"
        f"redirect_uri=http://localhost:8000/api/v1/auth/callback&"
        "scope=openid"
    )
    print(keycloak_login_url)

    return RedirectResponse(keycloak_login_url)


@router.get("/callback")
async def callback(code: str):
    token_url = "http://192.168.49.2:30001/realms/myrealm/protocol/openid-connect/token"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": "fastapi-app",
                "client_secret": "your-client-secret",
                "code": code,
                "redirect_uri": "http://localhost:8000/api/v1/auth/callback",
            },
        )
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail="Failed to get token")
