"""
This module initializes the FastAPI application, sets up middleware, and includes routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.session import init_db
from backend.routes import user, credential, two_factor_authentication, sshkey, password_generator, recover_main_password
from contextlib import asynccontextmanager

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    This is where you can initialize resources or perform setup tasks.
    """
    init_db()
    yield
app = FastAPI(lifespan=lifespan)

# Include routes without prefix
app.include_router(user.router)
app.include_router(credential.router)
app.include_router(two_factor_authentication.router)
app.include_router(sshkey.router)
app.include_router(password_generator.router)

app.include_router(recover_main_password.router)

@app.get("/")
def read_root():
    """Root endpoint returning a welcome message."""
    return {"message": "Hello from FastAPI"}
