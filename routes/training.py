from flask import Blueprint, render_template
from models import TrainingModule
from flask_login import login_required

training_bp = Blueprint('training', __name__)

@training_bp.route('/training')
@login_required
def view_training():
    # In real app, ensure user is a provider
    
    # Seed some dummy data if empty
    if TrainingModule.query.count() == 0:
        from models import db
        modules = [
            TrainingModule(title="Customer Communication 101", description="Learn how to talk to customers effectively.", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", category="Soft Skills"),
            TrainingModule(title="Safety First", description="Essential safety protocols for on-site jobs.", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", category="Safety"),
            TrainingModule(title="Pricing Your Services", description="How to set competitive yet profitable prices.", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", category="Business"),
            TrainingModule(title="Taking Professional Photos", description="Showcase your work with better photography.", video_url="https://www.youtube.com/embed/dQw4w9WgXcQ", category="Marketing")
        ]
        db.session.add_all(modules)
        db.session.commit()
        
    modules = TrainingModule.query.all()
    return render_template('training.html', modules=modules)
