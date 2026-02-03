# 新闻分类模型定义
from typing import Optional
from sqlalchemy import Index, Text, ForeignKey
from datetime import datetime
from sqlalchemy import DateTime

from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        #nullable=False,
        comment="记录创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        onupdate=datetime.now,
        #nullable=False,
        comment="记录更新时间"
    )
class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True, comment="主键ID")
    name: Mapped[str] = mapped_column(String(50),unique=True,nullable=False,comment="新闻分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0,nullable=False,comment="排序字段，数值越小越靠前")
    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name}, sort_order={self.sort_order})"
# 创建索引，提升查询速度
class News(Base):
    __tablename__ = "news"
    __table_args__=(
        Index('fk_news_category_idx','category_id'),
        Index('idx_publish_time','publish_time')
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="新闻描述")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="新闻封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="新闻作者")
    category_id: Mapped[int] = mapped_column(Integer,ForeignKey('news_category.id'),nullable=False, comment="所属分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览次数")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="发布时间")
    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, category_id={self.category_id}, published_at={self.published_at})>"
    