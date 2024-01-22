from utils.secutiry import create_access_token
from sqlalchemy.orm import Session
from service.user import find_user_by_email
from utils.crypt import Crypt
from typing import Union
from models.user import User



def authenticate_user(email: str, password: str, db: Session) -> Union[User, bool]:
    user = find_user_by_email(email=email, db=db)
    if not user:
        return False
    if not Crypt.verify_hash(password, user.password):
        return False
    return user
