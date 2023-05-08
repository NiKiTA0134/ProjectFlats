from app import app, login_manager
from flask import render_template, request, redirect, url_for
from app.db.database import session, User, Flats, Hryvnia, Dollar, Euro
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).where(User.id == user_id).first()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html", current_user=current_user)


@app.route("/message", methods=["POST", "GET"])
@login_required
def message():
    if request.method == "POST":
        message = request.form["message"]
        session.query(User).filter(User.id == current_user.id). \
            update({User.message: message}, synchronize_session='evaluate')
        session.commit()
        session.close()
        return redirect("answer")
    return render_template("message.html")


@app.route("/answer", methods=["POST", "GET"])
@login_required
def answer():
    if request.method == "GET":
        message = session.query(User).all()
        print(message)
    return render_template("answer.html", message=message)


@app.route("/admin_answer", methods=["POST", "GET"])
@login_required
def admin_answer():
    if request.method == "POST":
        answer = request.form["answer"]
        id = request.form["id"]
        session.query(User).filter(User.id == id). \
            update({User.answer: answer}, synchronize_session='evaluate')
        session.commit()
        session.close()
        return redirect("answer")

    if request.method == "GET":
        answers = session.query(User).all()
        print(answers)
        return render_template("admin_answer.html", answers=answers)
    return render_template("admin_answer.html")


@app.route("/bot")
def bot():
    return render_template("bot.html")


@app.route("/pay")
@login_required
def pay():
    return render_template("pay.html")


@app.route("/not_now", methods=["POST", "GET"])
@login_required
def not_now():
    if request.method == "POST":
        return render_template("not_now.html")
    return render_template("not_now.html")


@app.route("/addflats", methods=["POST", "GET"])
@login_required
def addflats():
    if request.method == "POST":
        name = request.form["name"]
        street = request.form["street"]
        floor = request.form["floor"]
        room = request.form["room"]
        size = request.form["size"]
        near = request.form["near"]
        price = request.form["price"]
        position = request.form["position"]
        currency = request.form["currency"]

        new_flat = Flats(name=name, street=street, floor=floor, size=size, room=room, near=near, price=price, position=position, currency=currency)
        print(new_flat)
        session.add(new_flat)
        session.commit()
        session.close()
        return render_template("main.html")
    return render_template("addflats.html")


@app.route("/showflats", methods=["POST", "GET"])
@login_required
def showflats():
    if request.method == "GET":
        flat = session.query(Flats).all()
    return render_template("showflats.html", flat=flat)


@app.route("/single_flat/<id>")
@login_required
def singleflat(id):
    dollareuro = session.query(Dollar).first().dollar_euro
    dollarhryvnia = session.query(Dollar).first().dollar_hryvnia

    flat = session.query(Flats).where(Flats.id == id).first()

    price_now = session.query(Flats).where(Flats.id == id).first().price

    print(11111111111111111111111111111111111111111)
    cost_de = price_now * dollareuro
    r_cost_de = round(cost_de)
    print(r_cost_de)
    cost_dh = price_now * dollarhryvnia
    r_cost_dh = round(cost_dh)
    print(r_cost_dh)
    return render_template("single_flat.html", flat=flat, r_cost_de=r_cost_de, r_cost_dh=r_cost_dh)


@app.route("/currency", methods=["POST", "GET"])
@login_required
def currency():
    if request.method == "POST":
        hryvnia_dollar = request.form["hryvnia_dollar"]
        hryvnia_euro = request.form["hryvnia_euro"]
        dollar_hryvnia = request.form["dollar_hryvnia"]
        dollar_euro = request.form["dollar_euro"]
        euro_dollar = request.form["euro_dollar"]
        euro_hryvnia = request.form["euro_hryvnia"]

        new_currency_hryvnia = Hryvnia(hryvnia_dollar=hryvnia_dollar, hryvnia_euro=hryvnia_euro)
        new_currency_dollar = Dollar(dollar_hryvnia=dollar_hryvnia, dollar_euro=dollar_euro)
        new_currency_euro = Euro(euro_dollar=euro_dollar, euro_hryvnia=euro_hryvnia)

        session.add(new_currency_hryvnia)
        session.add(new_currency_dollar)
        session.add(new_currency_euro)
        session.commit()
        session.close()
    return render_template("currency.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        message = None
        answer = None
        currency = request.form["currency"]
        nickname = request.form["nickname"]
        password = request.form["password"]
        email = request.form["email"]

        user = session.query(User).where(User.nickname == nickname).first()

        if user:
            return redirect(url_for("signup"))

        new_user = User(nickname=nickname, email=email, password=generate_password_hash(password), message=message, answer=answer, currency=currency)
        session.add(new_user)
        session.commit()
        session.close()
        return redirect("login")
    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        remember = True if request.form.get("remember") else False

        user = session.query(User).where(User.nickname == nickname).first()

        if not user or not check_password_hash(user.password, password):
            print("Test? Test? Test?")
            return redirect(url_for("login"))
        login_user(user)
        return redirect("main")
    return render_template("login.html")


@app.route("/apipage")
def test():
    import requests

    response = requests.get('https://www.boredapi.com/api/activity')
    print(response)
    if response.status_code == 200:
        data = response.json()["activity"]
    else:
        data = "ERROR"
    print(data)
    return render_template("apipage.html", data=data)

