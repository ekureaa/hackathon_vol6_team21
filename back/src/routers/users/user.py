from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...model.model import User

router = APIRouter()

@router.get("/users")
def read_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/users")
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}")
def update_user(user_id: int, username: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = username
    db_user.email = email
    db_user.password = password
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted"}

@router.post("/users/google-auth")
def google_auth_user(username: str, email: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return existing_user
    db_user = User(username=username, email=email, password="")  # パスワードは空にするか、適切に処理
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/by-email/{email}")
def get_user_id_by_email(email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": db_user.id}