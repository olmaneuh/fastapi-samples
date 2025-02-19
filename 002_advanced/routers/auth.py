from datetime import timedelta, datetime, timezone
from db import SessionMaker
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User, UserCreateUpdateRequest, Token
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["auth"])

ALGORITHM = "HS256"
SECRET_KEY = "b4e7c44ed9652976e696a3648754d0f9d93b5cccc0d3ecde4e0a92a3c3b8cf34"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


# provides a new SQLAlchemy session
def get_db():
    db = SessionMaker()  # create a new database session
    try:
        yield db  # provide it to the request handler
    finally:
        db.close()  # close the session after request is done


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: UserCreateUpdateRequest):
    user = User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        hashed_password=bcrypt_context.hash(request.password),
        is_active=True,
        role=request.role,
    )

    db.add(user)
    db.commit()


@router.post("/token", response_model=Token)
async def access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not valid."
        )
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )
    return {"access_token": token, "type": "bearer"}


# utility methods
def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not valid."
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not valid."
        )
