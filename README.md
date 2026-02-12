# 🚗 Simple Flask MVC Car Management

A beginner-friendly Flask application demonstrating **Model-View-Controller (MVC)** architecture with the **Repository Pattern**.

## 📚 What You'll Learn

- **MVC Architecture** - Separation of concerns
- **Repository Pattern** - Data access layer
- **Flask Basics** - Routes, templates, blueprints
- **SQLAlchemy ORM** - Explicit database operations (no "magic")
- **CRUD Operations** - Create, Read, Update, Delete

## 🏗️ Project Structure

```
simple-mvc/
├── app.py                      # Application entry point
├── requirements.txt            # Dependencies
│
├── model/                      # DATA LAYER
│   ├── car.py                 # Car entity (pure data)
│   └── repository/
│       ├── car_repository.py  # Database operations
│       └── instance/
│           └── cars.db        # SQLite database
│
├── controller/                 # HTTP LAYER
│   └── car_controller.py      # Routes & request handling
│
└── view/                       # PRESENTATION LAYER
    ├── *.html                 # Templates
    └── static/css/            # Stylesheets
```

## 🚀 Quick Start

See [QUICK_START.md](QUICK_START.md) for installation and running instructions.

**TL;DR:**
```bash
./start.sh
```
Then visit: http://127.0.0.1:5001

## 🎯 Architecture

```
Browser → Controller → Repository → Model → Database
            ↓
          View
```

### Model (`model/car.py`)
Pure data structure - defines what a Car is:
```python
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    color = db.Column(db.String(30))
    price = db.Column(db.Float)
```

### Repository (`model/repository/car_repository.py`)
All database operations - **no hidden "magic"**:
```python
# Explicit database queries
def find_all():
    # SELECT * FROM cars
    return db.session.query(Car).all()

def find_by_id(car_id):
    # SELECT * FROM cars WHERE id = ?
    car = db.session.get(Car, car_id)
    if car is None:
        abort(404)
    return car

def create(make, model, year, color, price):
    # INSERT INTO cars (...)
    new_car = Car(make=make, model=model, year=year, color=color, price=price)
    db.session.add(new_car)
    db.session.commit()
    return new_car
```

### Controller (`controller/car_controller.py`)
HTTP handling - calls repository methods:
```python
@car_bp.route('/')
def index():
    cars = CarRepository.find_all()
    return render_template('index.html', cars=cars)

@car_bp.route('/car/<int:car_id>')
def show(car_id):
    car = CarRepository.find_by_id(car_id)
    return render_template('show_car.html', car=car)
```

### View (`view/*.html`)
HTML templates with CSS styling:
```html
{% for car in cars %}
  <div class="car-card">
    <h3>{{ car.year }} {{ car.make }} {{ car.model }}</h3>
    <p>Price: ${{ car.price }}</p>
  </div>
{% endfor %}
```

## 💡 Key Learning Points

### 1. Explicit Database Operations
**We don't use the "magic" `Car.query` shortcut.** Instead, we use explicit `db.session` calls so you can see exactly what's happening:

```python
# ❌ Magic (confusing for beginners)
cars = Car.query.all()

# ✅ Explicit (clear what's happening)
cars = db.session.query(Car).all()
```

Every database operation shows:
- What it does
- SQL equivalent in comments
- Step-by-step explanation

### 2. Repository Pattern
Business logic lives in the repository, not in controllers or models:

```python
# Controller just coordinates
def create_car():
    data = request.form
    car = CarRepository.create(
        make=data['make'],
        model=data['model'],
        year=int(data['year']),
        color=data['color'],
        price=float(data['price'])
    )
    return redirect(url_for('car.show', car_id=car.id))
```

The repository handles validation, database operations, and business rules.

### 3. MVC Separation
Each layer has a clear responsibility:

| Layer | Responsibility | Examples |
|-------|---------------|----------|
| **Model** | Data structure | Car fields, computed properties |
| **Repository** | Database & logic | CRUD, validation, queries |
| **Controller** | HTTP handling | Routes, redirects, errors |
| **View** | Presentation | HTML, CSS, display data |

## 📖 Understanding the Code

### How Database Queries Work

```python
# CREATE - Add a new car
new_car = Car(make='Toyota', model='Camry', year=2024, color='Blue', price=30000)
db.session.add(new_car)      # Stage for insert
db.session.commit()          # Execute INSERT

# READ - Get all cars
cars = db.session.query(Car).all()  # SELECT * FROM cars

# READ - Get one car
car = db.session.get(Car, 1)        # SELECT * FROM cars WHERE id = 1

# UPDATE - Modify a car
car = db.session.get(Car, 1)
car.price = 32000                   # SQLAlchemy tracks this change
db.session.commit()                 # UPDATE cars SET price = 32000 WHERE id = 1

# DELETE - Remove a car
car = db.session.get(Car, 1)
db.session.delete(car)              # Mark for deletion
db.session.commit()                 # DELETE FROM cars WHERE id = 1

# FILTER - Query with conditions
expensive = db.session.query(Car).filter(Car.price >= 40000).all()
# SELECT * FROM cars WHERE price >= 40000
```

