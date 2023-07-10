from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import  userBase, userDbEngine, userDbSessionLocal
from modals import User, Train
from typing import Annotated
from uvicorn import run


app = FastAPI()


class Userbase(BaseModel):
    user_id : int
    username: str
    password: str
    email: str
    role: str

class Trainbase(BaseModel):
    train_id : int
    train_name: str
    source: str
    destination: str
    seat_capacity: int
    arrival_time_at_source: str
    arrival_time_at_destination: str

# class Bookingbase(BaseModel):
#     user_id: str
#     train_id: str
#     seats_booked: int




userBase.metadata.create_all(bind = userDbEngine)
# trainBase.metadata.create_all(bind = trainDbEngine)
def get_user_db():
    userDb = userDbSessionLocal()
    try:
        yield userDb
    finally:
        userDb.close()
# def get_train_db():
#     trainDb = userDbSessionLocal()
#     try:
#         yield trainDb
#     finally:
#         trainDb.close()

user_db_dependency = Annotated[Session, Depends(get_user_db())]
# train_db_dependency = Annotated[Session, Depends(get_train_db)]


@app.post("/api/signup")
def signup(user: Userbase, db:user_db_dependency):
    user = dict(user)
    u = User(username=user.username, password=user.password, email=user.email, role=user.role)
    db.add(u)
    db.commit()
    db.refresh(user)
    return {
        "status": "Account successfully created",
        "status_code": 200,
        "user_id": user.user_id
    }

@app.post("/api/login")
def login(username: str, password: str, db:user_db_dependency):
    user_data = db.query(Userbase).filter(Userbase.username == username, Userbase.password == password).first()

    if user_data:
        return {
            "status": "Login successful",
            "status_code": 200,
            "user_id": user_data.user_id,
            "access_token": "dummy_access_token"
        }
    else:
        raise HTTPException(status_code=401, detail="Incorrect username/password provided")

@app.post("/api/trains/create")
def create_train(train: Trainbase, db: user_db_dependency):
    train = Train
    db.add(train)
    db.commit()
    db.refresh(train)
    return {
        "message": "Train added successfully",
        "train_id": train.train_id
    }

@app.get("/api/trains/availability")
def get_seat_availability(source: str, destination: str, db: user_db_dependency):
    train_data = db.query(Trainbase).filter(Trainbase.source == source, Trainbase.destination == destination).all()
    return train_data


if __name__ == "__main__":
    host = "127.0.0.2"  # Set the desired host address
    port = 5000  # Set the desired port number
    
    run("main:app", host=host, port=port)