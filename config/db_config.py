#异步数据库配置文件
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
#数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:Zhang2003@localhost:3306/news_app?charset=utf8mb4"
#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 是否输出SQL日志
    pool_size=10,  # 启用连接池预检
    max_overflow=20 # 连接池最大溢出数量
)
#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
#依赖注入获取异步会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()







