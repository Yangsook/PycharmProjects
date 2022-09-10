from flask import Flask, render_template, redirect, url_for, flash, abort, jsonify
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, RegisterForm, CreateItemForm, ShowItemForm, ShowCartForm
import stripe


app = Flask(__name__)
app.config['SECRET_KEY'] = 'onlineshop'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51LZU7tJDdM0RhJG9gAMKGIyZw1hxtfaFB35oIo3QV2LqL2mRBE7FwN6MCH016qY2OlkWI4AMW69RG53Rqgfaefby00DushM0qZ'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51LZU7tJDdM0RhJG99TJR35Wx0BslTGtpLs49xLx4Tj8XSlIWm6wLQM25bWHCS2Du4Cpyp3iGsqVY5E77IIUbrMBW00VRtpCX8f'

stripe.api_key = app.config['STRIPE_SECRET_KEY']
YOUR_DOMAIN = 'http://localhost:5000'


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlineshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    tel = db.Column(db.String(100))

    cart = relationship("ShopCart", back_populates="cart_user")

class ShopItem(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(250), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    cart = relationship("ShopCart", back_populates="cart_item")

class ShopCart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(250), nullable=False)

    cart_user = relationship("User", back_populates="cart")
    cart_item = relationship("ShopItem", back_populates="cart")

db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def get_all_item():
    items = ShopItem.query.all()
    return render_template("index.html", all_item=items, current_user=current_user)

@app.route('/pricing-page')
def pricing_page():
    return render_template("sample_pricing_page.html", current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            # print(User.query.filter_by(email=form.email.data).first())
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
            address=form.address.data,
            tel=form.tel.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_item"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_item'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_item'))


@app.route("/item/<int:item_id>", methods=["GET", "POST"])
def show_item(item_id):
    form = ShowItemForm()
    requested_item = ShopItem.query.get(item_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register!")
            return redirect(url_for("login"))

        if int(form.count.data) == 0:
            flash("Select count!")
            return redirect(url_for('show_item', item_id=item_id))
        else:
            new_cart = ShopCart(
                user_id=int(current_user.id),
                item_id=item_id,
                count=form.count.data,
                status=0,
                price=requested_item.price,
                date=datetime.now().strftime("%Y-%m-%d %X"),
                # date=date.today().strftime("%B %d, %Y"),
            )
            db.session.add(new_cart)
            db.session.commit()
            return redirect(url_for('show_cart'))

    return render_template("item.html", item=requested_item, form=form, current_user=current_user)


@app.route("/cart_save_item/<int:cart_id>", methods=["GET", "POST"])
def save_for_later(cart_id):
    rows_updated = ShopCart.query.filter_by(id=cart_id, status=0).update(
        dict(status=2, date=datetime.now().strftime("%Y-%m-%d %X")))
    db.session.commit()
    return redirect(url_for("show_cart"))


@app.route("/cart_move_item/<int:cart_id>", methods=["GET", "POST"])
def move_to_cart(cart_id):
    rows_updated = ShopCart.query.filter_by(id=cart_id, status=2).update(dict(status=0, date=datetime.now().strftime("%Y-%m-%d %X")))
    db.session.commit()
    return redirect(url_for("show_cart"))


@app.route("/cart_delete_item/<int:cart_id>")
def cart_item_delete(cart_id):
    item_to_delete = ShopCart.query.get(cart_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('show_cart'))


@app.route("/cart", methods=["GET", "POST"])
@login_required
def show_cart():
    form = ShowCartForm()
    my_cart_item = ShopCart.query.filter_by(user_id=current_user.id, status=0)
    my_save_item = ShopCart.query.filter_by(user_id=current_user.id, status=2)

    global payable_amount
    global cart_list

    cart_list = ""
    total_price = 0

    # 데이터를 장바구니에 넘길때 카운트 할 수 있게 리스트 타입으로 넘겨주기 위해..
    list_cart_item = []
    for data in my_cart_item:
        list_cart_item.append(data)
        total_price += data.price * 100 * data.count
        print(data.price * data.count)
        print(total_price)

    # payable_amount = total_price + (0.05 * total_price) - 1
    payable_amount = int(total_price)

    # payable_amount = round(total_price, 2)
    cart_list = ', '.join([data.cart_item.item_name + ' ' + str(data.count) + '($' + str(data.cart_item.price) +')' for data in my_cart_item])

    print(payable_amount)
    print(cart_list)


    list_save_item = []
    for data in my_save_item:
        list_save_item.append(data)

    if form.validate_on_submit():
        rows_updated = ShopCart.query.filter_by(user_id=current_user.id, status=0).update(dict(status = 1, date = datetime.now().strftime("%Y-%m-%d %X")))
        db.session.commit()
        return redirect(url_for("get_all_ordered"))

    return render_template("cart.html", items=list_cart_item, save_items=list_save_item, form=form, current_user=current_user,
                           public_key=app.config['STRIPE_PUBLIC_KEY'], payable_amount=payable_amount)



# Book_Mart 참고 ============================================================================================
@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': cart_list,
                },
                'unit_amount': payable_amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        # success_url="https://book--mart.herokuapp.com/success",
        # cancel_url="https://book--mart.herokuapp.com/failed"
        success_url = url_for("succeed", _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = url_for("failed", _external=True),

    )
    response = jsonify({'id': checkout_session.id})
    return response

    # return redirect(checkout_session.url, code=303)


@app.route("/succeed")
@login_required
def succeed():
    global cart_list
    cart_list = ""

    rows_updated = ShopCart.query.filter_by(user_id=current_user.id, status=0).update(dict(status = 1, date = datetime.now().strftime("%Y-%m-%d %X")))
    db.session.commit()

    return render_template("pay_succeed.html", current_user=current_user)


@app.route("/failed")
@login_required
def failed():
    return render_template('pay_failed.html', current_user=current_user)

# Book_Mart 참고 end  ============================================================================================






@app.route('/orderhistory')
def get_all_ordered():
    items = ShopCart.query.filter_by(user_id=current_user.id, status=1)
    return render_template("orderhistory.html", items=items, current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


@app.route("/new-item", methods=["GET", "POST"])
@admin_only
def add_new_item():
    form = CreateItemForm()
    if form.validate_on_submit():
        new_item = ShopItem(
            item_name=form.item_name.data,
            price=form.price.data,
            img_url=form.img_url.data,
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("get_all_item"))

    return render_template("make-item.html", form=form, current_user=current_user)


@app.route("/edit-item/<int:item_id>", methods=["GET", "POST"])
@admin_only
def edit_item(item_id):
    item = ShopItem.query.get(item_id)
    edit_form = CreateItemForm(
        item_name=item.item_name,
        img_url=item.img_url,
        price=item.price
    )
    if edit_form.validate_on_submit():
        item.item_name = edit_form.item_name.data
        item.img_url = edit_form.img_url.data
        item.price = edit_form.price.data
        db.session.commit()
        return redirect(url_for("get_all_item"))

    return render_template("make-item.html", form=edit_form, is_edit=True, current_user=current_user)


@app.route("/delete/<int:item_id>")
@admin_only
def delete_item(item_id):
    item_to_delete = ShopItem.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_item'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
