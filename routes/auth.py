from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import bcrypt

from pydantic_schemas.user_login import UserLogin
from models.user import User
from database import get_db

router = APIRouter()

@router.post("/signup")
async def singnup_user(user: UserLogin, db: Session=Depends(get_db)):

    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(400, {"message": "User already exists"})

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    user = User(
        id=uuid.uuid4(),
        email=user.email,
        username=user.username,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/signin")
async def singnin_user(user: UserLogin, db: Session=Depends(get_db)):

    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(400, {"message": "User or password invalid"})

    if not bcrypt.checkpw(user.password.encode('utf-8'), user_db.password):
        raise HTTPException(400, {"message": "User or password invalid"})

    return user_db