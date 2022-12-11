from hack import app,db
from flask import render_template,redirect,url_for,request,flash,abort
from flask_login import login_user,login_required,logout_user,current_user
from hack.models import User, Product
from hack.forms import CarForm
from sqlalchemy import desc , asc
from werkzeug.security import generate_password_hash,check_password_hash
import flask
import stripe

public_key = 'pk_test_51MDqrBSCAN52haKfV41ZGub5BaDHsMifSLx7k8pIarvWNQDxBa6HqI72kwFbL1fkzd3tbd0vgNH33x4v52JuiMmy005urrKd9C'
stripe.api_key = 'sk_test_51MDqrBSCAN52haKfEnlc9YmjDKncApZvhLywRHz3VO7hrhZlkPOHxu0gZRSj3MM9Apzt7effye9XHjroD43KTNsV00g7fpuMVp'


@app.route('/')
def home():
    # prod1 = Product(id=1, name="Model-L", price=96600)
    # prod2 = Product(id=2, name="Model-M", price=96600)
    # db.session.add(prod1)
    # db.session.add(prod2)
    # db.session.commit()
    return render_template('HomePage.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    mess = 'Please fill the form to login to your account.'
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            mess = "Email not found."

    if current_user.is_authenticated:
        return abort(404)

    return render_template('Login.html', mess=mess)

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    mess = 'Please fill the form to create an account.'
    if request.method == 'POST':
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            mess = 'Email already exists.'
        elif password1 != password2:
            mess = "Passwords don't match"
        elif len(password1) < 6:
            mess = 'Password is too short'
        elif len(email) < 4:
            mess = 'Invalid email'
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('home'))

    if current_user.is_authenticated:
        return abort(404)

    return render_template('reg.html', mess=mess)

@app.route('/cart')
@login_required
def cart():
    name = []
    design = []
    # for i in current_user.products:
    #     design.append(i)
    #     name.append(i.products_[0].name)
    #     print('hi')
    ranges = range(len(design))
    return render_template('cart.html', name=name, design=design, ranges=ranges)


@app.errorhandler(404)
def handle_404(e):
    return render_template('error_404.html')

@app.route('/products/<name>', methods=['GET', 'POST'])
def display_product(name):
    product = Product.query.filter_by(name=name).first()
    form = CarForm()
    color_sel = form.colors.data
    model_sel = form.models.data
    return render_template('product.html', product=product, form=form, col=color_sel, mod=model_sel)
    
@app.route('/addtocart/<prod_id>/<name_>')
@login_required
def add(prod_id, name_):
    product = Product.query.filter_by(id=int(prod_id)).first()
    current_user.products.append(product)
    if current_user.product_names == '':
        current_user.product_names += name_
    else:
        current_user.product_names += ','+name_
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/payment/', methods=['POST'])
def payment_form(id):
    # product = Product.query.filter_by(id=id).first()
    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        amount= 96600,
        customer=customer.id,
        currency='usd',
        description='Premium'
    )

    return redirect(url_for('thankyou'))


if __name__ == '__main__':
    app.run(debug=True)
