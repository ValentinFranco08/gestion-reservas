# Contenido anterior de app/models.py, ahora en app/models/booking_model.py
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.name}>'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', backref='room', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Room {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Booking {self.room.name} by {self.user.name} from {self.start_time} to {self.end_time}>'

    @staticmethod
    def is_time_slot_available(room_id, start_time, end_time, current_booking_id=None):
        if start_time >= end_time:
            return False, "La hora de inicio debe ser anterior a la hora de fin."
        
        overlapping_bookings = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.end_time > start_time,
            Booking.start_time < end_time
        )
        
        if current_booking_id:
            overlapping_bookings = overlapping_bookings.filter(Booking.id != current_booking_id)
            
        if overlapping_bookings.first():
            return False, "La sala ya está reservada en este horario. Por favor, elige otro horario."
        return True, ""