from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app import db
from app.models import Violation
from app.forms import ViolationForm
from app.utils.qr_generator import generate_qr_code

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_login():
    pass

@admin_bp.route('/dashboard')
def dashboard():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Violation.query
    if search:
        query = query.filter(Violation.vehicle_number.ilike(f'%{search}%'))
        
    violations = query.order_by(Violation.date.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/dashboard.html', title='Admin Dashboard', violations=violations, search=search)

@admin_bp.route('/add', methods=['GET', 'POST'])
def add_violation():
    form = ViolationForm()
    if form.validate_on_submit():
        violation = Violation(
            vehicle_number=form.vehicle_number.data,
            violation_type=form.violation_type.data,
            location=form.location.data,
            fine_amount=form.fine_amount.data,
            status=form.status.data
        )
        db.session.add(violation)
        db.session.commit() # Commit to get the ID
        
        # Generate QR code
        qr_path = generate_qr_code(violation.id)
        violation.qr_code_path = qr_path
        db.session.commit()
        
        flash('Violation has been successfully added.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/violation_form.html', title='Add Violation', form=form, legend='New Violation')

@admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_violation(id):
    violation = Violation.query.get_or_404(id)
    form = ViolationForm()
    if form.validate_on_submit():
        violation.vehicle_number = form.vehicle_number.data
        violation.violation_type = form.violation_type.data
        violation.location = form.location.data
        violation.fine_amount = form.fine_amount.data
        violation.status = form.status.data
        db.session.commit()
        flash('Violation has been updated.', 'success')
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        form.vehicle_number.data = violation.vehicle_number
        form.violation_type.data = violation.violation_type
        form.location.data = violation.location
        form.fine_amount.data = violation.fine_amount
        form.status.data = violation.status
    return render_template('admin/violation_form.html', title='Edit Violation', form=form, legend='Edit Violation')

@admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete_violation(id):
    violation = Violation.query.get_or_404(id)
    db.session.delete(violation)
    db.session.commit()
    flash('Violation has been deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
