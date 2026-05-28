from flask import (

    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (

    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (

    generate_password_hash,
    check_password_hash
)
from flask_login import logout_user
from models.database import db

from models.user_model import User

# =====================================
# BLUEPRINT
# =====================================

auth_bp = Blueprint(

    "auth",

    __name__
)

# =====================================
# LOGIN
# =====================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        user = User.query.filter_by(

            username=username

        ).first()

        if (

            user
            and
            check_password_hash(
                user.password,
                password
            )
        ):

            login_user(user)

            return redirect("/")

        flash("Invalid credentials")

    return render_template(

        "auth/login.html"
    )

# =====================================
# LOGOUT
# =====================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(

        url_for("auth.login")
    )

# =====================================
# REGISTER
# =====================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        existing_user = User.query.filter_by(

            username=username

        ).first()

        if existing_user:

            flash("Username already exists")

            return redirect("/register")

        hashed_password = generate_password_hash(
            password
        )

        user = User(

            username=username,

            email=email,

            password=hashed_password
        )

        db.session.add(user)

        db.session.commit()

        flash("Registration successful")

        return redirect("/login")

    return render_template(

        "auth/register.html"
    )
