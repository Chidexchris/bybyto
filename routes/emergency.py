from flask import Blueprint, render_template, request
from models import Provider, db

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/emergency', methods=['GET', 'POST'])
def find_emergency():
    if request.method == 'POST':
        user_lat = float(request.form.get('lat', 0))
        user_lng = float(request.form.get('lng', 0))
        service_type = request.form.get('service_type')
        
        # Find providers who are available for emergency and match service type (simplified)
        # In real app, filter by service type properly
        query = Provider.query.filter_by(is_emergency_available=True)
        
        providers = query.all()
        
        nearby_providers = []
        for provider in providers:
            if provider.location_lat and provider.location_lng:
                distance = ((provider.location_lat - user_lat)**2 + (provider.location_lng - user_lng)**2)**0.5
                # Filter by distance (e.g., within 0.1 degrees approx 10km)
                if distance < 0.1:
                    nearby_providers.append({
                        'provider': provider,
                        'distance': distance
                    })
        
        nearby_providers.sort(key=lambda x: x['distance'])
        
        return render_template('emergency_results.html', providers=nearby_providers)
        
    return render_template('emergency.html')
