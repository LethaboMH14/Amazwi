from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.provider import DemoProvider
from app.routes import consent_router

app = FastAPI(title="starter")
app.include_router(consent_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

provider = DemoProvider()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "provider_mode": provider.mode}
