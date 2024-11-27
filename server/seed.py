#!/usr/bin/env python3

# Standard library imports
from random import randint
from datetime import date, datetime

# Local imports
from app import app
from models import db, User, Trip, Activity, Expense

if __name__ == '__main__':
    with app.app_context():
        print("🌱 Starting seed... 🌱")

       
        User.query.delete()
        Trip.query.delete()
        Activity.query.delete()
        Expense.query.delete()

        user1 = User(name="Alice Johnson", email="alice@example.com", password="password123")
        user2 = User(name="Bob Smith", email="bob@example.com", password="securepassword")

        trip1 = Trip(
            name="Hawaiian Adventure",
            destination="Hawaii, USA",
            start_date=date(2024, 12, 1), 
            end_date=date(2024, 12, 10),  
            user_id=1
        )
        trip2 = Trip(
            name="Paris Getaway",
            destination="Paris, France",
            start_date=date(2024, 12, 15), 
            end_date=date(2024, 12, 20),  
            user_id=2
        )

        activity1 = Activity(
            name="Snorkeling",
            description="Explore the coral reefs",
            location="Maui Beach",
            time=datetime(2024, 12, 2, 10, 0, 0),
            trip_id=1
        )
        activity2 = Activity(
            name="Wine Tasting",
            description="Enjoy the finest wines",
            location="Chateau de France",
            time=datetime(2024, 12, 16, 14, 0, 0),  
            trip_id=2
        )

        expense1 = Expense(amount=150.00, description="Snorkeling gear rental", trip_id=1)
        expense2 = Expense(amount=300.00, description="Wine tasting tour", trip_id=2)

       
        db.session.add_all([user1, user2, trip1, trip2, activity1, activity2, expense1, expense2])
        db.session.commit()

        print("🌱 Users, Trips, Activities, and Expenses successfully seeded! 🌱")
