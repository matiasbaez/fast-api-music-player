from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import uuid
import bcrypt
import jwt

from pydantic_schemas.user_login import UserLogin
from pydantic_schemas.user_create import UserCreate
from middleware.auth_middleware import auth_middleware
from models.user import User
from database import get_db

router = APIRouter()

@router.post("/signup")
async def singnup_user(user: UserCreate, db: Session=Depends(get_db)):

    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(400, "User already exists")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    user = User(
        id=str(uuid.uuid4()),
        email=user.email,
        username=user.name,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = jwt.encode({"id": str(user.id)}, "password_secret", algorithm="HS256")

    return {"token": token, "user": user}

@router.post("/signin")
async def singnin_user(user: UserLogin, db: Session=Depends(get_db)):

    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(400, "User or password invalid")

    if not bcrypt.checkpw(user.password.encode('utf-8'), user_db.password):
        raise HTTPException(400, "User or password invalid")

    token = jwt.encode({"id": str(user_db.id)}, "password_secret", algorithm="HS256")

    return {"token": token, "user": user_db}

@router.get("/")
def current_user(db: Session=Depends(get_db), user_dic: dict=Depends(auth_middleware)):

    user = db.query(User).filter(User.id == user_dic["uid"]).first()

    if not user:
        raise HTTPException(400, "User not found")

    return user
