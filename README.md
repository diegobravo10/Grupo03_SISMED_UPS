# SISMED UPS - Backend

Backend académico del sistema de gestión médica SISMED UPS, desarrollado con FastAPI y SQLite (SQLAlchemy).

## Estructura del proyecto

```
app/
├── main.py
├── database.py
├── models/
├── schemas/
├── repositories/
├── services/
└── routers/
```

## Requisitos

- Python 3.10+

## Instalación

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.

## Documentación interactiva (Swagger)

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
