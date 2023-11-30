from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash
from app.models import House, Booking, User
from flask_restful import Api
from app import db
from datetime import datetime

bp = Blueprint('main', __name__)
api = Api(bp)  # Create api object with bp

# API Resources
class QueryHouses(Resource):
  # Query houses with date, from, to and number of people
  # Return list of houses with their descriptions, amenities. Must support paging
  # No authentication needed
  def post(self):
    # Get query parameters
    parser = reqparse.RequestParser()
    parser.add_argument("from", type=str, help="From date is required", required=True)
    parser.add_argument("to", type=str, help="To date is required", required=True)
    parser.add_argument("people", type=int, help="Number of people is required", required=True)
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("limit", type=int, default=10)

    args = parser.parse_args()


    from_, to, people, page, limit = (
        args["from"],
        args["to"],
        args["people"],
        args["page"],
        args["limit"],
    )

    # Check if the dates are valid
    try:
        datetime_from = datetime.strptime(from_, '%Y-%m-%d')
        datetime_to = datetime.strptime(to, '%Y-%m-%d')
    except ValueError:
        # If ValueError is raised, the input is not a valid date
        return {"message": "Invalid date format."}, 400

    if (people < 1):
        return {"message": "Invalid number of people."}, 400
    
    if (page < 1):
        return {"message": "Invalid page number."}, 400
    
    if (limit < 1):
        return {"message": "Invalid limit."}, 400
    
    # Check if from date is before to date
    datetime_date1 = datetime.strptime(from_, '%Y-%m-%d')
    datetime_date2 = datetime.strptime(to, '%Y-%m-%d')

    if (datetime_date1 > datetime_date2):
        return {"message": "From date should be before to date."}, 400

    
    # Query database for available houses using SQLAlchemy
    available_houses = (
        House.query.filter(House.capacity >= people)
        .filter(
            ~db.session.query(Booking)
            .filter(Booking.house_id == House.id)
            .filter(Booking.date_from <= from_)
            .filter(Booking.date_to >= to)
            .exists()
        )
        .order_by(House.id)
        .paginate(page=page, per_page=limit)
    )

    # Format response as a list of houses
    houses = [
        {
            "id": house.id,
            "description": house.description,
            "amenities": house.amenities,
            "city": house.city,
            "capacity": house.capacity,
        }
        for house in available_houses.items
    ]

    return {
        "houses": houses,
        "total_results": available_houses.total,
        "current_page": available_houses.page,
        "total_pages": available_houses.pages,
    }, 200

class BookStay(Resource):
  # Perform booking using dates, from, to, names
  # If houses is queried again for given dates, it should not be available
  # Return status
  # Authentication by username/password needed
  @jwt_required()
  def post(self):
    # Get query parameters
    parser = reqparse.RequestParser()
    parser.add_argument("house_id", type=int, help="House ID is required", required=True)
    parser.add_argument("from", type=str, help="From date is required", required=True)
    parser.add_argument("to", type=str, help="To date is required", required=True)
    parser.add_argument("names", type=list, help="Names are required", required=True)

    args = parser.parse_args()

    house_id, from_, to, names = (
        args["house_id"],
        args["from"],
        args["to"],
        args["names"],
    )


    # Check if the dates are valid
    try:
        datetime_from = datetime.strptime(from_, '%Y-%m-%d')
        datetime_to = datetime.strptime(to, '%Y-%m-%d')
    except ValueError:
        # If ValueError is raised, the input is not a valid date
        return {"message": "Invalid date format"}, 400
    
    # Check if from date is before to date
    datetime_date1 = datetime.strptime(from_, '%Y-%m-%d')
    datetime_date2 = datetime.strptime(to, '%Y-%m-%d')

    if (datetime_date1 > datetime_date2):
        return {"message": "From date should be before to date."}, 400

    if (house_id < 1):
        return {"message": "Invalid house id."}, 400

    if (not names):
        return {"message": "User should enter names."}, 400

    # Check if the house is available for booking using SQLAlchemy
    house_available = (
        House.query.filter(House.id == house_id)
        .filter(
            ~db.session.query(Booking)
            .filter(Booking.house_id == house_id)
            .filter(Booking.date_from <= from_)
            .filter(Booking.date_to >= to)
            .exists()
        )
        .first()
    )

    if not house_available:
        return {"message": "House is not available for booking"}, 404

    # Check if the house capacity is enough for names
    if len(names) > house_available.capacity:
        return {"message": "House capacity is not enough for booking"}, 400

    # Insert booking into the database using SQLAlchemy
    new_booking = Booking(
        house_id=house_id,
        date_from=from_,
        date_to=to,
        names=",".join(names),
    )
    db.session.add(new_booking)
    db.session.commit()

    # Return success message
    return {"message": "Booking successful"}, 201

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)

        data = parser.parse_args()

        # Check if the username already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return {'message': 'User already exists'}, 400

        # Create a new user
        new_user = User(username=data['username'], password_hash=generate_password_hash(data['password'], method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=data['username'])

        return {
            'message': 'User registration successful',
            'access_token': access_token
        }, 201
    
class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)

        data = parser.parse_args()

        # Check if the user exists
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': 'User does not exist'}, 400

        # Check if the password is correct
        if not user.check_password(data['password']):
            return {'message': 'Password is incorrect'}, 400

        # Create access token
        access_token = create_access_token(identity=data['username'])

        return {
            'message': 'User login successful',
            'access_token': access_token
        }, 200

api.add_resource(QueryHouses, '/api/v1/query_houses')
api.add_resource(BookStay, '/api/v1/book_stay')
api.add_resource(UserRegistration, '/api/v1/register')
api.add_resource(UserLogin, '/api/v1/login')