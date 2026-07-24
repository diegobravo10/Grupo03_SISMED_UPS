from fastapi import FastAPI

from app.database import Base, engine
from app import models  # noqa: F401 - registra los modelos en Base.metadata
from app.routers import administrativo, certificado_medico, cita, consulta_medica, medico, orden_medica, paciente, prescripcion_medica
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SISMED UPS - API",
    description="Backend académico del sistema de gestión médica SISMED UPS",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cita.router)


@app.get("/")
def read_root():
    return {"message": "SISMED UPS API funcionando correctamente"}


app.include_router(
    paciente.router
)


app.include_router(
    medico.router
)


app.include_router(
    administrativo.router
)

app.include_router(
    consulta_medica.router
)

app.include_router(
    prescripcion_medica.router
)

app.include_router(
    orden_medica.router
)

app.include_router(
    certificado_medico.router
)