# 📊 Database Operations Guide

Understanding how the application talks to the database using SQLAlchemy.

## 🎯 The Big Picture

```
Your Code → db.session → SQLAlchemy → SQL → SQLite Database
```

**What is `db.session`?**
- Your connection to the database
- Like a "shopping cart" for database operations
- Tracks changes automatically
- Saves everything when you call `.commit()`

## 📖 Basic Operations (CRUD)

### CREATE - Adding New Records

```python
# Step 1: Create a Python object (not in database yet)
new_car = Car(
    make='Toyota',
    model='Camry',
    year=2024,
    color='Blue',
    price=30000
)

# Step 2: Tell the session "I want to save this"
db.session.add(new_car)

# Step 3: Actually save to database
db.session.commit()

# Now new_car has an ID assigned by the database!
print(f"Created car with ID: {new_car.id}")
```

**SQL Generated:**
```sql
INSERT INTO cars (make, model, year, color, price)
VALUES ('Toyota', 'Camry', 2024, 'Blue', 30000);
```

**Why 3 steps?**
- **Step 1**: Create object in Python memory
- **Step 2**: Stage it (can batch multiple adds)
- **Step 3**: Execute the SQL INSERT

---

### READ - Getting Records

#### Get All Records
```python
# Get all cars from database
cars = db.session.query(Car).all()

# Returns: [<Car>, <Car>, <Car>, ...]
# Or empty list [] if no cars
```

**SQL Generated:**
```sql
SELECT * FROM cars;
```

#### Get One Record by ID
```python
# Get a specific car by its primary key
car = db.session.get(Car, 1)

# Returns: <Car> object or None if not found
if car is None:
    print("Car not found!")
else:
    print(f"Found: {car.make} {car.model}")
```

**SQL Generated:**
```sql
SELECT * FROM cars WHERE id = 1;
```

#### Filter Records
```python
# Find all Toyota cars
toyotas = db.session.query(Car).filter_by(make='Toyota').all()

# Find expensive cars (price >= 40000)
expensive = db.session.query(Car).filter(Car.price >= 40000).all()

# Find cars from 2020-2024
recent = db.session.query(Car).filter(
    Car.year >= 2020,
    Car.year <= 2024
).all()
```

**SQL Generated:**
```sql
-- filter_by example
SELECT * FROM cars WHERE make = 'Toyota';

-- filter with comparison
SELECT * FROM cars WHERE price >= 40000;

-- multiple conditions (AND)
SELECT * FROM cars WHERE year >= 2020 AND year <= 2024;
```

---

### UPDATE - Changing Records

```python
# Step 1: Get the car from database
car = db.session.get(Car, 1)

# Step 2: Modify it (SQLAlchemy tracks changes automatically!)
car.price = 32000
car.color = 'Red'

# Step 3: Save changes
db.session.commit()
```

**SQL Generated:**
```sql
-- SQLAlchemy only updates changed fields!
UPDATE cars 
SET price = 32000, color = 'Red'
WHERE id = 1;
```

**Magic Behind the Scenes:**
1. When you load `car`, SQLAlchemy remembers original values
2. When you change `car.price`, SQLAlchemy notices
3. On commit, SQLAlchemy generates UPDATE for only changed fields
4. More efficient than updating all fields every time!

---

### DELETE - Removing Records

```python
# Step 1: Get the car to delete
car = db.session.get(Car, 1)

# Step 2: Mark it for deletion
db.session.delete(car)

# Step 3: Execute the delete
db.session.commit()
```

**SQL Generated:**
```sql
DELETE FROM cars WHERE id = 1;
```

---

## 🔍 Query Methods

### `.all()` - Get All Results
```python
cars = db.session.query(Car).all()
# Returns: List of Car objects
```

### `.first()` - Get First Result
```python
car = db.session.query(Car).filter_by(make='Toyota').first()
# Returns: One Car object or None
```

### `.count()` - Count Records
```python
total = db.session.query(Car).count()
# Returns: Integer (number of cars)
```

**SQL Generated:**
```sql
SELECT COUNT(*) FROM cars;
```

### `.filter()` vs `.filter_by()`

**Use `.filter_by()` for simple equality:**
```python
# Simple: WHERE make = 'Toyota'
toyotas = db.session.query(Car).filter_by(make='Toyota').all()
```

**Use `.filter()` for comparisons:**
```python
# Comparison: WHERE price >= 40000
expensive = db.session.query(Car).filter(Car.price >= 40000).all()

# You can also use filter() for equality
toyotas = db.session.query(Car).filter(Car.make == 'Toyota').all()
```

---

## 🛒 Understanding `db.session`

Think of the session as a shopping cart:

```python
# 1. Add items to cart
car1 = Car(make='Toyota', model='Camry', ...)
car2 = Car(make='Honda', model='Civic', ...)
db.session.add(car1)
db.session.add(car2)

# 2. Modify items already in cart
existing_car = db.session.get(Car, 5)
existing_car.price = 30000

# 3. Remove items from cart
old_car = db.session.get(Car, 10)
db.session.delete(old_car)

# 4. Checkout (save everything at once)
db.session.commit()  # Executes all operations in one transaction
```

