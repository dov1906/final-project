from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    trips = db.relationship('Trip', back_populates='user')

    @validates('name')
    def validate_name(self, column, value):
        if isinstance(value, str) and len(value) >= 3:
            return value
        raise ValueError(f"{column} must be a string at least 3 characters long!")

    @validates('email')
    def validate_email(self, column, value):
        if '@' in value and '.' in value:
            return value
        raise ValueError(f"{column} must be a valid email address!")


# class Trip(db.Model, SerializerMixin):
#     __tablename__ = "trips"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     destination = db.Column(db.String, nullable=False)
#     start_date = db.Column(db.Date, nullable=False)
#     end_date = db.Column(db.Date, nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user = db.relationship('User', back_populates='trips')

#     activities = db.relationship('Activity', back_populates='trip', cascade="all, delete-orphan")
#     expenses = db.relationship('Expense', back_populates='trip', cascade="all, delete-orphan")

#     @validates('name', 'destination')
#     def validate_strings(self, column, value):
#         if isinstance(value, str) and len(value) >= 3:
#             return value
#         raise ValueError(f"{column} must be a string at least 3 characters long!")


class Activity(db.Model, SerializerMixin):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    location = db.Column(db.String, nullable=True)
    time = db.Column(db.DateTime, nullable=False)

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='activities')

    @validates('name')
    def validate_name(self, column, value):
        if isinstance(value, str) and len(value) >= 3:
            return value
        raise ValueError(f"{column} must be a string at least 3 characters long!")

class Expense(db.Model, SerializerMixin):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', back_populates='expenses')

    users = db.relationship('ExpenseUser', back_populates='expense', cascade="all, delete-orphan")

    @validates('amount')
    def validate_amount(self, column, value):
        if isinstance(value, (float, int)) and value > 0:
            return value
        raise ValueError(f"{column} must be a positive number!")

class ExpenseUser(db.Model, SerializerMixin):
    __tablename__ = "expense_users"

    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    expense = db.relationship('Expense', back_populates='users')
    user = db.relationship('User')

    @validates('expense_id', 'user_id')
    def validate_foreign_keys(self, column, value):
        if isinstance(value, int):
            return value
        raise ValueError(f"{column} must be an integer!")

