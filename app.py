from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime

#Create a new flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # In production, use a secure random key

# Our "database" of sock products
socks = {
    1: {
        'id': 1,
        'name': 'Meme Lord',
        'description': 'Custom socks with your favorite internet meme',
        'base_price': 12.99,
        'image': 'meme_socks.jpg',
        'category': 'funny'
    },
    2: {
        'id': 2,
        'name': 'Campus Pride',
        'description': 'Show your school spirit with custom logo socks',
        'base_price': 14.99,
        'image': 'campus_socks.jpg',
        'category': 'school'
    },
    3: {
        'id': 3,
        'name': 'Quote Master',
        'description': 'Custom socks with your favorite quote or inside joke',
        'base_price': 13.99,
        'image': 'quote_socks.jpg',
        'category': 'funny'
    }
}

# Function to get available socks
def get_available_products(category=None):
    if category:
        return [product for product in socks.values() if product['category'] == category]
    return list(socks.values())

# Function to get a specific sock by ID
def get_product_by_id(product_id):
    return socks.get(int(product_id))

# Function to get all categories
def get_all_categories():
    categories = set()
    for product in socks.values():
        categories.add(product['category'])
    return list(categories)

# Initialize shopping cart in session
@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []

#Route for the home page
#Home() funtion sets up the home page, so it gets the products and categrories,
#Then adds them to the index.html file that serve as template for the home page
@app.route('/')
def home():
    category = request.args.get('category')
    products = get_available_products(category)
    categories = get_all_categories()
    return render_template('index.html', products=products, categories=categories, current_category=category)

#Route for the products page
#product_detail() funtion sets up the product_detail page
#It display the infor

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return redirect(url_for('home'))
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    custom_text = request.form.get('custom_text', '')
    
    product = get_product_by_id(product_id)
    if not product:
        return redirect(url_for('home'))
        
    cart_item = {
        'product_id': product_id,
        'name': product['name'],
        'price': product['base_price'],
        'quantity': quantity,
        'custom_text': custom_text,
        'total': product['base_price'] * quantity
    }
    
    cart = session.get('cart', [])
    cart.append(cart_item)
    session['cart'] = cart
    
    return redirect(url_for('cart'))




#route for cart page
#the cart() funtion sets up the cart page,and gets the cart with the items
#for the current session
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['total'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)




@app.route('/checkout')

def checkout():

    cart = session.get('cart', [])

    if not cart:

        return redirect(url_for('home'))

    

    total = sum(item['total'] for item in cart)

    return render_template('checkout.html', cart=cart, total=total)


@app.route('/complete_order', methods=['POST'])

def complete_order():

    # Get customer information

    name = request.form.get('name')

    email = request.form.get('email')

    

    # Clear the cart

    session['cart'] = []

    

    # Show thank you page

    return render_template('thank_you.html', name=name, email=email)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
