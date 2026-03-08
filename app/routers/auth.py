from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LoginRequest, TokenResponse
from app.utils import verify_password
from .. import auth2, database, models, schemas
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login/", response_model=TokenResponse)
def login_user(
    login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.UserModel)
        .filter(models.UserModel.email == login.username)
        .first()
    )

    if not user or not verify_password(login.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth2.create_access_token(
        data={"user_id": user.id},
    )
    return TokenResponse(
        access_token=access_token, token_type="bearer", message="Login successful"
    )
