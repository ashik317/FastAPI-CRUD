from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app import auth2
from app.database import get_db
from app.schemas import CourseCreate, CourseUpdate

router = APIRouter(
    prefix="/course",
    tags=["Course"]
)

# Create course
@router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(auth2.get_current_user)
):
    db_course = models.CourseModel(**course.model_dump())
    try:
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return db_course
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create course")


# List courses
@router.get("/list/")
def list_courses(db: Session = Depends(get_db), current_user: models.UserModel = Depends(auth2.get_current_user)):
    return db.query(models.CourseModel).all()


# Get single course
@router.get("/{course_id}/")
def get_course(course_id: int, db: Session = Depends(get_db), current_user: models.UserModel = Depends(auth2.get_current_user)):
    course = db.query(models.CourseModel).filter(
        models.CourseModel.id == course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# Update course
@router.put("/update/{course_id}/", status_code=status.HTTP_200_OK)
def update_course(
    course_id: int,
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(auth2.get_current_user)
):
    db_course = db.query(models.CourseModel).filter(
        models.CourseModel.id == course_id
    ).first()

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
        raise HTTPException(status_code=400, detail="Could not update course")


# Partial update
@router.patch("/partial-update/{course_id}/")
def partial_update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(auth2.get_current_user)
):
    db_course = db.query(models.CourseModel).filter(
        models.CourseModel.id == course_id
    ).first()

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
        raise HTTPException(status_code=400, detail="Could not partially update course")


# Delete course
@router.delete("/delete/{course_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: models.UserModel = Depends(auth2.get_current_user)):
    db_course = db.query(models.CourseModel).filter(
        models.CourseModel.id == course_id
    ).first()

    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    try:
        db.delete(db_course)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete course")