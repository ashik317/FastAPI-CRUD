from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import LoginRequest, UserList
from app.utils import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login/", response_model=UserList)
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(
        models.UserModel.email == login.email
    ).first()
    
    if not user or not verify_password(login.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user