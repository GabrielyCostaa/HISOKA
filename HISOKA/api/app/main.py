from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse, HTMLResponse
from .routers import auth, exams, readings, users
from .settings import Settings

settings = Settings()
app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(exams.router)
app.include_router(readings.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,  # ou ["*"] para liberar tudo (não recomendado em produção)
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
