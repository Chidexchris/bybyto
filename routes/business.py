from flask import Blueprint, render_template, redirect, url_for, flash
from models import Booking, User
from flask_login import current_user, login_required

business_bp = Blueprint('business', __name__)

@business_bp.route('/business/dashboard')
@login_required
def dashboard():
    # Ensure user is a business account
    if not current_user.is_business:
        flash('Access denied. Business accounts only.', 'error')
        return redirect(url_for('index'))
        
    # Get all bookings for this business user
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    
    # Calculate some stats
    total_spent = sum(b.service.price for b in bookings if b.service)
    active_tasks = sum(1 for b in bookings if b.status in ['pending', 'accepted', 'started'])
    
    return render_template('business_dashboard.html', bookings=bookings, total_spent=total_spent, active_tasks=active_tasks)
