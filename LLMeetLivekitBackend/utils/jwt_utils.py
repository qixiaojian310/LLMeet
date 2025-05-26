import base64
import os
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import datetime
from dotenv import load_dotenv
load_dotenv()  # 这一步是关键：加载 .env 文件的变量到 os.environ

security = HTTPBearer()


class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def verify_token(self, token: str) -> Optional[str]:
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload["sub"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            print(f"Token验证失败: {e}")
            return None


# 初始化 JWT
jwt_manager = JWTManager(secret_key=os.environ.get("TOKEN_SECRET_KEY"))

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    user_id = jwt_manager.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id
