import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security

# 根据用户名获取用户信息
async def get_user_by_username(db: AsyncSession, username: str):
    stmt=select(User).where(User.username == username)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    hashed_password = security.get_hash_password(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) # 重新数据库读会最新的 user
    return user
#生成token
async def create_token(db: AsyncSession, user_id: int):
    #这里模拟生成token+过期时间
    token=str(uuid.uuid4())
    expire_at=datetime.now()+timedelta(days=7)
    #查询数据库
    stmt=select(UserToken).where(UserToken.id==user_id)
    result=await db.execute(stmt)
    user_token=result.scalar_one_or_none()
    if user_token:
        #更新token和过期时间
        user_token.token=token
        user_token.expires_at=expire_at
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expire_at)
        db.add(user_token)
    await db.commit()
    await db.refresh(user_token)
    return token,user_token
