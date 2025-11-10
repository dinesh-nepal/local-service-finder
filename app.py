from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Provider, Service, ContactMessage,Rating
from config import Config
import os
import re
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import timedelta,datetime
from sqlalchemy import func
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=3)
# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
# Initialize database and sample data
def init_db():
    with app.app_context():
        db.create_all()
        try:
            admin_count=User.query.filter_by(user_type='admin').count()
        except:
            # Tables don't exist yet
            db.create_all()
            admin_count = 0
        all_admins = User.query.filter_by(user_type='admin').all()
        # Create default admin if not exists
        if len(all_admins) == 0:
            admin_email='admin@lsf.com'
        # admin = User.query.filter_by(email=admin_email).first()
        
            admin = User(
                username='admin',
                email=admin_email,
                full_name='System Administrator',
                phone='9862400161',
                user_type='admin',
                created_at=datetime.utcnow()
            )
        
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created! Username: admin, Password: admin123")
        elif len(all_admins)>1:
            # Multiple admins exist, check if default admin is one of them
            default_admin = User.query.filter_by(username='admin', email='admin@lsf.com').first()
            
            if default_admin:
                # Check if there are other admins besides the default
                other_admins = [admin for admin in all_admins if admin.id != default_admin.id]
                
                if len(other_admins) > 0:
                    # Other admins exist, delete the default
                    db.session.delete(default_admin)
                    db.session.commit()
                    print("✓ Default admin removed. Custom admin(s) detected.")
                
                else:
                # Exactly one admin exists
                    admin = all_admins[0]
                    if admin.username == 'admin' and admin.email == 'admin@lsf.com':
                        print("✓ Default admin exists.")
                    else:
                        print("✓ Custom admin exists.")       
                        print("✓ Only default admin exists.")
        # else:
        #     print(f"Admin user ({admin_email}) already exists.Skipping creation.")
        # Add sample services if not exists
        if Service.query.count() == 0:
            services_data = [
                {'name': 'Plumbing', 'description': 'Professional plumbing services', 'icon': 'fa-wrench'},
                {'name': 'Electrician', 'description': 'Licensed electrical services', 'icon': 'fa-bolt'},
                {'name': 'Mechanic', 'description': 'Auto repair and maintenance', 'icon': 'fa-car'},
                {'name': 'Cleaning', 'description': 'Home and office cleaning', 'icon': 'fa-broom'},
                {'name': 'Tutoring', 'description': 'Educational tutoring services', 'icon': 'fa-book'},
                {'name': 'Gardening', 'description': 'Garden maintenance and landscaping', 'icon': 'fa-leaf'},
                {'name': 'Painting', 'description': 'Interior and exterior painting', 'icon': 'fa-paint-roller'},
                {'name': 'Carpentry', 'description': 'Custom woodwork and repairs', 'icon': 'fa-hammer'},
                {'name': 'Pest Control', 'description': 'Pest elimination services', 'icon': 'fa-bug'},
                {'name': 'Moving', 'description': 'Relocation and moving services', 'icon': 'fa-truck'},
                {'name': 'Security', 'description': 'Security system installation', 'icon': 'fa-shield-alt'},
                {'name': 'Catering', 'description': 'Event catering services', 'icon': 'fa-utensils'}
            ]
            
            for service_data in services_data:
                service = Service(**service_data)
                db.session.add(service)
            
            db.session.commit()
            print("Sample services added!")


# Custom Jinja filter for counting providers
@app.template_filter('count_providers')
def count_providers(service_name):
    return Provider.query.filter_by(service_type=service_name).count()

