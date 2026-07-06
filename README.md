# Oforugo Provision Global - Beginner-Friendly Project Documentation

Welcome to Oforugo Provision Global. This project is a web-based grocery and provision store built with Python and Flask. It allows users to browse products, add items to a cart, place orders, and for admins to manage products, orders, users, and categories.

If you are completely new to programming, do not worry. This guide explains the project in simple words and also connects the explanation to the actual code files.

---

## 1. What this project does

This application is a small online shop for everyday items such as:

- food and groceries
- drinks
- household supplies
- snacks
- baby products

A normal customer can:

- create an account
- log in
- view products
- search products
- add products to the cart
- checkout and place an order

An admin can:

- add or edit products
- manage categories
- view user accounts
- view and update orders

---

## 2. What tools were used

This project uses the following main technologies:

- Python: the main programming language
- Flask: a lightweight web framework for building websites
- Flask-SQLAlchemy: helps work with a database using Python classes
- Flask-Login: handles user login and authentication
- Jinja2: used in HTML templates to display dynamic data
- SQLite/PostgreSQL support: used to store data
- HTML, CSS, and JavaScript: used for the website design and small interactive features

---

## 3. Main project structure

Here is the project layout:

```text
app.py                 # creates the Flask app and configures the database
models.py             # defines the database tables
run.py                 # starts the app
write.py               # generates a session secret
requirements.txt       # lists Python packages needed
routes/                # contains the app's pages and logic
static/                # CSS, JavaScript, images
templates/             # HTML pages shown to users
```

Each file has a responsibility. We will explain them one by one.

---

## 4. How the application works

A web application works like this:

1. A browser sends a request to the website.
2. Flask receives the request.
3. Flask checks which route (page) should handle the request.
4. The route gets data from the database if needed.
5. Flask sends the data to an HTML template.
6. The template renders the page and shows it in the browser.

In this project, the routes are stored in the routes folder.

---

## 5. The key files explained

### 5.1 app.py

This is the heart of the project.

It does several important jobs:

- creates the Flask application
- sets configuration values such as secret keys and database connection
- initializes the database
- registers the different route blueprints
- creates database tables
- seeds the database with sample data

#### Important ideas in app.py

```python
app = Flask(__name__)
```

This line creates the main Flask app object.

```python
db.init_app(app)
```

This connects SQLAlchemy to the Flask app so models can be stored in the database.

```python
def create_app():
```

This is a factory function. Instead of building the app in one place only, it creates the app when needed. This is a common Flask pattern and makes the app easier to manage.

```python
with app.app_context():
    db.create_all()
    seed_data()
```

This block tells Flask to create the database tables and insert sample data.

#### What seed_data() does

The seed_data() function adds:

- an admin user
- categories such as food, beverages, household items, and snacks
- example products

This means the store is not empty when you launch it for the first time.

---

### 5.2 models.py

This file defines the database structure.

Think of it as a blueprint for the data the app stores.

Each class in this file becomes a table in the database.

#### User

The User model stores account information for customers and admins.

Fields include:

- username
- email
- password_hash
- full_name
- phone
- address
- is_admin

This model represents a user account.

#### Category

A category groups products. For example:

- Food & Provisions
- Beverages
- Household Items

#### Product

The Product model stores items sold in the shop.

Fields include:

- name
- description
- price
- stock
- category_id
- image_url
- featured
- active

This is the central table for the inventory.

#### CartItem

This stores items currently in a user’s shopping cart.

#### Order

This records a completed or pending order.

#### OrderItem

This stores each product inside an order.

---

### 5.3 run.py

This file starts the web server.

It imports create_app() from app.py and runs the application.

```python
app = create_app()
```

This creates the app object.

```python
app.run(host='0.0.0.0', port=port, debug=False)
```

This tells Flask to start the server so the site can be opened in the browser.

---

### 5.4 write.py

This script generates a random session secret.

A session secret is used to protect user sessions. It helps keep login data secure.

You usually do not need to edit this unless you want to change the method used to create the secret.

---

## 6. How the routes work

The routes folder contains the main web logic for the app.

### 6.1 routes/auth.py

This file handles everything related to authentication:

- login
- registration
- logout
- profile updates

#### Login logic

When a user clicks login, the app checks whether the email and password match a user in the database.

If the credentials are correct, Flask-Login creates a session so the user stays logged in.

#### Registration logic

The registration page collects details such as:

- username
- email
- full name
- phone number
- password

If the details are valid, a new user record is added to the database.

#### Profile page

The profile route lets authenticated users update their information and view their past orders.

