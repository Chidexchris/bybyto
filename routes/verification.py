from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Provider, db
from flask_login import current_user, login_required
import os

verification_bp = Blueprint('verification', __name__)

@verification_bp.route('/verification', methods=['GET', 'POST'])
@login_required
def verify_provider():
    # Ensure current user is a provider
    if not isinstance(current_user, Provider):
        flash('Verification is only for providers.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'id_document' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['id_document']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
            
        if file:
            # In real app, save securely and maybe use S3
            # For now, just simulate saving
            filename = f"verification_{current_user.id}_{file.filename}"
            # file.save(os.path.join('static/uploads', filename))
            
            current_user.verification_doc_url = filename
            # In real app, this would trigger a manual review process
            # For demo, we auto-verify
            current_user.is_verified = True
            db.session.commit()
            
            flash('Documents submitted! You are now verified.', 'success')
            return redirect(url_for('verification.verify_provider'))

    return render_template('verification.html', provider=current_user)
