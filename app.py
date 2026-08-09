import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def normalize_image_url(image_url):
    if not image_url:
        return '/static/images/placeholder.jpg'

    value = str(image_url).strip()
    if value.startswith(('http://', 'https://')):
        return value

    value = value.replace('\\', '/')
    value = value.lstrip('/')

    if value.startswith('static/'):
        return '/' + value
    if value.startswith('images/'):
        return '/static/' + value
    if value.startswith('uploads/'):
        return '/' + value
    return '/static/images/' + value if not value.startswith('images/') else '/static/' + value


def create_app():
    app = Flask(__name__)
    app.jinja_env.globals['normalize_image_url'] = normalize_image_url
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'oforugo-secret-key-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['PAYSTACK_PUBLIC_KEY'] = os.environ.get('PAYSTACK_PUBLIC_KEY', 'pk_test_demo')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.shop import shop_bp
    from routes.cart import cart_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    from models import User, Category, Product
    from werkzeug.security import generate_password_hash

    if User.query.filter_by(email='admin@oforugo.com').first():
        return

    admin = User(
        username='admin',
        email='admin@oforugo.com',
        password_hash=generate_password_hash('admin123'),
        is_admin=True,
        full_name='Admin User',
        phone='08000000000'
    )
    db.session.add(admin)

    categories = [
        Category(name='Food & Provisions', description='Rice, beans, garri, oil, flour, spices and more', icon='🍚'),
        Category(name='Beverages', description='Soft drinks, water, juice, beer, wine and spirits', icon='🥤'),
        Category(name='Household Items', description='Cleaning supplies, toiletries and home essentials', icon='🏠'),
        Category(name='Snacks & Confectionery', description='Biscuits, chocolates, candies and snacks', icon='🍫'),
        Category(name='Condiments & Sauces', description='Tomato paste, seasoning cubes, pepper, salt', icon='🧂'),
        Category(name='Baby Products', description='Baby food, diapers, cream and accessories', icon='👶'),
    ]
    for cat in categories:
        db.session.add(cat)
    db.session.flush()

    products = [
        Product(name='Golden Penny Rice (25kg)', description='Premium quality long grain parboiled rice. Perfect for all Nigerian meals. Clean, sorted and hygienic.', price=32000, stock=150, category_id=categories[0].id, image_url='/static/images/rice.jpg', featured=True),
        Product(name='Dangote Flour (10kg)', description='Fortified wheat flour for baking bread, pastries and other flour-based products. Rich in essential vitamins.', price=8500, stock=200, category_id=categories[0].id, image_url='/static/images/flour.jpg', featured=True),
        Product(name='Kings Vegetable Oil (5L)', description='100% pure vegetable oil. Ideal for frying, cooking and baking. Cholesterol free and rich in Vitamin E.', price=12000, stock=120, category_id=categories[0].id, image_url='/static/images/oil.jpg', featured=True),
        Product(name='Peak Milk Powder (2.5kg)', description='Full cream milk powder packed with calcium and essential nutrients. Great for adults and children alike.', price=9800, stock=85, category_id=categories[0].id, image_url='/static/images/milk.jpg'),
        Product(name='Garri (10kg Bag)', description='Premium quality white garri, finely processed and dried. Great for eba or drinking with cold water.', price=5500, stock=200, category_id=categories[0].id, image_url='/static/images/garri.jpg'),
        Product(name='Coca-Cola (24 Cans)', description='Refreshing Coca-Cola canned drinks. 330ml per can. Serve chilled for best taste.', price=7200, stock=300, category_id=categories[1].id, image_url='/static/images/coke.jpg', featured=True),
        Product(name='Eva Water (12 x 1.5L)', description='Pure and safe natural spring water. Refreshing and healthy hydration for the whole family.', price=2400, stock=500, category_id=categories[1].id, image_url='/static/images/water.jpg'),
        Product(name='Milo Tin (500g)', description='Energy-giving chocolate malt drink. Packed with vitamins and minerals for active lifestyles.', price=4200, stock=150, category_id=categories[1].id, image_url='/static/images/milo.jpg'),
        Product(name='Ariel Detergent (3kg)', description='Powerful laundry detergent that removes tough stains. Leaves clothes clean, fresh and bright.', price=6500, stock=180, category_id=categories[2].id, image_url='/static/images/ariel.jpg'),
        Product(name='Dettol Antiseptic (750ml)', description='Multi-purpose antiseptic liquid. Kills 99.9% of germs. Ideal for wound cleaning and surface disinfection.', price=2800, stock=250, category_id=categories[2].id, image_url='/static/images/dettol.jpg'),
        Product(name='Snickers (12 bars)', description='Delicious chocolate bars filled with caramel, nougat and peanuts. Perfect snack any time of day.', price=5400, stock=200, category_id=categories[3].id, image_url='/static/images/snickers.jpg'),
        Product(name='Indomie Noodles (40 packs)', description='Nigeria\'s favourite instant noodles. Quick to prepare, delicious and satisfying. Various flavours available.', price=8000, stock=400, category_id=categories[3].id, image_url='/static/images/indomie.jpg', featured=True),
        Product(name='Maggi Cubes (100 cubes)', description='Classic seasoning cubes that add rich flavour to all your Nigerian dishes. A kitchen essential.', price=1500, stock=500, category_id=categories[4].id, image_url='/static/images/maggi.jpg'),
        Product(name='Tomato Paste (70g x 12)', description='Rich, thick tomato paste for cooking soups, stews and sauces. Made from fresh ripe tomatoes.', price=3600, stock=300, category_id=categories[4].id, image_url='/static/images/tomato.jpg'),
        Product(name='Pampers Baby Diapers (Large)', description='Super absorbent diapers for babies. Gentle on skin, leak-proof protection for up to 12 hours.', price=12500, stock=100, category_id=categories[5].id, image_url='/static/images/pampers.jpg'),
    ]
    for prod in products:
        db.session.add(prod)

    db.session.commit()
