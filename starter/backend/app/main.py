from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.provider import DemoProvider

app = FastAPI(title="starter")
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
