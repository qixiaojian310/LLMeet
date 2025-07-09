import os
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()
security = HTTPBearer()

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_seconds: int = 86400):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_seconds = expire_seconds

    def create_token(self, username: str) -> str:
        """创建 JWT，只包含 username"""
        payload = {
            "sub": username,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expire_seconds),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[str]:
        """验证 JWT 并返回 username"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload.get("sub")
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            print(f"Token验证失败: {e}")
            return None


# 初始化
jwt_manager = JWTManager(secret_key=os.environ.get("TOKEN_SECRET_KEY"))

# FastAPI 依赖项：获取当前用户（username）
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    username = jwt_manager.verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username
