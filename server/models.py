from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db


class Trip(db.Model, SerializerMixin):
    __tablename__ = "trips"
    serialize_rules = ("-user", "-activities.trip", "-expenses.trip")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='trips')

    activities = db.relationship('Activity', back_populates='trip', cascade="all, delete-orphan")
    expenses = db.relationship('Expense', back_populates='trip', cascade="all, delete-orphan")


class Activity(db.Model, SerializerMixin):
    __tablename__ = "activities"
    serialize_rules = ("-trip.activities",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    location = db.Column(db.String, nullable=True)
    time = db.Column(db.DateTime, nullable=False)

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='activities')

class Expense(db.Model, SerializerMixin):
    __tablename__ = "expenses"
    serialize_rules = ("-trip.expenses", "-users.expenses")  

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='expenses')

    users = db.relationship('ExpenseUser', back_populates='expense')  # Corrected relationship


class ExpenseUser(db.Model, SerializerMixin):
    __tablename__ = "expense_users"

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    expense = db.relationship('Expense', back_populates='users')
    user = db.relationship('User', back_populates='expenses')  # Fixed back_populates


class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_rules = ("-trips.user", "-expenses.user") 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    trips = db.relationship('Trip', back_populates='user')
    expenses = db.relationship('ExpenseUser', back_populates='user')  # Adjusted relationship


