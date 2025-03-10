from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from src.api import properties, auth_routes, user_routes
from src.core.config import FRONTEND_HOSTNAME, WHEELTRIP_USER_PORT, REQUEST_PROTOCOL, ENVIRONMENT

app = FastAPI()

# Include your API routers
app.include_router(properties.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")

# Define OAuth2 security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="DataMedia",
        version="0.1.0",
        description="Documentation pour l'API DataMedia. Consultez-moi (Alejo) pour toute suggestion, problème ou question.",
        routes=app.routes,
    )

    # Define security scheme for Swagger
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply security globally to all routes
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Apply custom OpenAPI schema
app.openapi = custom_openapi

# CORS configuration
if ENVIRONMENT.lower() in ["local", "development"]:
    origins = ["*"]  # Allows all origins (any IP)
else:
    origins = ["*"]  # Allows all origins in production too (use with caution)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4500, reload=True)
