from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from src.api import properties
from src.core.config import FRONTEND_HOSTNAME, WHEELTRIP_USER_PORT, REQUEST_PROTOCOL, ENVIRONMENT
from src.api import users, trajets

app = FastAPI()
app.include_router(properties.router, prefix="/api")
app.include_router(users.router, prefix="/api")
# app.include_router(trajets.router, prefix="/api")
# app.include_router(auth.router, prefix="/api")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="DataMedia",
        version="0.1.0",
        description="Documentation pour l'API DataMedia. Consultez moi (Alejo) pour quelconque suggestion, problème ou question.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS configuration
if ENVIRONMENT.lower() in ["local", "development"]:
    origins = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ]
else:
    # CORS configuration
    origins = [
        f"{REQUEST_PROTOCOL}://{FRONTEND_HOSTNAME}:{WHEELTRIP_USER_PORT}",
    ]

# Add CORS middleware to allow cross-origin requests
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
