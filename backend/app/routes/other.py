from flask import Blueprint, render_template

other_bp = Blueprint('privacy_policy', __name__)


@other_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@other_bp.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')