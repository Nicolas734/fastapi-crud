from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from fastapi import status,HTTPException


from db.db import get_db
from schemas.token import Token
from api.auth import authenticate_user
from utils.secutiry import create_access_token

router = APIRouter()



@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    data = {"name":user.name, "email":user.email}
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type":"bearer"}