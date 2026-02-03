# 新闻分类的封装crud操作
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


async def get_categories(db:AsyncSession,skip: int = 0, limit: int = 100):
    #模拟获取新闻分类列表-》先定义模型类,封装再实现crud操作
    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()
async def get_news_count(db:AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one() #只能有一个
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt=select(News).where(News.id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()
async def add_news_views(db:AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views + 1)
    result=await db.execute(stmt)
    await db.commit()
    #更新-》检查数据库是否真的命中了数据-》命中了返回True
    return result.rowcount > 0 if hasattr(result,'rowcount') else True
async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit: int= 5):
    #order_by 排序-》浏览量和发布时间
    # 为防止返回内容重复（例如数据库中存在几条标题/图片相同的记录），
    # 先多取几条结果，然后在 Python 端按 (title, image) 去重，最后截取 limit 条返回
    fetch_limit = max(limit * 3, 10)
    stmt=select(News).where(News.category_id==category_id,News.id != news_id).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(fetch_limit)
    result=await db.execute(stmt)
    related_news=result.scalars().all()
    unique = []
    seen = set()
    for news_detail in related_news:
        # 确保不包含当前新闻本身
        if news_detail.id == news_id:
            continue
        # 使用标题和图片作为去重键（都归一化），如果需要可以改为只按 title 去重
        title = (getattr(news_detail, 'title', '') or '').strip().lower()
        image = (getattr(news_detail, 'image', '') or '').strip()
        key = (title, image)
        if key in seen:
            continue
        seen.add(key)
        unique.append(news_detail)
        if len(unique) >= limit:
            break
    return unique
