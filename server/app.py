#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, request, jsonify
from flask_restful import Resource
import requests
# Local imports
from config import app, db, api, FLIGHT_API_KEY

# Add your model imports
from models import User, Trip, Activity, Expense, ExpenseUser
from services.flight_api import get_flight_prices
from services.hotel_api import get_city_id, fetch_hotels
# Views go here!

from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env
load_dotenv()

# Get the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

MAKCORPS_API_KEY = "674661a07d3a82d995227011"  
MAKCORPS_BASE_URL = "https://api.makcorps.com"

# User Routes
class Signup(Resource):
    def post(self):
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        try:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            response_body = new_user.to_dict(only=('id', 'name', 'email'))
            return make_response(response_body, 201)
        except:
            response_body = {"error": "Invalid user data provided!"}
            return make_response(response_body, 422)

api.add_resource(Signup, '/signup')

class Login(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            response_body = user.to_dict(only=('id', 'name', 'email'))
            return make_response(response_body, 200)
        else:
            response_body = {"error": "Invalid email or password!"}
            return make_response(response_body, 401)

api.add_resource(Login, '/login')

# Trip Routes
class AllTrips(Resource):
    def get(self):
        trips = Trip.query.all()
        response_body = [trip.to_dict(only=('id', 'name', 'destination', 'start_date', 'end_date')) for trip in trips]
        return make_response(response_body, 200)

    def post(self):
        name = request.json.get('name')
        destination = request.json.get('destination')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        user_id = request.json.get('user_id')
        try:
            new_trip = Trip(name=name, destination=destination, start_date=start_date, end_date=end_date, user_id=user_id)
            db.session.add(new_trip)
            db.session.commit()
            response_body = new_trip.to_dict(only=('id', 'name', 'destination', 'start_date', 'end_date'))
            return make_response(response_body, 201)
        except:
            response_body = {"error": "Invalid trip data provided!"}
            return make_response(response_body, 422)

api.add_resource(AllTrips, '/trips')

class TripByID(Resource):
    def get(self, id):
        trip = Trip.query.get(id)
        if trip:
            response_body = trip.to_dict(only=(
                'id', 'name', 'destination', 'start_date', 'end_date',
                'activities.id', 'activities.name', 'activities.description',
                'expenses.id', 'expenses.amount', 'expenses.description',
            ))
            return make_response(jsonify(response_body), 200)
        else:
            return make_response({"error": "Trip not found!"}, 404)
        
    def put(self, id):
        trip = Trip.query.get(id)
        if trip:
            try:
                for attr in request.json:
                    setattr(trip, attr, request.json.get(attr))
                db.session.commit()
                response_body = trip.to_dict(only=('id', 'name', 'destination', 'start_date', 'end_date'))
                return make_response(response_body, 200)
            except:
                response_body = {"error": "Invalid trip data provided!"}
                return make_response(response_body, 422)
        else:
            response_body = {"error": "Trip not found!"}
            return make_response(response_body, 404)

    def delete(self, id):
        trip = Trip.query.get(id)
        if trip:
            db.session.delete(trip)
            db.session.commit()
            return make_response({}, 204)
        else:
            response_body = {"error": "Trip not found!"}
            return make_response(response_body, 404)

api.add_resource(TripByID, '/trips/<int:id>')

# Activity Routes
class TripActivities(Resource):
    def get(self, trip_id):
        activities = Activity.query.filter_by(trip_id=trip_id).all()
        response_body = [activity.to_dict(only=('id', 'name', 'description', 'location', 'time')) for activity in activities]
        return make_response(response_body, 200)

    def post(self, trip_id):
        name = request.json.get('name')
        description = request.json.get('description')
        location = request.json.get('location')
        time = request.json.get('time')
        try:
            new_activity = Activity(name=name, description=description, location=location, time=time, trip_id=trip_id)
            db.session.add(new_activity)
            db.session.commit()
            response_body = new_activity.to_dict(only=('id', 'name', 'description', 'location', 'time'))
            return make_response(response_body, 201)
        except:
            response_body = {"error": "Invalid activity data provided!"}
            return make_response(response_body, 422)

api.add_resource(TripActivities, '/trips/<int:trip_id>/activities')

class ActivityByID(Resource):
    def put(self, id):
        activity = Activity.query.get(id)
        if activity:
            try:
                for attr in request.json:
                    setattr(activity, attr, request.json.get(attr))
                db.session.commit()
                response_body = activity.to_dict(only=('id', 'name', 'description', 'location', 'time'))
                return make_response(response_body, 200)
            except:
                response_body = {"error": "Invalid activity data provided!"}
                return make_response(response_body, 422)
        else:
            response_body = {"error": "Activity not found!"}
            return make_response(response_body, 404)

    def delete(self, id):
        activity = Activity.query.get(id)
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return make_response({}, 204)
        else:
            response_body = {"error": "Activity not found!"}
            return make_response(response_body, 404)

api.add_resource(ActivityByID, '/activities/<int:id>')

# Expense Routes
class TripExpenses(Resource):
    def get(self, trip_id):
        expenses = Expense.query.filter_by(trip_id=trip_id).all()
        response_body = [expense.to_dict(only=('id', 'amount', 'description')) for expense in expenses]
        return make_response(response_body, 200)

    def post(self, trip_id):
        amount = request.json.get('amount')
        description = request.json.get('description')
        try:
            new_expense = Expense(amount=amount, description=description, trip_id=trip_id)
            db.session.add(new_expense)
            db.session.commit()
            response_body = new_expense.to_dict(only=('id', 'amount', 'description'))
            return make_response(response_body, 201)
        except:
            response_body = {"error": "Invalid expense data provided!"}
            return make_response(response_body, 422)

api.add_resource(TripExpenses, '/trips/<int:trip_id>/expenses')

class ExpenseByID(Resource):
    def put(self, id):
        expense = Expense.query.get(id)
        if expense:
            try:
                for attr in request.json:
                    setattr(expense, attr, request.json.get(attr))
                db.session.commit()
                response_body = expense.to_dict(only=('id', 'amount', 'description'))
                return make_response(response_body, 200)
            except:
                response_body = {"error": "Invalid expense data provided!"}
                return make_response(response_body, 422)
        else:
            response_body = {"error": "Expense not found!"}
            return make_response(response_body, 404)

    def delete(self, id):
        expense = Expense.query.get(id)
        if expense:
            db.session.delete(expense)
            db.session.commit()
            return make_response({}, 204)
        else:
            response_body = {"error": "Expense not found!"}
            return make_response(response_body, 404)

api.add_resource(ExpenseByID, '/expenses/<int:id>')

@app.route('/api/generate_itinerary', methods=['POST'])
def generate_itinerary_route():
    # data = request.json
    # destination = data.get("destination")
    # duration = data.get("duration")
    # interests = data.get("interests")
    
    itinerary = generate_itinerary()
    if itinerary:
        return jsonify({"itinerary": itinerary}), 200
    else:
        return jsonify({"error": "Failed to generate itinerary"}), 500


@app.route('/api/roundtrip', methods=['GET'])
def roundtrip():
    # Get query parameters
    departure_airport_code = request.args.get("departure_airport_code")
    arrival_airport_code = request.args.get("arrival_airport_code")
    departure_date = request.args.get("departure_date")
    arrival_date = request.args.get("arrival_date")
    number_of_adults = request.args.get("number_of_adults", 1)
    number_of_childrens = request.args.get("number_of_childrens", 0)
    number_of_infants = request.args.get("number_of_infants", 0)
    cabin_class = request.args.get("cabin_class", "Economy")
    currency = request.args.get("currency", "USD")
    region = request.args.get("region", "US")

    # Validate required parameters
    if not departure_airport_code or not arrival_airport_code or not departure_date or not arrival_date:
        return jsonify({"error": "Missing required query parameters"}), 400

    try:
        # Fetch data using the get_flight_prices function
        flight_data = get_flight_prices(
            departure_airport_code, 
            arrival_airport_code, 
            departure_date, 
            arrival_date, 
            number_of_adults, 
            number_of_childrens, 
            number_of_infants, 
            cabin_class, 
            currency, 
            region
        )

        # if not flight_data:
        #     return jsonify({"error": "Unable to fetch flight data"}), 500

        # Simplify the response
        simplified_data = []
        itineraries = flight_data.get("itineraries", [])
        legs = {leg["id"]: leg for leg in flight_data.get("legs", [])}
        segments = {segment["id"]: segment for segment in flight_data.get("segments", [])}

        for itinerary in itineraries[:10]:  # Limit to 10 results
            pricing_option = itinerary.get("pricing_options", [{}])[0]
            price_info = pricing_option.get("price", {})
            leg_ids = itinerary.get("leg_ids", [])

            for leg_id in leg_ids:
                leg = legs.get(leg_id, {})

                # Collect segment-level details (optional)
                flight_numbers = []
                operating_carriers = []
                modes = []

                for segment_id in leg.get("segment_ids", []):
                    segment = segments.get(segment_id, {})
                    flight_numbers.append(segment.get("marketing_flight_number"))
                    operating_carriers.append(segment.get("operating_carrier_id"))
                    modes.append(segment.get("mode"))

                # Add the leg to the simplified data, avoiding duplication
                simplified_data.append({
                    "price": price_info.get("amount"),
                    "currency": price_info.get("currency"),
                    "departure": leg.get("departure"),
                    "arrival": leg.get("arrival"),
                    "duration_minutes": leg.get("duration"),
                    "stops": leg.get("stop_count"),
                    "flight_numbers": flight_numbers,  # Include all segment flight numbers
                    "operating_carrier_ids": operating_carriers,  # Include all carrier IDs
                    "modes": modes  # Include all transport modes
                })

        # Return the simplified data
        return jsonify(simplified_data), 200

    except requests.exceptions.RequestException as e:
        print("Error fetching flight data:", e)
        return jsonify({"error": "Unable to fetch flight data"}), 500
    except KeyError as e:
        print("Missing key in response:", e)
        return jsonify({"error": "Unexpected API response format"}), 500
    

@app.route('/generate-itinerary', methods=['GET'])
def generate_itinerary():
    
    destination = request.args.get("destination", "Paris")
    duration = request.args.get("duration", 1)
    interests = request.args.get("interests", "art museums")

    try:
        # Call OpenAI API with minimal token usage
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a travel assistant."},
                {"role": "user", "content": (
                    f"Generate a {duration}-day itinerary for {destination} focusing on {interests}. Answer by doing a list of activities. Only this "
                )}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Extract the AI-generated content
        itinerary = response.choices[0].message['content']
        return jsonify({"itinerary": itinerary}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# @app.route('/api/get_city_id', methods=['GET'])
# def api_get_city_id():
#     """
#     API route to fetch the city ID for a given city name.
#     """
#     # city_name = request.args.get("city_name")
#     # if not city_name:
#     #     return make_response({"error": "City name is required"}, 400)
    
#     city_id = get_city_id(
#         # city_name
#         )
#     if city_id:
#         return jsonify({"city_id": city_id}), 200
#     else:
#         return jsonify({"error": "City not found or invalid API key"}), 404


@app.route('/api/get_hotels', methods=['GET'])
def api_get_hotels():
    """
    API route to fetch hotels in a city for given check-in and check-out dates.
    """
    city_name = request.args.get("city_name")
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")
    rooms = request.args.get("rooms", 1, type=int)
    adults = request.args.get("adults", 2, type=int)
    children = request.args.get("children", 0, type=int)
    pagination = request.args.get("pagination", 0, type=int)
    currency = request.args.get("currency", "USD")
    
    # if not city_name or not checkin or not checkout:
    #     return make_response({"error": "City name, checkin, and checkout dates are required"}, 400)

    # Get the city ID
    city_id = get_city_id(
        city_name
    )
    # if not city_id:
    #     return jsonify({"error": "City not found"}), 404

    # Fetch hotels
    hotels = fetch_hotels( city_id, checkin, checkout, pagination, currency, rooms, adults, children)
    return jsonify(hotels), 200



@app.route('/')
def index():
    return '<h1>Travel Planner Server</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