---

### 6.2 routes/shop.py

This file handles the customer-facing store pages.

It contains routes for:

- the homepage
- the products listing page
- the product detail page

#### Homepage

The homepage shows:

- featured products
- product categories
- total number of products available

#### Products page

This route lets users:

- browse products
- search for items
- sort by name or price
- filter by category

#### Product detail page

This page shows details for one specific product.

---

### 6.3 routes/cart.py

This file manages the shopping cart and checkout process.

It contains routes for:

- viewing the cart
- adding items to the cart
- updating quantity
- removing items
- checking out
- showing order confirmation

#### Adding to cart

When a user clicks add to cart:

1. the selected product is found in the database
2. the app checks the product stock
3. the item is added to the database as a cart record

#### Checkout

When a user checks out:

1. the cart items are collected
2. the total amount is calculated
3. the order is created
4. order items are saved
5. stock is reduced
6. cart items are cleared

This is the main process behind turning a shopping cart into an order.

---

### 6.4 routes/admin.py

This file controls the admin dashboard and admin-only features.

It includes routes for:

- viewing the dashboard
- managing products
- viewing orders
- updating order status
- viewing users
- managing categories

#### Admin protection

The admin_required decorator ensures that only admin users can access admin pages.

It checks whether the user is logged in and whether they are marked as an admin.

---

## 7. How the templates work

The HTML pages are stored in the templates folder.

Examples include:

- templates/shop/index.html -> homepage
- templates/shop/products.html -> product listing page
- templates/shop/cart.html -> cart page
- templates/auth/login.html -> login form
- templates/admin/dashboard.html -> admin overview page

These pages use Jinja2 syntax to display data from Python.

Example:

```html
<h1>{{ product.name }}</h1>
```

This means: display the product’s name inside the HTML page.

---

## 8. How to set up the project locally

### Step 1: Open the project folder

Open the project folder in your terminal or VS Code.

### Step 2: Create a Python environment

If you are using Anaconda, you can create an environment like this:

```bash
conda create -n oforugo-env python=3.11
conda activate oforugo-env
```

### Step 3: Install the required packages

Run:

```bash
pip install -r requirements.txt
```

### Step 4: Run the app

```bash
python run.py
```

Then open the browser and go to:

```text
http://127.0.0.1:5000/
```

---

## 9. Default login details

When the app starts for the first time, it seeds an admin account:

- email: admin@oforugo.com
- password: admin123

You can log in with those details and access the admin pages.

---

## 10. Database explanation

The app stores its data in a database.

When the app starts, Flask-SQLAlchemy creates the tables from the models in models.py.

This means you do not need to manually create the tables in most cases.

If the database is empty, the app seeds it with sample data.

---

## 11. A beginner-friendly explanation of the main code patterns

### 11.1 Routes

Routes are like pages in the website.

Example:

```python
@shop_bp.route('/')
def index():
```

This means: when someone visits the homepage, run the index() function.

### 11.2 Decorators

Decorators are special Python instructions placed above a function.

Example:

```python
@login_required
def profile():
```

This means the profile page can only be accessed by logged-in users.

### 11.3 Database queries

Example:

```python
Product.query.filter_by(active=True).all()
```

This means: get all active products from the database.

### 11.4 Templates

Templates are HTML files that receive data from the Python code.

Example:

```python
return render_template('shop/products.html', products=products)
```

This sends the products data into the products page template.

---

## 12. Where to make common changes

### Add a new product

You can add a product through the admin panel, or you can add one in the database seed data inside app.py.

### Change the site style

Edit the CSS files in the static/css folder.

### Change the homepage content

Edit the template in templates/shop/index.html or the route in routes/shop.py.

### Add a new page

1. create a new route in a route file
2. create a new HTML template in templates/
3. link to it from the website when needed

---

## 13. Common beginner mistakes

- forgetting to install dependencies from requirements.txt
- running the app from the wrong folder
- not activating the Python environment
- forgetting the database is created automatically
- trying to access admin pages without logging in as admin

---

## 14. Summary

This project is a full-featured Flask online grocery store.

It includes:

- user accounts
- product browsing
- cart management
- order processing
- admin dashboard features
- database-backed content

The application is a great beginner project because it shows how Python, Flask, HTML, and databases can work together to build a real web application.

---

## 15. Suggested next steps for learning

If you want to understand the project better, try these next:

1. read app.py first
2. then read models.py
3. then read routes/shop.py and routes/cart.py
4. then explore the templates
5. try adding a new product or a new route

You will understand the project much better after going through it step by step.
