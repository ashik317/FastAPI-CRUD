from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import UserList, UserRegistration
from app.utils import hash_password

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# Register
@router.post("/register/", response_model=UserList, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    # Check if user already exists by email
    existing_user = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.UserModel(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)  # hash the password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# List users
@router.get("/list/", response_model=list[UserList])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.UserModel).all()

# delete user
@router.delete("/delete/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None