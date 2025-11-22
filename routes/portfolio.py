from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import PortfolioItem, Provider, db
from flask_login import current_user, login_required

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/provider/<int:provider_id>/portfolio')
def view_portfolio(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    return render_template('portfolio.html', provider=provider)

@portfolio_bp.route('/my-portfolio', methods=['GET', 'POST'])
@login_required
def manage_portfolio():
    # Assuming current_user can be a provider. In real app, check type.
    if not isinstance(current_user, Provider):
        flash('Access denied. Providers only.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        image_url = request.form.get('image_url')
        description = request.form.get('description')
        is_before_after = request.form.get('is_before_after') == 'on'
        
        item = PortfolioItem(
            provider_id=current_user.id,
            image_url=image_url,
            description=description,
            is_before_after=is_before_after
        )
        db.session.add(item)
        db.session.commit()
        flash('Portfolio item added!', 'success')
        
    return render_template('manage_portfolio.html', provider=current_user)
