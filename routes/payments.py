from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Booking, SplitPayment, User, db
from flask_login import current_user, login_required

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/booking/<int:booking_id>/split', methods=['GET', 'POST'])
@login_required
def split_payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if request.method == 'POST':
        email = request.form.get('email')
        amount = float(request.form.get('amount'))
        
        other_user = User.query.filter_by(email=email).first()
        if not other_user:
            flash('User not found.', 'error')
            return redirect(url_for('payments.split_payment', booking_id=booking_id))
            
        split = SplitPayment(
            booking_id=booking_id,
            user_id=other_user.id,
            amount=amount
        )
        db.session.add(split)
        db.session.commit()
        
        flash(f'Split payment request sent to {email}', 'success')
        return redirect(url_for('payments.split_payment', booking_id=booking_id))
        
    return render_template('split_payment.html', booking=booking)
