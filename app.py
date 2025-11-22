from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
from config import Config
from models import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        # Import here to avoid circular imports
        from models import User
        return User.query.get(int(user_id))

    # Import blueprints here to avoid circular imports
    from routes.user import user_bp
    from routes.provider import provider_bp
    from routes.servicemen import servicemen_bp
    from routes.api import api_bp

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(provider_bp, url_prefix='/provider')
    app.register_blueprint(servicemen_bp, url_prefix='/servicemen')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from routes.matching import matching_bp
    app.register_blueprint(matching_bp, url_prefix='/matching')

    from routes.tracking import tracking_bp
    app.register_blueprint(tracking_bp, url_prefix='/tracking')

    from routes.portfolio import portfolio_bp
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')

    from routes.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    from routes.emergency import emergency_bp
    app.register_blueprint(emergency_bp, url_prefix='/emergency')

    from routes.verification import verification_bp
    app.register_blueprint(verification_bp, url_prefix='/verification')

    from routes.loyalty import loyalty_bp
    app.register_blueprint(loyalty_bp, url_prefix='/loyalty')

    from routes.payments import payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')

    from routes.business import business_bp
    app.register_blueprint(business_bp, url_prefix='/business')

    from routes.training import training_bp
    app.register_blueprint(training_bp, url_prefix='/training')










    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory('static/bybytoo', filename)

    return app

# Create the app instance for gunicorn
app = create_app()

# Only create tables in development, not in production
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
