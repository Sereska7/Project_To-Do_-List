from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


class DataBaseHelper:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(bind=self.engine)

    async def dispose(self):
        await self.engine.dispose()


if settings.MODE == "TEST":
    DATABASE_PARAMS = {"poolclass": NullPool}
    db_helper = DataBaseHelper(url=str(settings.TEST_DB_URL))
else:
    DATABASE_PARAMS = {}
    db_helper = DataBaseHelper(url=str(settings.DB_URL))
