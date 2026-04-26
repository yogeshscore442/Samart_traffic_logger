from app import create_app, db
from app.models import User, Violation
from datetime import datetime

app = create_app()

with app.app_context():
    # Create database tables
    db.create_all()

    # Check if admin user exists
    if not User.query.filter_by(username='admin').first():
        print("Creating admin user...")
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created (username: admin, password: admin123)")
    else:
        print("Admin user already exists.")

    print("Database initialization complete.")
