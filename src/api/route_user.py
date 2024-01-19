from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, Response, HTTPException, status
from typing import List
from schemas.user import UserCreate, ResponseCreateUser, ResponseGetUser
from db.db import get_db
from service.user import create_new_user, find_all_users


router = APIRouter()

@router.post(path="/create", status_code=status.HTTP_200_OK, response_model=ResponseCreateUser)
def create(res: Response, user: UserCreate, db:Session = Depends(get_db)):
    user, ret = create_new_user(user=user, db=db)
    if not user and not ret:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already registered. Please choose a different email."
        )
    return user


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ResponseGetUser])
def all_users(db: Session = Depends(get_db)):
    users =  find_all_users(db)
    return users
