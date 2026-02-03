# 新闻模块路由文件
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import news
router = APIRouter(prefix="/api/news", tags=["news"])
#接口实现流程
#1.模块化路由-》API接口规范文档
#2.定义模型类-》数据库表（数据库设计文档）
#3.在crud文件夹下实现增删改查，封装数据库操作
#4.在路由文件中调用crud文件夹下的增删改查操作
@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100,db:AsyncSession=Depends(get_db)):
   #模拟获取新闻分类列表-》先定义模型类,封装再实现crud操作
    categories=await news.get_categories(db,skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data":categories
    }
@router.get("/list")
async def get_news_list(
        category_id: int = Query(...,alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize",le=100),
        db: AsyncSession = Depends(get_db)
):
    # 思路:处理分页规则-》查询新闻列表-》计算总量-》计算是否有更多
    offset=(page - 1) * page_size
    news_list=await news.get_news_list(db, category_id,offset,page_size)
    total=await news.get_news_count(db, category_id)
    #（跳过的+每页大小）<总数
    hasmore=(offset + page_size )< total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": hasmore
        }
    }
@router.get("/detail")
async def read_news_detail(news_id: int = Query(..., alias="id"),db: AsyncSession = Depends(get_db)):
    news_detail=await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻未找到")
    views_res=await news.add_news_views(db, news_detail.id)
    if not views_res:
        raise HTTPException(status_code=500, detail="浏览失败")
    # 确保返回值中的 views 是递增后的值（update 已提交到 DB，但对象内存值可能未更新）
    try:
        news_detail.views = (news_detail.views or 0) + 1
    except Exception:
        pass
    related_news=await news.get_related_news(db, news_detail.id, news_detail.category_id)
    return {
    "code": 200,
    "message": "success",
    "data": {
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": related_news #相关推荐
        }
    }