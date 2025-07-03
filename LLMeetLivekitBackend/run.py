from fastapi import FastAPI
from static.database_connector import init_connection_pool, close_connection_pool
from router import meeting
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🟢 启动时：初始化数据库连接池
    init_connection_pool()
    print("✅ Database connection pool initialized.")

    yield  # ⬅️ 应用正常运行

    # 🔴 关闭时：释放数据库连接池
    close_connection_pool()
    print("✅ Database connection pool closed.")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者指定域名 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 挂载 auth 路由
app.include_router(meeting.router)


def main():
    uvicorn.run("run:app", host="0.0.0.0", port=7700, reload=True)


if __name__ == "__main__":
    main()
