from flask import Blueprint, render_template, jsonify, request
from models import Booking, Serviceman, db

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track/<int:booking_id>')
def track_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('tracking.html', booking=booking)

@tracking_bp.route('/api/update_location', methods=['POST'])
def update_location():
    data = request.json
    serviceman_id = data.get('serviceman_id')
    lat = data.get('lat')
    lng = data.get('lng')
    
    serviceman = Serviceman.query.get(serviceman_id)
    if serviceman:
        serviceman.current_lat = lat
        serviceman.current_lng = lng
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Serviceman not found'}), 404

@tracking_bp.route('/api/get_location/<int:booking_id>')
def get_location(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.serviceman:
        return jsonify({
            'lat': booking.serviceman.current_lat,
            'lng': booking.serviceman.current_lng,
            'status': booking.tracking_status
        })
    return jsonify({'status': 'error', 'message': 'No serviceman assigned'}), 404
