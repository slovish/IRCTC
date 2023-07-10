from sqlalchemy import Column, Integer, String
from database import userBase


class User(userBase):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, unique= True)
    username = Column(String(20))
    password = Column(String(10))
    email = Column(String(100))
    role = Column(String(10))


class Train(userBase):
    __tablename__ = "trains"
    train_id = Column(Integer, primary_key=True)
    train_name = Column(String(10))
    source = Column(String(10))
    destination = Column(String(10))
    seat_capacity = Column(Integer)
    arrival_time_at_source = Column(String(10))
    arrival_time_at_destination = Column(String(10))


class Booking(userBase):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True)
    user_id = Column(String(10))
    train_id = Column(String(10))
    seats_booked = Column(Integer)
