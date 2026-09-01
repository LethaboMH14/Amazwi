from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.provider import DemoProvider
from app.routes import consent_router, council_router
from app.routes.contributions import router as contribution_router
from app.routes.assignments import router as assignment_router

app = FastAPI(title="starter")
app.include_router(consent_router)
app.include_router(contribution_router)
app.include_router(assignment_router)
app.include_router(council_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

provider = DemoProvider()


@app.get("/health")
@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "provider_mode": provider.mode}
