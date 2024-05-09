from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import SECRET_KEY
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from app import models


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        print("Token:", token)  # Add this line for debugging

        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = models.users.User().get_by_id(data["user_id"])

            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

        except jwt.ExpiredSignatureError:
            return {
                "message": "Token has expired. Please log in again.",
                "data": None,
                "error": "Unauthorized"
            }, 401

        except jwt.InvalidTokenError:
            return {
                "message": "Invalid token. Please log in again.",
                "data": None,
                "error": "Unauthorized"
            }, 401

        return f(current_user, *args, **kwargs)

    return decorated


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

"""def issue_token(subject, scope: str, expire_minutes: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "scope": scope,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt"""