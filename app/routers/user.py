from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app import models
from app.database import get_db
from app.schemas import LoginRequest, UserList, UserRegistration

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

password_hash = PasswordHash.recommended()

# ✅ Register
@router.post("/register/", response_model=UserList, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    new_user = models.UserModel(
        username=user.username,
        email=user.email,
        password=password_hash.hash(user.password)
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

# ✅ List users
@router.get("/list/", response_model=list[UserList])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.UserModel).all()