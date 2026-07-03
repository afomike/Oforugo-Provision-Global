from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import CartItem, Product, Order, OrderItem

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items)
    return render_template('shop/cart.html', items=items, total=total)


@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    existing = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        new_qty = existing.quantity + quantity
        if new_qty > product.stock:
            flash(f'Only {product.stock} units available in stock.', 'warning')
            return redirect(request.referrer or url_for('shop.products'))
        existing.quantity = new_qty
    else:
        if quantity > product.stock:
            flash(f'Only {product.stock} units available in stock.', 'warning')
            return redirect(request.referrer or url_for('shop.products'))
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    flash(f'"{product.name}" added to cart.', 'success')
    return redirect(request.referrer or url_for('shop.products'))


@cart_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        db.session.delete(item)
    elif quantity > item.product.stock:
        flash(f'Only {item.product.stock} units available.', 'warning')
        return redirect(url_for('cart.cart'))
    else:
        item.quantity = quantity
    db.session.commit()
    return redirect(url_for('cart.cart'))


@cart_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart.cart'))


@cart_bp.route('/cart/count')
@login_required
def cart_count():
    count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'count': count})


@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    from flask import current_app
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop.products'))
    total = sum(item.product.price * item.quantity for item in items)
    if request.method == 'POST':
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        payment_method = request.form.get('payment_method', 'pay_on_delivery')
        paystack_reference = request.form.get('paystack_reference', '').strip()
        notes = request.form.get('notes', '').strip()
        if not address or not phone:
            flash('Delivery address and phone number are required.', 'danger')
            return render_template('shop/checkout.html', items=items, total=total,
                                   paystack_public_key=current_app.config['PAYSTACK_PUBLIC_KEY'])

        status = 'paid' if payment_method == 'paystack' and paystack_reference else 'pending'

        order = Order(
            user_id=current_user.id,
            total_amount=total,
            delivery_address=address,
            phone=phone,
            payment_method=payment_method,
            paystack_reference=paystack_reference or None,
            notes=notes,
            status=status
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.product.price
            )
            db.session.add(order_item)
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
            db.session.delete(item)

        db.session.commit()
        if payment_method == 'paystack':
            flash(f'Payment successful! Order #{order.id} confirmed. Reference: {paystack_reference}', 'success')
        else:
            flash(f'Order #{order.id} placed successfully! We will contact you shortly.', 'success')
        return redirect(url_for('cart.order_confirmation', order_id=order.id))

    from flask import current_app
    return render_template('shop/checkout.html', items=items, total=total,
                           paystack_public_key=current_app.config['PAYSTACK_PUBLIC_KEY'])


@cart_bp.route('/order/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('shop/order_confirmation.html', order=order)
