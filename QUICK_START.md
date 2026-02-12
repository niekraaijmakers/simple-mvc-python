# 🚀 Quick Start Guide

## For macOS/Linux Users

### Option 1: Using the start script (Easiest)
```bash
./start.sh
```

### Option 2: Manual setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## For Windows Users

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## After Starting

1. Open your browser
2. Navigate to: `http://127.0.0.1:5001`
3. You'll see the car management interface with sample data
4. Try adding, editing, and deleting cars!

## Understanding the Code Flow

### Adding a New Car (Example)

**Step 1: User clicks "Add New Car"**
- Browser navigates to `/car/new`
- **Controller** (`controller/car_controller.py`): `new_car()` handles route
- **View** (`view/new_car.html`): Form is rendered

**Step 2: User fills form and clicks "Add Car"**
- Browser POSTs form data to `/car/create`
- **Controller**: `create_car()` handles route
- **Model/Repository** (`model/repository/car_repository.py`): Validates and saves
- **Model** (`model/car.py`): Creates Car object
- **Database**: New record inserted
- **Controller**: Redirects to home page with success message

**Step 3: User sees updated list**
- Browser navigates to `/`
- **Controller**: `index()` calls the repository service, forwards the data to the view 
- **Model/Repository**: Queries database, builds array of car models
- **View** (`view/index.html`): Displays the list with new car

## File Reference

| File | Purpose |
|------|---------|
| `app.py` | Main application - ties everything together |
| `model/car.py` | Car data model (pure data structure) |
| `model/repository/car_repository.py` | Database operations & business logic |
| `controller/car_controller.py` | HTTP routes and request handling |
| `view/*.html` | HTML templates for user interface |
| `view/static/css/*.css` | Stylesheets |
| `model/repository/instance/cars.db` | SQLite database (auto-created) |

## Common Tasks

### View all routes
```bash
# With Flask running, you can see all routes in the startup message
# Or add this to app.py:
# print(app.url_map)
```

### Reset database
```bash
# Stop the application (Ctrl+C)
# Delete the database file
rm model/repository/instance/cars.db
# Restart the application
python app.py
```

### Add more sample data
Edit the `create_app()` function in `app.py` and add more cars to the `sample_cars` list.

## Next Steps

1. ✅ Run the application
2. ✅ Explore all CRUD operations (Create, Read, Update, Delete)
3. ✅ Read through the code in this order:
   - `app.py` - Understand the setup
   - `model/car.py` - See the data structure
   - `model/repository/car_repository.py` - See database operations
   - `controller/car_controller.py` - See HTTP routes
   - `view/index.html` - See how data is displayed
4. ✅ Read the guides:
   - `README.md` - Full overview
   - `DATABASE_GUIDE.md` - Database operations explained
   - `FINAL_STRUCTURE.md` - Architecture deep dive
5. ✅ Try modifying the code:
   - Add a new field (e.g., "mileage")
   - Change the styling in `view/static/css/`
   - Add a search feature

## Troubleshooting

**"Module not found" error?**
→ Make sure virtual environment is activated and dependencies are installed

**HTTP 403 Error?**
→ This usually means port 5000 is being used by macOS ControlCenter
→ The app now uses port 5001 to avoid this issue
→ Make sure to navigate to http://127.0.0.1:5001 (not 5000)

**"Port already in use"?**
→ Change port in `app.py` line: `app.run(port=5002)`

**"Database is locked"?**
→ Stop the application and restart it

## Questions to Consider

As you explore the code, think about:
- Where is data validation happening? (Hint: Repository)
- How does Flask know which template to render? (Hint: `render_template`)
- What happens if you visit a non-existent car ID? (Hint: 404 error)
- Why do we use `db.session.commit()`? (Hint: saves changes)
- What's the difference between `.all()` and `.first()`?

## Learning Resources

- **README.md** - Main documentation with examples
- **DATABASE_GUIDE.md** - Understanding database queries
- **FINAL_STRUCTURE.md** - Architecture patterns explained
- **STRUCTURE_OVERVIEW.txt** - Quick visual structure

---

**Happy Learning! 🚀** Start with `README.md` for a complete overview!
