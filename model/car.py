"""
Car Model - Pure data structure representing a car entity
This is the MODEL in MVC pattern (using Service Layer architecture)

ARCHITECTURE NOTE:
- Model: Pure data structure (this file) - just fields and basic utilities
- Service: Business logic and database operations (car_service.py)
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    """
    Car entity - represents a car in the database
    
    This is a "thin" model that only defines the data structure.
    Business logic and database operations are handled by CarService.
    """
    __tablename__ = 'cars'
    
    # Database fields
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __init__(self, make, model, year, color, price):
        """Initialize a car instance with the given attributes"""
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.price = price
    
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
