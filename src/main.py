import uvicorn
from api import router as api_router
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI Store",
    description="API for an online store with Keycloak authentication",
    version="0.1.0",
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://192.168.49.2:30001/realms/myrealm/protocol/openid-connect/token"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (для тестирования)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Store",
        version="0.1.0",
        description="API for an online store with Keycloak authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": "http://192.168.49.2:30001/realms/myrealm/protocol/openid-connect/auth",
                    "tokenUrl": "http://192.168.49.2:30001/realms/myrealm/protocol/openid-connect/token",
                    "scopes": {},
                }
            },
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(
    api_router,
)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
    )
