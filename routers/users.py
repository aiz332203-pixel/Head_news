from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from schemas.users import UserRequest
from crud import users
router=APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register_user(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    existing_user=await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    new_user=await users.create_user(db, user_data)
    token=await users.create_token(db, new_user.id)
    return {
        "code": 200,
        "message": "用户注册成功",
        "data": {
            "token": token,
            "userInfo": {
                "id":new_user.id,
                "username": new_user.username,
                "bio":new_user.bio,
                "avatar": new_user.avatar
            }
        }
    }
