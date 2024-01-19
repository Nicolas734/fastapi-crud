from models.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from utils.crypt import Crypt


class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)


    def set_password(self, psw):
        self.password_hash = Crypt.get_hash(psw)

    def check_password(self, psw):
        return Crypt.verify_hash(self.password, psw)