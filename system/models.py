from datetime import datetime
from typing import Set

from system import db, login_manager
from flask_login import UserMixin




@login_manager.user_loader
def get_user_by_id(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    preparation = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    picture = db.Column(db.String(20), nullable=False, default="food_image.png")
    categories = db.Column(Set[str], nullable=False, default="Други")

    def __repr__(self):
        return f"Recipe('{self.title}', '{self.ingredients}', '{self.preparation}', '{self.category}')"

    def sort_recipes_by_category(self, category):
        return Recipe.query.filter(Recipe.categories.contains(category)).all()


    def sort_recipes_by_date(self):
        return Recipe.query.order_by(Recipe.date_posted.desc()).all()

    def sort_recipes_by_ingredient(self, ingredient):
        return Recipe.query.filter(Recipe.ingredients.contains(ingredient)).all()




