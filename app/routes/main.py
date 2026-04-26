from flask import Blueprint, render_template, request
from app.models import Violation

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html', title='Home')

@main_bp.route('/violation/<int:id>')
def public_status(id):
    violation = Violation.query.get_or_404(id)
    return render_template('main/public_status.html', title='Violation Status', violation=violation)