def validate_password(password):
    """Validate password: min 6 chars, at least 1 uppercase and 1 number"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Valid"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    all_services = Service.query.all()
    return render_template('services.html', services=all_services)

@app.route('/provider-details/<service_name>')
@login_required
def provider_details(service_name):
    # Only show approved providers to regular users
    providers = Provider.query.filter_by(service_type=service_name, is_approved=True, status='approved').all()
    user_ratings = {r.provider_id: r.rating for r in Rating.query.filter_by(user_id=current_user.id).all()}
    return render_template('provider-details.html', service_name=service_name, providers=providers,user_ratings=user_ratings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Contact admin.', 'error')
                return redirect(url_for('login'))
            
            login_user(user, remember=True)
            session.permanent=True
            flash('Login successful!', 'success')
            
            # Redirect admin to admin dashboard
            if user.is_admin():
                return redirect(url_for('admin_dashboard'))
             # Redirect provider to provider dashboard
            if user.user_type == 'provider':
                return redirect(url_for('provider_dashboard'))
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        

        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, 'error')
            return redirect(url_for('signup'))
        
        # Validate phone number (10 digits only)
        if not phone.isdigit() or len(phone) != 10:
            flash('Phone number must be exactly 10 digits', 'error')
            return redirect(url_for('signup'))
        
        # Validate name (no numbers)
        if any(char.isdigit() for char in full_name):
            flash('Name cannot contain numbers', 'error')
            return redirect(url_for('signup'))
        

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
        
        user = User(username=username, email=email, full_name=full_name, phone=phone)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Check if user already has a provider profile
    existing_provider = Provider.query.filter_by(user_id=current_user.id).first()
    if existing_provider:
        flash('You already have a provider profile!', 'error')
        return redirect(url_for('provider_dashboard'))
    if request.method == 'POST':
        service_type = request.form.get('service_type')
        business_name = request.form.get('business_name')
        description = request.form.get('description')
        location = request.form.get('location')
        
        photo = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo = filename
        license_document = None
        if 'license' in request.files:
            file = request.files['license']
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    license_document = filename
                else:
                    flash('Invalid license file format. Please upload PDF, JPG, or PNG', 'error')
                    return redirect(url_for('register'))
        provider = Provider(
            user_id=current_user.id,
            service_type=service_type,
            business_name=business_name,
            description=description,
            location=location,
            photo=photo,
            license_document=license_document,
            is_approved=False,
            status='pending'
        )
        
        db.session.add(provider)
        current_user.user_type = 'provider'
        db.session.commit()
        
        flash('Provider registration successful! Waiting for admin approval', 'success')
        return redirect(url_for('provider_dashboard'))
    
    services = Service.query.all()
    return render_template('register.html', services=services)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        contact_msg = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(contact_msg)
        db.session.commit()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/api/check-login')
def check_login():
    return jsonify({'logged_in': current_user.is_authenticated})


@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.filter_by(user_type='customer').count()
    total_providers = Provider.query.count()
    pending_providers = Provider.query.filter_by(status='pending').count()
    total_services = Service.query.count()
    total_messages = ContactMessage.query.count()
    
    recent_providers = Provider.query.order_by(Provider.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_providers=total_providers,
                         pending_providers=pending_providers,
                         total_services=total_services,
                         total_messages=total_messages,
                         recent_providers=recent_providers,
                         recent_messages=recent_messages)

@app.route('/admin/providers')
@login_required
@admin_required
def admin_providers():
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        providers = Provider.query.order_by(Provider.created_at.desc()).all()
    else:
        providers = Provider.query.filter_by(status=status_filter).order_by(Provider.created_at.desc()).all()
    
    return render_template('admin/providers.html', providers=providers, status_filter=status_filter)

@app.route('/admin/provider/approve/<int:provider_id>')
@login_required
@admin_required
def approve_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    provider.is_approved = True
    provider.status = 'approved'
    db.session.commit()
    flash(f'Provider {provider.business_name} approved successfully!', 'success')
    return redirect(url_for('admin_providers'))

@app.route('/admin/provider/reject/<int:provider_id>')
@login_required
@admin_required
def reject_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    provider.is_approved = False
    provider.status = 'rejected'
    db.session.commit()
    flash(f'Provider {provider.business_name} rejected.', 'success')
    return redirect(url_for('admin_providers'))

# @app.route('/admin/provider/delete/<int:provider_id>')
# @login_required
# @admin_required
# def delete_provider(provider_id):
#     provider = Provider.query.get_or_404(provider_id)
#     db.session.delete(provider)
#     db.session.commit()
#     flash('Provider deleted successfully!', 'success')
#     return redirect(url_for('admin_providers'))

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.filter(User.user_type != 'admin').order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/toggle/<int:user_id>')
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.user_type == 'admin':
        flash('Cannot modify admin users!', 'error')
        return redirect(url_for('admin_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} {status} successfully!', 'success')
    return redirect(url_for('admin_users'))

# @app.route('/admin/user/delete/<int:user_id>')
# @login_required
# @admin_required
# def delete_user(user_id):
#     user = User.query.get_or_404(user_id)
#     if user.user_type == 'admin':
#         flash('Cannot delete admin users!', 'error')
#         return redirect(url_for('admin_users'))
    
#     # Delete associated provider profile if exists
#     Provider.query.filter_by(user_id=user_id).delete()
#     db.session.delete(user)
#     db.session.commit()
#     flash('User deleted successfully!', 'success')
#     return redirect(url_for('admin_users'))

@app.route('/admin/services')
@login_required
@admin_required
def admin_services():
    services = Service.query.order_by(Service.name).all()
    return render_template('admin/services.html', services=services)

@app.route('/admin/service/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon')
        
        if Service.query.filter_by(name=name).first():
            flash('Service already exists!', 'error')
            return redirect(url_for('add_service'))
        
        service = Service(name=name, description=description, icon=icon)
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/add_service.html')

@app.route('/admin/service/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.description = request.form.get('description')
        service.icon = request.form.get('icon')
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/edit_service.html', service=service)

# @app.route('/admin/service/delete/<int:service_id>')
# @login_required
# @admin_required
# def delete_service(service_id):
#     service = Service.query.get_or_404(service_id)
    
#     # Check if providers exist for this service
#     provider_count = Provider.query.filter_by(service_type=service.name).count()
#     if provider_count > 0:
#         flash(f'Cannot delete service! {provider_count} providers are registered under this category.', 'error')
#         return redirect(url_for('admin_services'))
    
#     db.session.delete(service)
#     db.session.commit()
#     flash('Service deleted successfully!', 'success')
#     return redirect(url_for('admin_services'))

@app.route('/admin/messages')
@login_required
@admin_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

# @app.route('/admin/message/delete/<int:message_id>')
# @login_required
# @admin_required
# def delete_message(message_id):
#     message = ContactMessage.query.get_or_404(message_id)
#     db.session.delete(message)
#     db.session.commit()
#     flash('Message deleted successfully!', 'success')
#     return redirect(url_for('admin_messages'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_settings():
    if request.method == 'POST':
        action=request.form.get('action')
        # Update admin password
        if action=='change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
        
            if not current_user.check_password(current_password):
                flash('Current password is incorrect!', 'error')
                return redirect(url_for('admin_settings'))
            
            if new_password != confirm_password:
                flash('Passwords do not match!', 'error')
                return redirect(url_for('admin_settings'))
            # Validate password
            is_valid, message = validate_password(new_password)
            if not is_valid:
                flash(message, 'error')
                return redirect(url_for('admin_settings'))
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        elif action == 'change_username':
            new_username = request.form.get('new_username')
            
            if User.query.filter_by(username=new_username).first():
                flash('Username already exists!', 'error')
                return redirect(url_for('admin_settings'))
            
            current_user.username = new_username
            db.session.commit()
            flash('Username updated successfully!', 'success')
        elif action =='change_email':
            new_email=request.form.get('new_email')
            confirm_password=request.form.get('confirm_password')
            if not current_user.check_password(confirm_password):
                flash('password is incorrect!','error')
                return redirect(url_for('admin_settings'))
            
            if new_email==current_user.email:
                flash('New email is same as current email!','error')
                return redirect(url_for('admin_settings'))

            if User.query.filter_by(email=new_email).first():
                flash('Email already exists!','error')
                return redirect(url_for('admin_settings'))
            email_pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern,new_email):
                flash('Invalid email format!','Error')
                return redirect(url_for('admin_settings'))
            current_user.email=new_email
            db.session.commit()
            flash('Email updated successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html')
 # ==================== PROVIDER ROUTES ====================

@app.route('/provider/dashboard')
@login_required
def provider_dashboard():
    if current_user.user_type != 'provider':
        flash('Access denied. Provider account required.', 'error')
        return redirect(url_for('index'))
    
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    if not provider:
        flash('Please complete provider registration first.', 'error')
        return redirect(url_for('register'))
    
    # Get provider statistics
    total_ratings = Rating.query.filter_by(provider_id=provider.id).count()
    recent_ratings = Rating.query.filter_by(provider_id=provider.id).order_by(Rating.created_at.desc()).limit(5).all()
    
    # Recalculate average rating
    avg_rating = db.session.query(func.avg(Rating.rating)).filter_by(provider_id=provider.id).scalar()
    if avg_rating:
        provider.rating = round(float(avg_rating), 1)
        provider.reviews_count = total_ratings
        db.session.commit()
    
    return render_template('provider/dashboard.html', 
                         provider=provider, 
                         total_ratings=total_ratings,
                         recent_ratings=recent_ratings)

@app.route('/provider/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_provider_profile():
    if current_user.user_type != 'provider':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    provider = Provider.query.filter_by(user_id=current_user.id).first()
    if not provider:
        flash('Provider profile not found.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        provider.business_name = request.form.get('business_name')
        provider.description = request.form.get('description')
        provider.location = request.form.get('location')
        
        # Handle photo upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                provider.photo = filename
        
        # Handle license upload
        if 'license' in request.files:
            file = request.files['license']
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    provider.license_document = filename
                else:
                    flash('Invalid license file format.', 'error')
                    return redirect(url_for('edit_provider_profile'))
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('provider_dashboard'))
    
    services = Service.query.all()
    return render_template('provider/edit_profile.html', provider=provider, services=services)



# ==================== USER ROUTES ====================

@app.route('/user/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect!', 'error')
            return redirect(url_for('change_password'))
        
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('change_password'))
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            flash(message, 'error')
            return redirect(url_for('change_password'))
        
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('user/change_password.html')

@app.route('/provider/rate/<int:provider_id>', methods=['POST'])
@login_required
def rate_provider(provider_id):
    if current_user.user_type == 'provider':
        flash('Providers cannot rate other providers.', 'error')
        return redirect(url_for('services'))
    
    provider = Provider.query.get_or_404(provider_id)
    rating_value = int(request.form.get('rating'))
    review_text = request.form.get('review', '')
    
    if rating_value < 1 or rating_value > 5:
        flash('Rating must be between 1 and 5', 'error')
        return redirect(url_for('provider_details', service_name=provider.service_type))
    
    # Check if user already rated this provider
    existing_rating = Rating.query.filter_by(provider_id=provider_id, user_id=current_user.id).first()
    
    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.review = review_text
        flash('Your rating has been updated!', 'success')
    else:
        new_rating = Rating(
            provider_id=provider_id,
            user_id=current_user.id,
            rating=rating_value,
            review=review_text
        )
        db.session.add(new_rating)
        flash('Thank you for your rating!', 'success')
    
    # Update provider average rating
    avg_rating = db.session.query(func.avg(Rating.rating)).filter_by(provider_id=provider_id).scalar()
    provider.rating = round(float(avg_rating), 1)
    provider.reviews_count = Rating.query.filter_by(provider_id=provider_id).count()
    
    db.session.commit()
    return redirect(url_for('provider_details', service_name=provider.service_type))
@app.route('/admin/provider/view/<int:provider_id>')
@login_required
@admin_required
def view_provider_profile(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    # licenses = ProviderLicense.query.filter_by(provider_id=provider_id).all()
    ratings = Rating.query.filter_by(provider_id=provider_id).order_by(Rating.created_at.desc()).all()
    return render_template('admin/view_provider.html', provider=provider, ratings=ratings)

@app.route('/admin/service/delete/<int:service_id>')
@login_required
@admin_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    # Check if providers exist for this service
    provider_count = Provider.query.filter_by(service_type=service.name).count()
    if provider_count > 0:
        flash(f'Cannot delete service! {provider_count} providers are registered under this category.', 'error')
        return redirect(url_for('admin_services'))
    
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_services'))

@app.route('/admin/provider/delete/<int:provider_id>')
@login_required
@admin_required
def delete_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    db.session.delete(provider)
    db.session.commit()
    flash('Provider deleted successfully!', 'success')
    return redirect(url_for('admin_providers'))

@app.route('/admin/user/delete/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.user_type == 'admin':
        flash('Cannot delete admin users!', 'error')
        return redirect(url_for('admin_users'))
    
    # Delete associated provider profile if exists
    Provider.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/message/delete/<int:message_id>')
@login_required
@admin_required
def delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin_messages'))


if __name__ == '__main__':
    init_db()
    port=int(os.environ.get('PORT',5000))
    debug=os.environ.get('FLASK_ENV')!='production'
    app.run(debug=debug, port=port,host='0.0.0.0')