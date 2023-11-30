# Travel Company API

This repository contains the source code for the Travel Company API, a Flask-based web application that allows users to query available houses, book stays, and manage user registrations and logins.

## Code Repository

The source code for this project can be found on [GitHub](https://github.com/your-username/your-repo).

## Design

### Project Structure

The project structure is organized as follows:

- **app/**
  - **\_\_init\_\_.py:** Initialization of Flask app and configuration.
  - **routes.py:** Definition of API routes and resources.
  - **models.py:** SQLAlchemy models for database tables.
  - **static/swagger.json:** Swagger API documentation.
- **config.py:** Configuration settings, including database connection.
- **run.py:** Main script to run the Flask app.
- **README.md:** Documentation for the project.

### Data Model (ER Diagram)

![diagram](https://github.com/omerdikyol/dy_api_for_travel_company/assets/41495154/0eb9163c-5a1b-47e4-94f9-2da1be2a789a)

### Assumptions and Design Choices

- The project assumes the use of a Microsoft SQL Server database for storing house, booking, and user information.
- JWT (JSON Web Token) is used for user authentication.
- Flask-RESTful is employed for building the API.
- Swagger UI is integrated for API documentation.

### Issues Encountered

1. **Database Connection Issue:**
   - *Description:* Challenges were faced during the establishment of a connection to the Microsoft SQL Server database using SQLAlchemy and PyODBC.
   - *Resolution:* Ensure the correctness of the database connection string in `config.py`. Verify credentials, server address, and driver compatibility.

2. **Date Formatting in API Requests:**
   - *Description:* The API expects date parameters in the format 'YYYY-MM-DD', and incorrect date formats may result in errors.
   - *Resolution:* Clearly document the expected date format in API requests to prevent user errors. Implement additional validation for date inputs.

3. **User Authentication Flow:**
   - *Description:* The user authentication flow might be confusing for new contributors or users of the API.
   - *Resolution:* Add comments in the authentication-related routes to clarify the flow. Consider documenting the expected authentication headers in the README.

4. **Swagger Documentation Update:**
   - *Description:* The Swagger API documentation might not be up-to-date with the latest changes in the API routes or data models.
   - *Resolution:* Regularly update the Swagger documentation to reflect any changes in the API. Consider automating this process if possible.

## Functionality

The API provides the following functionality:

- **QueryHouses:** Retrieve available houses based on date, number of people, and pagination.

- **BookStay:** Allow authenticated users to book stays for specified dates and names.

- **UserRegistration:** Register new users.

- **UserLogin:** Authenticate and log in existing users.

## Database Connection

The application connects to a Microsoft Azure SQL Server database using SQLAlchemy and PyODBC.

## How to Run

1. Clone the repository: `git clone https://github.com/your-username/your-repo.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure the database connection in `config.py`.
4. Run the application: `python run.py`

## Video Presentation

[Include a link to a short video presentation of your project, e.g., on YouTube or another cloud storage service.]
