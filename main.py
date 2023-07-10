from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import  userBase, userDbEngine, userDbSessionLocal
from modals import User, Train, Booking
from typing import Annotated
from uvicorn import run


app = FastAPI()



class Userbase(BaseModel):
    username: str
    password: str
    email: str
    role: str

class Trainbase(BaseModel):
    train_name: str
    source: str
    destination: str
    seat_capacity: int
    arrival_time_at_source: str
    arrival_time_at_destination: str

class Bookingbase(BaseModel):
    user_id: str
    train_id: str
    seats_booked: int




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
    u = User(username=user.username, password=user.password, email=user.email, role=user.role)
    db.add(u)
    db.commit()
    db.refresh(user)
    return {
        "status": "Account successfully created",
        "status_code": 200,
        "user_id": user.user_id
    }

# User Login
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

# Add a New Train (Admin operation)
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

# Get Seat Availability
@app.get("/api/trains/availability")
def get_seat_availability(source: str, destination: str, db: user_db_dependency):
    train_data = db.query(Trainbase).filter(Trainbase.source == source, Trainbase.destination == destination).all()
    return train_data

# # Book a Seat
# @app.post("/api/bookings")
# def book_seat(train_id: str, seats: int, authorized: bool = Depends(get_api_key)):
#     for train in trains_db:
#         if train.train_id == train_id:
#             booked_seats = sum(booking.seats_booked for booking in bookings_db if booking.train_id == train_id)
#             available_seats = train.seat_capacity - booked_seats
#             if available_seats >= seats:
#                 # Create booking record
#                 user_id = "12345"  # Get the user_id from the authenticated user
#                 booking_id = str(len(bookings_db) + 1)  # Generate unique booking ID
#                 booking = Booking(booking_id=booking_id, user_id=user_id, train_id=train_id, seats_booked=seats)
#                 bookings_db.append(booking)
#                 return {
#                     "status": "Booking successful",
#                     "status_code": 200,
#                     "booking_id": booking_id
#                 }
#             else:
#                 raise HTTPException(status_code=400, detail="Insufficient seats available")
#     raise HTTPException(status_code=404, detail="Train not found")

# # Get Specific Booking Details
# @app.get("/api/bookings/{booking_id}")
# def get_booking_details(booking_id: str, authorized: bool = Depends(get_api_key)):
#     for booking in bookings_db:
#         if booking.booking_id == booking_id:
#             return booking
#     raise HTTPException(status_code=404, detail="Booking not found")


if __name__ == "__main__":
    host = "127.0.0.2"  # Set the desired host address
    port = 5000  # Set the desired port number
    
    run("main:app", host=host, port=port)