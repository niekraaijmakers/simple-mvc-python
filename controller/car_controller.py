"""
Car Controller - Handles HTTP requests and coordinates between Repository and Views
This is the CONTROLLER in MVC + Repository Pattern

ARCHITECTURE:
Controller -> Repository -> Model -> Database

RESPONSIBILITY:
- Handle HTTP requests (routing)
- Extract data from requests (forms, query params)
- Call repository methods
- Handle responses (render templates, redirects, flash messages)
- NO direct database operations
- NO business logic (that's in the repository layer)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.repository.car_repository import CarRepository

# Create a Blueprint for car routes
car_bp = Blueprint('car', __name__)


@car_bp.route('/')
def index():
    """Display all cars - READ operation"""
    cars = CarRepository.find_all()  # Using repository
    return render_template('index.html', cars=cars)


@car_bp.route('/car/new', methods=['GET'])
def new_car():
    """Show form to create a new car"""
    return render_template('new_car.html')


@car_bp.route('/car/create', methods=['POST'])
def create_car():
    """Create a new car - CREATE operation"""
    try:
        # Extract data from form (Controller's responsibility)
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        color = request.form['color']
        price = float(request.form['price'])
        
        # Call repository (Repository handles validation and persistence)
        new_car = CarRepository.create(make=make, model=model, year=year, 
                                       color=color, price=price)
        
        flash(f'Successfully added {new_car.full_name}!', 'success')
        return redirect(url_for('car.index'))
    except ValueError as e:
        # Validation errors from repository
        flash(f'Validation error: {str(e)}', 'error')
        return redirect(url_for('car.new_car'))
    except Exception as e:
        # Other errors
        flash(f'Error adding car: {str(e)}', 'error')
        return redirect(url_for('car.new_car'))


@car_bp.route('/car/<int:id>')
def show_car(id):
    """Show details of a specific car - READ operation"""
    car = CarRepository.find_by_id(id)  # Using repository
    return render_template('show_car.html', car=car)


@car_bp.route('/car/<int:id>/edit')
def edit_car(id):
    """Show form to edit a car"""
    car = CarRepository.find_by_id(id)  # Using repository
    return render_template('edit_car.html', car=car)


@car_bp.route('/car/<int:id>/update', methods=['POST'])
def update_car(id):
    """Update a car - UPDATE operation"""
    try:
        # Extract form data (Controller's responsibility)
        make = request.form['make']
        model = request.form['model']
        year = int(request.form['year'])
        color = request.form['color']
        price = float(request.form['price'])
        
        # Call repository (Repository handles validation and update)
        car = CarRepository.update(id, make=make, model=model, year=year, 
                                    color=color, price=price)
        
        flash(f'Successfully updated {car.full_name}!', 'success')
        return redirect(url_for('car.show_car', id=id))
    except ValueError as e:
        # Validation errors from repository
        flash(f'Validation error: {str(e)}', 'error')
        return redirect(url_for('car.edit_car', id=id))
    except Exception as e:
        flash(f'Error updating car: {str(e)}', 'error')
        return redirect(url_for('car.edit_car', id=id))


@car_bp.route('/car/<int:id>/delete', methods=['POST'])
def delete_car(id):
    """Delete a car - DELETE operation"""
    try:
        # Call repository (Repository handles deletion)
        car_info = CarRepository.delete(id)
        
        flash(f'Successfully deleted {car_info["full_name"]}!', 'success')
        return redirect(url_for('car.index'))
    except Exception as e:
        flash(f'Error deleting car: {str(e)}', 'error')
        return redirect(url_for('car.index'))
