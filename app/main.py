from fastapi import FastAPI

app = FastAPI(
    title="SISMED UPS - API",
    description="Backend académico del sistema de gestión médica SISMED UPS",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "SISMED UPS API funcionando correctamente"}
