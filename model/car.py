"""
Car Model - Pure data structure representing a car entity
This is the MODEL in MVC pattern (using Repository architecture)

ARCHITECTURE NOTE:
- Model: Pure data structure (this file) - just fields and basic utilities
- Repository: Business logic and database operations (car_repository.py)

IMPORTANT FOR INTERNS:
The db.Column definitions below are for SQLAlchemy ORM (Object-Relational Mapping).
They tell SQLAlchemy how to map between database columns and Python objects.

When you CREATE a Car instance, these become regular Python primitives:
    car = Car(make='Toyota', model='Camry', year=2024, color='Blue', price=30000)
    car.make   → str
    car.year   → int
    car.price  → float
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    """
    Car entity - represents a car in the database
    
    This is a "thin" model that only defines the data structure.
    Business logic and database operations are handled by CarRepository.
    
    Instance Attributes (actual Python types when you use them):
        id (int): Unique identifier (auto-generated)
        make (str): Car manufacturer (e.g., 'Toyota')
        model (str): Car model (e.g., 'Camry')
        year (int): Manufacturing year (e.g., 2024)
        color (str): Car color (e.g., 'Blue')
        price (float): Car price (e.g., 30000.00)
    """
    __tablename__ = 'cars'
    
    # ORM Field Definitions (for database mapping)
    # These define the database schema, but instances will have primitive values
    id = db.Column(db.Integer, primary_key=True)        # → int (auto-increment)
    make = db.Column(db.String(50), nullable=False)     # → str (max 50 chars)
    model = db.Column(db.String(50), nullable=False)    # → str (max 50 chars)
    year = db.Column(db.Integer, nullable=False)        # → int
    color = db.Column(db.String(30), nullable=False)    # → str (max 30 chars)
    price = db.Column(db.Float, nullable=False)         # → float
    
    def __init__(self, make: str, model: str, year: int, color: str, price: float):
        """
        Initialize a car instance with the given attributes
        
        Args:
            make (str): Car manufacturer
            model (str): Car model
            year (int): Manufacturing year
            color (str): Car color
            price (float): Car price
            
        After initialization, all fields are PRIMITIVE Python types:
            self.make is a str
            self.year is an int
            self.price is a float
        """
        # Assign primitive values to instance
        self.make = make      # str
        self.model = model    # str
        self.year = year      # int
        self.color = color    # str
        self.price = price    # float
    
    def __repr__(self):
        """String representation of the car"""
        return f'<Car {self.year} {self.make} {self.model}>'
    
    def to_dict(self):
        """Convert car object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'price': self.price
        }
    
    # Computed properties (no database operations)
    
    @property
    def full_name(self):
        """Return the full name of the car"""
        return f'{self.year} {self.make} {self.model}'
    
    @property
    def price_with_tax(self, tax_rate=0.08):
        """Calculate price with tax (example of business logic in model)"""
        return self.price * (1 + tax_rate)


# ============================================================================
# FOR INTERNS: Understanding Fields
# ============================================================================
#
# COMMON CONFUSION: "Are the fields db.Column objects or primitives?"
#
# ANSWER: It depends on when you look at them!
#
# 1. AT CLASS LEVEL (Car.make) - It's a db.Column descriptor
#    Used by SQLAlchemy to create the database schema
#
# 2. AT INSTANCE LEVEL (car.make) - It's a primitive Python value!
#    Used by your code in templates, logic, etc.
#
# EXAMPLE:
#
#   # Create a car instance
#   car = Car(make='Toyota', model='Camry', year=2024, color='Blue', price=30000.00)
#
#   # Now these are all PRIMITIVE types:
#   print(type(car.make))   # <class 'str'>
#   print(type(car.year))   # <class 'int'>
#   print(type(car.price))  # <class 'float'>
#
#   # You can use them like any Python primitive:
#   if car.year > 2020:              # int comparison - works!
#       print(car.make.upper())      # str method - works!
#       total = car.price * 1.08     # float math - works!
#
# IN TEMPLATES (Jinja2):
#
#   {{ car.make }}   →  'Toyota' (str)
#   {{ car.year }}   →  2024 (int)
#   {{ car.price }}  →  30000.0 (float)
#
# These are plain primitive values, not ORM objects!
# ============================================================================
