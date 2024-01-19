from sqlalchemy.orm import Session
from typing import Union, List

from schemas.user import UserCreate
from models.user  import User
from utils.crypt  import Crypt



def create_new_user(user: UserCreate, db:Session) -> Union[Union[User, None], bool]:
    res = find_user_by_email(email=user.email, db=db)
    
    if res:
        return None, False

    user = User(
        name = user.name,
        surname = user.surname,
        email = user.email, 
        password = Crypt.get_hash(user.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user, True


def find_user_by_email(email: str, db: Session) :
    res = db.query(User).filter(User.email == email).first()
    return res


def find_all_users(db:Session) -> List[User]:
    res = db.query(User).all()
    return res