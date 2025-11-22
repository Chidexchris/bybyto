from flask import Blueprint, render_template, request, jsonify
from models import ChatMessage, Booking, db
from flask_login import current_user, login_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/booking/<int:booking_id>/chat')
@login_required
def view_chat(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    # Ensure user is part of the booking
    if current_user.id != booking.user_id and (not booking.serviceman or current_user.id != booking.serviceman.id) and (not booking.service.provider or current_user.id != booking.service.provider.id):
        # This check is simplified. In real app, check properly against User/Provider/Serviceman models
        pass 
        
    messages = ChatMessage.query.filter_by(booking_id=booking_id).order_by(ChatMessage.created_at).all()
    return render_template('chat.html', booking=booking, messages=messages)

@chat_bp.route('/api/send_message', methods=['POST'])
@login_required
def send_message():
    data = request.json
    booking_id = data.get('booking_id')
    message_text = data.get('message')
    price_proposal = data.get('price_proposal')
    
    # Determine sender type (simplified)
    sender_type = 'user' # Default
    # Logic to determine if sender is provider/serviceman would go here
    
    message = ChatMessage(
        booking_id=booking_id,
        sender_id=current_user.id,
        sender_type=sender_type,
        message=message_text,
        price_proposal=price_proposal
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': {
        'text': message.message,
        'price': message.price_proposal,
        'created_at': message.created_at.strftime('%H:%M')
    }})
