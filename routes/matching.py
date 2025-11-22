from flask import Blueprint, render_template, request, jsonify
from models import User, Provider, Service, db
from sqlalchemy import func

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/match', methods=['GET', 'POST'])
def match_providers():
    if request.method == 'POST':
        # Get user requirements
        service_category = request.form.get('category')
        user_lat = float(request.form.get('lat', 0))
        user_lng = float(request.form.get('lng', 0))
        
        # Simple matching algorithm
        # 1. Filter by category
        # 2. Calculate distance (simplified)
        # 3. Sort by rating and distance
        
        query = Provider.query.join(Service).filter(Service.category == service_category)
        
        providers = query.all()
        
        scored_providers = []
        for provider in providers:
            # Calculate distance (Euclidean for simplicity, use Haversine in prod)
            if provider.location_lat and provider.location_lng:
                distance = ((provider.location_lat - user_lat)**2 + (provider.location_lng - user_lng)**2)**0.5
            else:
                distance = 9999 # Far away if no location
            
            # Score: Higher rating is better, lower distance is better
            # Score = (Rating * 20) - (Distance * 100) (Arbitrary weights)
            score = (provider.rating * 20) - (distance * 100)
            
            scored_providers.append({
                'provider': provider,
                'score': score,
                'distance': distance
            })
            
        # Sort by score descending
        scored_providers.sort(key=lambda x: x['score'], reverse=True)
        
        return render_template('matching_results.html', matches=scored_providers)
        
    return render_template('matching_form.html')
