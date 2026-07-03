from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# движек для подключния к бд
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG, #active logs
    pool_size=5, # max count connections
    max_overflow=10, # доп соединения при пиковой нагрузке
)

# фабрика сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

