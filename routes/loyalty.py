from flask import Blueprint, render_template
from models import User
from flask_login import current_user, login_required

loyalty_bp = Blueprint('loyalty', __name__)

@loyalty_bp.route('/loyalty')
@login_required
def view_loyalty():
    # Ensure current user is a User (not provider)
    # In real app, check type properly
    
    # Logic to calculate points history would go here
    # For now, just show current points
    
    rewards = [
        {'name': '$5 Off Coupon', 'cost': 500},
        {'name': 'Free Service Call', 'cost': 1000},
        {'name': '$20 Gift Card', 'cost': 2000}
    ]
    
    return render_template('loyalty.html', user=current_user, rewards=rewards)
