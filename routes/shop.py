from flask import Blueprint, render_template, request
from models import Product, Category

shop_bp = Blueprint('shop', __name__)


@shop_bp.route('/')
def index():
    featured = Product.query.filter_by(featured=True, active=True).limit(8).all()
    categories = Category.query.all()
    total_products = Product.query.filter_by(active=True).count()
    return render_template('shop/index.html', featured=featured, categories=categories, total_products=total_products)


@shop_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'name')

    query = Product.query.filter_by(active=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.name.asc())

    pagination = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()
    return render_template('shop/products.html', products=pagination.items, pagination=pagination,
                           categories=categories, current_category=category_id, search=search, sort=sort)


@shop_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter_by(category_id=product.category_id, active=True).filter(
        Product.id != product_id).limit(4).all()
    return render_template('shop/product_detail.html', product=product, related=related)
