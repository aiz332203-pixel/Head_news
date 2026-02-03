from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    # 这里可以添加更多允许的来源
    "http://localhost:5173/"
]
# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源,开发的时候可以使用*，企业上线时必须指定具体域名，以防止跨站攻击
    allow_credentials=True,# 允许携带cookie
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

#注册路由
app.include_router(news.router)
app.include_router(users.router)

