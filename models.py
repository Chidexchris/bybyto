from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    # New fields for features
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    loyalty_points = db.Column(db.Integer, default=0)
    is_business = db.Column(db.Boolean, default=False)
    business_name = db.Column(db.String(150))

class Provider(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    services = db.relationship('Service', backref='provider', lazy=True)
    servicemen = db.relationship('Serviceman', backref='provider', lazy=True)
    # New fields for features
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    rating = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)
    verification_doc_url = db.Column(db.String(255))
    is_emergency_available = db.Column(db.Boolean, default=False)
    portfolio_items = db.relationship('PortfolioItem', backref='provider', lazy=True)

class Serviceman(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='serviceman', lazy=True)
    # New fields for features
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    bookings = db.relationship('Booking', backref='service', lazy=True)
    reviews = db.relationship('Review', backref='service', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    serviceman_id = db.Column(db.Integer, db.ForeignKey('serviceman.id'), nullable=True)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, accepted, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # New fields
    tracking_status = db.Column(db.String(50)) # e.g., 'en_route', 'arrived', 'started'
    split_payments = db.relationship('SplitPayment', backref='booking', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='booking', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# New Models

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_before_after = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=True)
    sender_id = db.Column(db.Integer, nullable=False) # User or Provider ID
    sender_type = db.Column(db.String(20), nullable=False) # 'user' or 'provider'
    message = db.Column(db.Text, nullable=False)
    price_proposal = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SplitPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # The user sharing the cost
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrainingModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
