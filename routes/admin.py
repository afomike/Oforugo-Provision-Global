from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db, normalize_image_url
from models import Product, Category, Order, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('shop.index'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    pending_orders = Order.query.filter_by(status='pending').count()
    from sqlalchemy import func
    revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.status.in_(['confirmed', 'delivered'])).scalar() or 0
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    low_stock = Product.query.filter(Product.stock < 20).all()
    return render_template('admin/dashboard.html', total_products=total_products,
                           total_orders=total_orders, total_users=total_users,
                           pending_orders=pending_orders, revenue=revenue,
                           recent_orders=recent_orders, low_stock=low_stock)


@admin_bp.route('/products')
@login_required
@admin_required
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', 0)
        stock = request.form.get('stock', 0)
        category_id = request.form.get('category_id', type=int)
        image_url = request.form.get('image_url', '').strip()
        featured = request.form.get('featured') == 'on'
        if not name or not price or not category_id:
            flash('Name, price and category are required.', 'danger')
            return render_template('admin/product_form.html', categories=categories, product=None)
        product = Product(name=name, description=description, price=float(price),
                          stock=int(stock), category_id=category_id,
                          image_url=normalize_image_url(image_url),
                          featured=featured)
        db.session.add(product)
        db.session.commit()
        flash(f'Product "{name}" added successfully.', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', categories=categories, product=None)


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        product.price = float(request.form.get('price', 0))
        product.stock = int(request.form.get('stock', 0))
        product.category_id = int(request.form.get('category_id'))
        product.image_url = normalize_image_url(request.form.get('image_url', ''))
        product.featured = request.form.get('featured') == 'on'
        product.active = request.form.get('active') == 'on'
        db.session.commit()
        flash(f'Product "{product.name}" updated.', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', categories=categories, product=product)


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.active = False
    db.session.commit()
    flash(f'Product "{product.name}" deactivated.', 'info')
    return redirect(url_for('admin.products'))


@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    query = Order.query.order_by(Order.created_at.desc())
    if status:
        query = query.filter_by(status=status)
    orders = query.paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders, status=status)


@admin_bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)


@admin_bp.route('/orders/<int:order_id>/update', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    valid = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
    if new_status in valid:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} status updated to {new_status}.', 'success')
    return redirect(url_for('admin.order_detail', order_id=order_id))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/categories/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    icon = request.form.get('icon', '').strip()
    if name:
        cat = Category(name=name, description=description, icon=icon)
        db.session.add(cat)
        db.session.commit()
        flash(f'Category "{name}" added.', 'success')
    return redirect(url_for('admin.categories'))
