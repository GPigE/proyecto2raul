from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.user import User
from auth.password import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from auth.token import create_access_token
from auth.password import verify_password
from fastapi import Response, Depends
from jose import JWTError
from fastapi import Request
from auth.token import decode_token

router = APIRouter()

@router.post("/register")
def register(name: str, username: str, password: str):
    with Session(engine) as session:
        
        userExists = session.exec(select(User).where(User.username == username)).first()

        if userExists:
          raise HTTPException(status_code=400, detail="Username already exists")

        user = User(
            name=name,
            username=username,
            password_hash=hash_password(password)
        )

        session.add(user)
        session.commit()

        return {"system": "user created"}
    
@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        
        user = session.exec(
            select(User).where(User.username == form_data.username)
        ).first()

        if not user or not verify_password(user.password_hash, form_data.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.username})

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=180
        )

        return {"access_token": token, "token_type": "bearer"}
    
@router.get("/users/me")
def get_current_user(request: Request):
    token = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    if not token:
        token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(token)
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "name": user.name,
            "username": user.username,
            "password_hash": user.password_hash
        }