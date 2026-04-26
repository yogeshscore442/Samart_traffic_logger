from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), index=True, nullable=False)
    violation_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    fine_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), index=True, default='Unpaid', nullable=False) # Paid or Unpaid
    qr_code_path = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Violation {self.vehicle_number} - {self.violation_type}>'
