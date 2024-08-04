from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


class DataBaseHelper:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(bind=self.engine)

    async def dispose(self):
        await self.engine.dispose()


db_helper = DataBaseHelper(url=str(settings.DB_URL))
