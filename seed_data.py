from app import create_app, db
from models import User, Provider, Service, Serviceman, Booking, Review, PortfolioItem, ChatMessage, SplitPayment, TrainingModule
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Check if data already exists
    if User.query.first():
        print("Data already exists. Skipping seed.")
    else:
        print("Seeding data...")

        # Users
        user1 = User(username='john_doe', email='john@example.com', password=generate_password_hash('password'), location_lat=40.7128, location_lng=-74.0060, loyalty_points=600)
        user2 = User(username='jane_smith', email='jane@example.com', password=generate_password_hash('password'), location_lat=40.7300, location_lng=-74.0100, is_business=True, business_name="Smith Corp")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Providers
        provider1 = Provider(name='Bybytoo Pro', email='pro@bybytoo.com', password=generate_password_hash('password'), location_lat=40.7150, location_lng=-74.0080, rating=4.8, is_verified=True, is_emergency_available=True, phone="555-0101")
        provider2 = Provider(name='Quick Fix', email='quick@bybytoo.com', password=generate_password_hash('password'), location_lat=40.7500, location_lng=-73.9900, rating=4.2, is_verified=False, is_emergency_available=False, phone="555-0102")
        db.session.add_all([provider1, provider2])
        db.session.commit()

        # Services
        service1 = Service(name='Deep Cleaning', price=100.0, category='Cleaning', provider_id=provider1.id)
        service2 = Service(name='Emergency Plumbing', price=150.0, category='Plumber', provider_id=provider1.id)
        service3 = Service(name='Basic Electrical', price=80.0, category='Electrician', provider_id=provider2.id)
        db.session.add_all([service1, service2, service3])
        db.session.commit()

        # Servicemen
        man1 = Serviceman(name='Mike', email='mike@bybytoo.com', password=generate_password_hash('password'), provider_id=provider1.id, current_lat=40.7160, current_lng=-74.0070)
        man2 = Serviceman(name='Bob', email='bob@bybytoo.com', password=generate_password_hash('password'), provider_id=provider2.id, current_lat=40.7510, current_lng=-73.9910)
        db.session.add_all([man1, man2])
        db.session.commit()

        # Bookings
        booking1 = Booking(user_id=user1.id, service_id=service1.id, serviceman_id=man1.id, booking_date=datetime.utcnow(), status='accepted', tracking_status='en_route')
        booking2 = Booking(user_id=user2.id, service_id=service3.id, booking_date=datetime.utcnow() - timedelta(days=1), status='completed')
        db.session.add_all([booking1, booking2])
        db.session.commit()

        # Portfolio
        portfolio1 = PortfolioItem(provider_id=provider1.id, image_url='https://via.placeholder.com/300', description='Cleaned a messy apartment', is_before_after=True)
        db.session.add(portfolio1)

        # Chat
        chat1 = ChatMessage(booking_id=booking1.id, sender_id=user1.id, sender_type='user', message='When will you arrive?')
        chat2 = ChatMessage(booking_id=booking1.id, sender_id=provider1.id, sender_type='provider', message='In 10 minutes.', price_proposal=None)
        db.session.add_all([chat1, chat2])

        # Split Payment
        split1 = SplitPayment(booking_id=booking1.id, user_id=user2.id, amount=50.0)
        db.session.add(split1)

        # Training
        tm1 = TrainingModule(title="Customer Service Mastery", description="Be polite and professional.", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", category="Soft Skills")
        db.session.add(tm1)

        db.session.commit()
        print("Data seeded successfully!")
