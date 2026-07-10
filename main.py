import logging.config
import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, LOGGING_CONFIG
from app.api.v1 import router as v1_router

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs",
    version="1.0.0",
)

# настройка cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  
        logging.FileHandler("app.log"),  
    ]
)

app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
