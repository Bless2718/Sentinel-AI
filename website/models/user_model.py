from models.database import db
from flask_login import UserMixin

# =====================================
# USER MODEL
# =====================================

class User(

    UserMixin,

    db.Model
):

    __tablename__ = "users"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = db.Column(

        db.Integer,

        primary_key=True
    )

    # =====================================
    # USERNAME
    # =====================================

    username = db.Column(

        db.String(120),

        unique=True,

        nullable=False
    )

    # =====================================
    # EMAIL
    # =====================================

    email = db.Column(

        db.String(255),

        unique=True,

        nullable=False
    )

    # =====================================
    # PASSWORD HASH
    # =====================================

    password = db.Column(

        db.String(500),

        nullable=False
    )

    # =====================================
    # ROLE
    # =====================================

    role = db.Column(

        db.String(50),

        default="analyst"
    )