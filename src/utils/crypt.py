from passlib.context import CryptContext


context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Crypt():
    @staticmethod
    def verify_hash(value, hash_value):
        return context.verify(value, hash_value)
    
    @staticmethod
    def get_hash(value):
        return context.hash(value)