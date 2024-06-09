from datetime import datetime, timezone, timedelta
from typing import Optional
from jwt import InvalidTokenError
import jwt
from passlib.context import CryptContext
import re

SECRET_KEY = "ToiDaFakeHon250kGDC"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_type: str = payload.get("type")
        cccd: str = payload.get("cccd")
        if username is None or user_type is None:
            return None
        return {"username": username, "type": user_type, "cccd": cccd}
    except InvalidTokenError:
        return None

def validate_cccd(cccd):
    if not re.fullmatch(r'\d{12}', cccd):
        return False

    province_code = int(cccd[:3])
    if province_code < 1 or province_code > 96:
        return False

    gender_century_code = int(cccd[3])
    if gender_century_code not in range(0, 10):
        return False

    birth_year_code = int(cccd[4:6])
    if birth_year_code < 0 or birth_year_code > 99:
        return False

    return True