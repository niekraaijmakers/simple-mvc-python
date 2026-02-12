"""
Car Repository - Data access layer for Car entities
This is the REPOSITORY PATTERN

RESPONSIBILITY:
- Abstract database operations (CRUD)
- Provide collection-like interface to access data
- Business logic and validation
- Complex queries

The Repository Pattern sits between the Controller and Model:
Controller -> Repository -> Model -> Database
"""
from model.car import Car, db


class CarRepository:
    """
    Repository class for Car data access
    
    The Repository pattern provides a collection-like interface for accessing
    domain objects. It encapsulates the logic required to access data sources.
    
    Controllers should call these methods instead of directly manipulating
    the database or model.
    """
    
    @staticmethod
    def create(make, model, year, color, price):
        """
        Create a new car and persist it to the database
        
        Args:
            make (str): Car manufacturer
            model (str): Car model
            year (int): Manufacturing year
            color (str): Car color
            price (float): Car price
            
        Returns:
            Car: The newly created car instance
            
        Raises:
            ValueError: If validation fails
        """
        # Validation logic (business rules)
        CarRepository._validate_car_data(make, model, year, color, price)
        
        # Create a new Car instance (in memory, not yet in database)
        new_car = Car(make=make, model=model, year=year, color=color, price=price)
        
        # Add the car to the database session (stages it for insertion)
        # This is equivalent to: INSERT INTO cars (...) VALUES (...)
        db.session.add(new_car)
        
        # Execute the insert operation and save to database
        db.session.commit()
        
        return new_car
    
    @staticmethod
    def find_all():
        """
        Retrieve all cars from the database
        
        Returns:
            list[Car]: List of all car instances
        """
        # Explicitly query the database session for all Car records
        # This is equivalent to: SELECT * FROM cars
        return db.session.query(Car).all()
    
    @staticmethod
    def find_by_id(car_id):
        """
        Find a specific car by its ID
        
        Args:
            car_id (int): The car's ID
            
        Returns:
            Car: The car instance
            
        Raises:
            404: If car not found
        """
        # Explicitly get a Car record by primary key (ID)
        # This is equivalent to: SELECT * FROM cars WHERE id = ?
        car = db.session.get(Car, car_id)
        
        # If not found, raise a 404 error
        if car is None:
            from flask import abort
            abort(404)
        
        return car
    
    @staticmethod
    def update(car_id, make=None, model=None, year=None, color=None, price=None):
        """
        Update an existing car's attributes
        
        Args:
            car_id (int): The car's ID
            make (str, optional): New manufacturer
            model (str, optional): New model
            year (int, optional): New year
            color (str, optional): New color
            price (float, optional): New price
            
        Returns:
            Car: The updated car instance
            
        Raises:
            ValueError: If validation fails
            404: If car not found
        """
        # First, get the car from the database
        car = db.session.get(Car, car_id)
        if car is None:
            from flask import abort
            abort(404)
        
        # Update only provided fields
        if make is not None:
            car.make = make
        if model is not None:
            car.model = model
        if year is not None:
            CarRepository._validate_year(year)
            car.year = year
        if color is not None:
            car.color = color
        if price is not None:
            CarRepository._validate_price(price)
            car.price = price
        
        # Save changes to the database
        # SQLAlchemy tracks changes to objects and updates them on commit
        db.session.commit()
        return car
    
    @staticmethod
    def delete(car_id):
        """
        Delete a car from the database
        
        Args:
            car_id (int): The car's ID
            
        Returns:
            dict: Information about the deleted car
            
        Raises:
            404: If car not found
        """
        # First, get the car from the database
        car = db.session.get(Car, car_id)
        if car is None:
            from flask import abort
            abort(404)
        
        # Save info before deleting
        car_info = {
            'id': car.id,
            'full_name': car.full_name,
            'make': car.make,
            'model': car.model,
            'year': car.year
        }
        
        # Mark the car for deletion
        # This is equivalent to: DELETE FROM cars WHERE id = ?
        db.session.delete(car)
        
        # Execute the delete operation
        db.session.commit()
        
        return car_info
    
    @staticmethod
    def find_by_make(make):
        """
        Find all cars from a specific manufacturer
        
        Args:
            make (str): The manufacturer name
            
        Returns:
            list[Car]: List of cars from that manufacturer
        """
        # Query the database with a WHERE clause
        # This is equivalent to: SELECT * FROM cars WHERE make = ?
        return db.session.query(Car).filter_by(make=make).all()
    
    @staticmethod
    def find_expensive_cars(min_price=40000):
        """
        Find all cars above a certain price
        
        Args:
            min_price (float): Minimum price threshold
            
        Returns:
            list[Car]: List of expensive cars
        """
        # Query with a comparison operator
        # This is equivalent to: SELECT * FROM cars WHERE price >= ?
        return db.session.query(Car).filter(Car.price >= min_price).all()
    
    @staticmethod
    def find_by_year_range(start_year, end_year):
        """
        Find all cars within a year range
        
        Args:
            start_year (int): Starting year (inclusive)
            end_year (int): Ending year (inclusive)
            
        Returns:
            list[Car]: List of cars in that year range
        """
        # Query with multiple conditions (AND)
        # This is equivalent to: SELECT * FROM cars WHERE year >= ? AND year <= ?
        return db.session.query(Car).filter(
            Car.year >= start_year,
            Car.year <= end_year
        ).all()
    
    @staticmethod
    def count():
        """
        Count total number of cars in the database
        
        Returns:
            int: Total count of cars
        """
        # Count all cars in the database
        # This is equivalent to: SELECT COUNT(*) FROM cars
        return db.session.query(Car).count()
    
    @staticmethod
    def exists(car_id):
        """
        Check if a car exists
        
        Args:
            car_id (int): The car's ID
            
        Returns:
            bool: True if car exists, False otherwise
        """
        # Query for a car with this ID and get the first result (or None)
        # This is equivalent to: SELECT * FROM cars WHERE id = ? LIMIT 1
        car = db.session.query(Car).filter_by(id=car_id).first()
        return car is not None
    
    # Private validation methods
    
    @staticmethod
    def _validate_car_data(make, model, year, color, price):
        """
        Validate all car data before creating/updating
        
        Raises:
            ValueError: If any validation fails
        """
        if not make or not make.strip():
            raise ValueError('Make is required')
        if not model or not model.strip():
            raise ValueError('Model is required')
        if not color or not color.strip():
            raise ValueError('Color is required')
        
        CarRepository._validate_year(year)
        CarRepository._validate_price(price)
    
    @staticmethod
    def _validate_year(year):
        """
        Validate car year
        
        Raises:
            ValueError: If year is invalid
        """
        if not isinstance(year, int):
            raise ValueError('Year must be an integer')
        if year < 1900 or year > 2030:
            raise ValueError('Year must be between 1900 and 2030')
    
    @staticmethod
    def _validate_price(price):
        """
        Validate car price
        
        Raises:
            ValueError: If price is invalid
        """
        if not isinstance(price, (int, float)):
            raise ValueError('Price must be a number')
        if price < 0:
            raise ValueError('Price cannot be negative')
        if price > 10000000:  # 10 million cap
            raise ValueError('Price is unreasonably high')
