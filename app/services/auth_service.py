import bcrypt
from tortoise.exceptions import DoesNotExist

from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self):
        self.salt = bcrypt.gensalt()

    async def register_user(self, user_data: UserCreate) -> User:
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), self.salt).decode('utf-8')
        user = await User.create(
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name
        )
        return user

    async def authenticate_user(self, email: str, password: str) -> User | None:
        try:
            user = await User.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return user
            return None
        except DoesNotExist:
            return None