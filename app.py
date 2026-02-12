"""
Main Flask Application File
This initializes the Flask app and ties together Models, Views, and Controllers
"""
from flask import Flask
from model.car import db
from controller.car_controller import car_bp
import os


def create_app():
    """Application factory function"""
    app = Flask(__name__, 
                template_folder='view',
                static_folder='view/static',
                static_url_path='/static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    # Database stored in repository layer (where data access happens)
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'model', 'repository', 'instance', 'cars.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints (controllers)
    app.register_blueprint(car_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Add some sample data if database is empty
        from model.car import Car
        if Car.query.count() == 0:
            sample_cars = [
                Car(make='Toyota', model='Camry', year=2023, color='Blue', price=28500.00),
                Car(make='Honda', model='Civic', year=2022, color='Silver', price=24000.00),
                Car(make='Ford', model='Mustang', year=2024, color='Red', price=45000.00),
                Car(make='Tesla', model='Model 3', year=2023, color='White', price=42000.00),
            ]
            for car in sample_cars:
                db.session.add(car)
            db.session.commit()
            print("✓ Sample data added to database")
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*50)
    print("🚗 Car Management System Started!")
    print("="*50)
    print("📍 Navigate to: http://127.0.0.1:5001")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