### What is `db.session`?

Think of `db.session` as your **shopping cart** for database operations:
1. Add items: `db.session.add(car)`
2. Remove items: `db.session.delete(car)`
3. Checkout (save): `db.session.commit()`
4. Cancel: `db.session.rollback()`

### Common Patterns

**Pattern 1: Get or 404**
```python
car = db.session.get(Car, car_id)
if car is None:
    abort(404)  # Show "Not Found" error
```

**Pattern 2: Create with Validation**
```python
# Validate first
if not make or not model:
    raise ValueError("Make and model required")

# Then save
new_car = Car(make=make, model=model, ...)
db.session.add(new_car)
db.session.commit()
```

**Pattern 3: Update Tracked Objects**
```python
car = db.session.get(Car, car_id)
car.price = 30000  # SQLAlchemy sees this change
db.session.commit()  # Only updates changed fields
```

## 🎓 Learning Path

### Day 1: Understand the Structure
1. Read [QUICK_START.md](QUICK_START.md) and run the app
2. Explore the UI - add, edit, delete cars
3. Look at the folder structure

### Day 2: Read the Code
Start from the request flow:
1. `controller/car_controller.py` - See the routes
2. `model/repository/car_repository.py` - See database operations
3. `model/car.py` - See the data model
4. `view/index.html` - See the templates

### Day 3: Understand Database Operations
1. Read comments in `car_repository.py`
2. See SQL equivalents for each operation
3. Understand `db.session` workflow

### Day 4: Make Changes
Try these exercises:
1. Add a new field (e.g., `mileage`)
2. Add a search feature (filter by make)
3. Add sorting (by price, year, etc.)
4. Style changes in `view/static/css/`

### Day 5: Advanced Features
1. Add pagination
2. Add input validation
3. Add error handling
4. Create an API endpoint

## 🔍 Common Questions

**Q: Why explicit `db.session` instead of `Car.query`?**
A: To show exactly what's happening. `Car.query` is "magic" that hides the database connection. `db.session.query(Car)` is explicit and clear.

**Q: Why is the database in `model/repository/instance/`?**
A: Logical grouping - the repository manages data, so the database file lives with it.

**Q: Why singular folder names (model, controller, view)?**
A: Python package convention. Folders represent layers/namespaces, not collections.

**Q: Where should validation go?**
A: In the repository layer. It's business logic that happens before database operations.

**Q: Can I use `Car.query.all()` instead?**
A: Yes, it works, but we avoid it for teaching. The explicit way shows what's actually happening.

## 📁 File Guide

| File | Purpose |
|------|---------|
| `app.py` | Flask app setup and configuration |
| `model/car.py` | Car entity definition |
| `model/repository/car_repository.py` | All database operations |
| `controller/car_controller.py` | HTTP routes and handlers |
| `view/base.html` | Base template (navigation, layout) |
| `view/index.html` | List all cars |
| `view/show_car.html` | Show car details |
| `view/new_car.html` | Create new car form |
| `view/edit_car.html` | Edit car form |
| `view/static/css/main.css` | Base styles |

## 🛠️ Tech Stack

- **Flask** 3.0.0 - Web framework
- **Flask-SQLAlchemy** 3.1.1 - Database ORM
- **SQLite** - Database (file-based, no server needed)
- **Jinja2** - Template engine (included with Flask)
- **HTML/CSS** - Frontend

## 📚 Additional Documentation

- [QUICK_START.md](QUICK_START.md) - Installation and running
- [FINAL_STRUCTURE.md](FINAL_STRUCTURE.md) - Detailed architecture explanation

## 💬 For Instructors

This project is designed with explicit code over "clever" shortcuts:
- All database operations use `db.session` (no hidden `Model.query`)
- SQL comments explain what each operation does
- Clear separation of concerns
- Validation and business logic in repository
- Inline comments explain the "why"

## 🎯 Summary

This is a **teaching project** that prioritizes:
- ✅ **Clarity** over brevity
- ✅ **Explicit** over magic
- ✅ **Understanding** over efficiency
- ✅ **Learning** over production-readiness

The goal is to help interns understand **how web applications work** and build a strong foundation for future learning.

---

**Happy Learning! 🚀**
