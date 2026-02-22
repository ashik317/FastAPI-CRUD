import time
from fastapi import FastAPI, Depends, HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from app import models
from app.database import engine, get_db
from app.schemas import (
    CourseCreate,
    CourseUpdate,
    LoginRequest,
    UserList,
    UserRegistration
)
from app.utils import hash_password

# FastAPI instance
app = FastAPI(title="Course API")

# Startup: wait for DB + create tables
@app.on_event("startup")
def startup_db():
    retries = 15
    for i in range(retries):
        try:
            with engine.connect():
                print("Database connected")
                models.Base.metadata.create_all(bind=engine)
                return
        except OperationalError:
            print(f"DB not ready ({i+1}/{retries}), retrying...")
            time.sleep(2)

    print("Database not available, app started without DB")


# course APIs

@app.post(
    "/course/create/",
    status_code=status.HTTP_201_CREATED
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    db_course = models.CourseModel(**course.model_dump())

    try:
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not create course"
        )


@app.get("/courses/list/")
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.CourseModel).all()


@app.get("/course/{course_id}/")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = (
        db.query(models.CourseModel)
        .filter(models.CourseModel.id == course_id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.put("/course/update/{course_id}/")
def update_course(
    course_id: int,
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    db_course = (
        db.query(models.CourseModel)
        .filter(models.CourseModel.id == course_id)
        .first()
    )

    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in course.model_dump().items():
        setattr(db_course, key, value)

    try:
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not update course"
        )


@app.patch("/course/partial-update/{course_id}/")
def partial_update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db)
):
    db_course = (
        db.query(models.CourseModel)
        .filter(models.CourseModel.id == course_id)
        .first()
    )

    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in course.model_dump(exclude_unset=True).items():
        setattr(db_course, key, value)

    try:
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not partially update course"
        )


@app.delete(
    "/course/delete/{course_id}/",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = (
        db.query(models.CourseModel)
        .filter(models.CourseModel.id == course_id)
        .first()
    )

    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    try:
        db.delete(db_course)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not delete course"
        )

# User Registration API
@app.post("/user/register/", response_model=UserList, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserRegistration,
    db: Session = Depends(get_db)
):
    new_user = models.UserModel(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

# GET all users List
@app.get("/users/list/", response_model=list[UserList])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.UserModel).all()

# GET user by ID
@app.get("/users/{user_id}/", response_model=UserList)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(models.UserModel)
        .filter(models.UserModel.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# User login API
@app.post("/user/login/", status_code=status.HTTP_200_OK)
def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.UserModel)
        .filter(models.UserModel.email == login_data.email)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_hash = PasswordHash.recommended()
    if not password_hash.verify(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}