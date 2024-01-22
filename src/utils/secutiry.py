from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

from utils.config import Config

config = Config()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config._g.getint("JWT", "EXPIRE_MINUTES"))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, config._g.get("JWT", "SECRET_KEY"), algorithm=config._g.get("JWT", "ALGORITHM"))
    return encoded_jwt