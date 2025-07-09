from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
from static.user import username_exists, email_exists, insert_user, get_user_by_username
from utils.jwt_utils import jwt_manager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

class RegisterResponse(BaseModel):
    success: bool

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    accessToken: str
    username: str


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse)
def register(req: RegisterRequest):
    if username_exists(req.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    if email_exists(req.email):
        raise HTTPException(status_code=400, detail="邮箱已注册")

    success = insert_user(req.username, req.email, hash_password(req.password))
    if not success:
        raise HTTPException(status_code=500, detail="用户注册失败")
    return RegisterResponse(success=True)


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    row = get_user_by_username(req.username)
    if not row:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    username, hashed_pw = row  # 去掉 user_id
    if not verify_password(req.password, hashed_pw):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = jwt_manager.create_token(username=username)
    return LoginResponse(accessToken=token, username=username)

