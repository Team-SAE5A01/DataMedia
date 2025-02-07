from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .config import FRONTEND_HOSTNAME, WHEELTRIP_USER_PORT, REQUEST_PROTOCOL, ENVIRONMENT
app = FastAPI()

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

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
