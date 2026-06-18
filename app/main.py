from fastapi import FastAPI

from app.database import Base, engine
from app import models  # noqa: F401 - registra los modelos en Base.metadata
from app.routers import cita
from app.routers import paciente_router
from app.routers import medico_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SISMED UPS - API",
    description="Backend académico del sistema de gestión médica SISMED UPS",
    version="0.1.0",
)

app.include_router(cita.router)


@app.get("/")
def read_root():
    return {"message": "SISMED UPS API funcionando correctamente"}


app.include_router(
    paciente_router.router
)


app.include_router(
    medico_router.router
)