### Session Tracks Changes

```python
car = db.session.get(Car, 1)
print(car.price)  # 28000

car.price = 30000
# Session remembers: "car.price changed from 28000 to 30000"

car.color = 'Blue'
# Session remembers: "car.color changed from X to Blue"

db.session.commit()
# Session executes: UPDATE cars SET price = 30000, color = 'Blue' WHERE id = 1
```

### Rollback - Undo Changes

```python
car = db.session.get(Car, 1)
car.price = 99999  # Oops, mistake!

db.session.rollback()  # Undo all changes since last commit
print(car.price)  # Back to original value
```

---

## 📋 Common Patterns

### Pattern 1: Get or 404

```python
def find_by_id(car_id):
    car = db.session.get(Car, car_id)
    
    if car is None:
        # Return HTTP 404 error to user
        from flask import abort
        abort(404)
    
    return car
```

**Why?** If user requests `/car/999` but car 999 doesn't exist, show a proper "Not Found" page instead of crashing.

### Pattern 2: Create with Validation

```python
def create(make, model, year, color, price):
    # Validate BEFORE touching database
    if not make or not model:
        raise ValueError("Make and model are required")
    
    if year < 1900 or year > 2030:
        raise ValueError("Invalid year")
    
    if price < 0:
        raise ValueError("Price cannot be negative")
    
    # Only create if validation passes
    new_car = Car(make=make, model=model, year=year, color=color, price=price)
    db.session.add(new_car)
    db.session.commit()
    
    return new_car
```

**Why?** Catch bad data before it reaches the database.

### Pattern 3: Query Builder

```python
# Build query step by step
query = db.session.query(Car)

# Add conditions dynamically
if make:
    query = query.filter_by(make=make)

if min_price:
    query = query.filter(Car.price >= min_price)

if max_price:
    query = query.filter(Car.price <= max_price)

# Execute query
results = query.all()
```

**Why?** Flexible searching - only filter by fields that user provided.

---

## ❌ Common Mistakes

### Mistake 1: Forgetting to Commit

```python
# ❌ WRONG - Changes not saved
new_car = Car(make='Toyota', model='Camry', ...)
db.session.add(new_car)
# Missing: db.session.commit()
# Car is NOT in database!

# ✅ CORRECT
new_car = Car(make='Toyota', model='Camry', ...)
db.session.add(new_car)
db.session.commit()  # Now it's saved!
```

### Mistake 2: Not Checking for None

```python
# ❌ WRONG - Will crash if car not found
car = db.session.get(Car, 999)
car.price = 30000  # ERROR! car is None

# ✅ CORRECT
car = db.session.get(Car, 999)
if car is None:
    print("Car not found")
else:
    car.price = 30000
    db.session.commit()
```

### Mistake 3: Modifying Without Commit

```python
# ❌ WRONG - Change not saved
car = db.session.get(Car, 1)
car.price = 30000
# Missing: db.session.commit()
# Change is NOT saved to database!

# ✅ CORRECT
car = db.session.get(Car, 1)
car.price = 30000
db.session.commit()  # Now it's saved!
```

---

## 🎓 Practice Exercises

### Exercise 1: Create Your First Car
```python
# Create a car with your favorite make/model
# Don't forget to commit!
```

### Exercise 2: Update a Car's Price
```python
# Load car with ID 1
# Change its price to 35000
# Save the change
```

### Exercise 3: Find Expensive Cars
```python
# Query for all cars with price >= 50000
# Print how many you found
```

### Exercise 4: Delete Old Cars
```python
# Find cars older than 2010
# Delete them
# (Test with sample data first!)
```

### Exercise 5: Search by Make
```python
# Get user input for a car make
# Find all cars with that make
# Print each car's full name
```

---

## 🔗 Relationships (Future Learning)

This project uses a simple single table. In real applications, you'll have relationships:

```python
# One-to-Many: One manufacturer, many cars
class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cars = db.relationship('Car', backref='manufacturer')

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
```

You'll learn this next!

---

## 📚 Summary

**Key Concepts:**
- `db.session` = Your database connection
- `query()` = Start building a SELECT
- `add()` = Stage for INSERT
- `delete()` = Stage for DELETE
- `commit()` = Execute all staged operations
- `.all()` = Get all results
- `.first()` = Get first result
- `.get()` = Get by primary key
- `.filter()` = Add WHERE conditions

**Three-Step Pattern:**
1. **Get/Create** the object
2. **Modify** it (session tracks changes)
3. **Commit** to save

**Always Remember:**
- Check for `None` before using an object
- Validate data before saving
- Commit to save changes
- Use rollback to undo mistakes

---

**Questions?** Check `model/repository/car_repository.py` for real examples with comments!
