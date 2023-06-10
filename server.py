from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from config import DBUSER,DBHOST,DBPASS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/postgres'
app.config['SECRET_KEY'] = 'ju43hgri2347rs'
CORS(app)
db = SQLAlchemy(app)
api = Api(app)

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False,unique=True)
    image = db.Column(db.String(200),nullable=False)
    dishes = db.relationship('Dish',backref = 'category')

    def serialize(self):
        return {
        "id":self.id,
        "name":self.name,
        "image":self.image
    }

class Dish(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable=False,unique=True)
    price = db.Column(db.Integer,nullable=False)
    description = db.Column(db.Text,nullable=False)
    image = db.Column(db.String(200),nullable=False)
    is_gluten_free = db.Column(db.String(200),nullable=False)
    is_vegeterian = db.Column(db.String(200),nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    

    def serialize(self):
        return {
        "id":self.id,
        "name":self.name,
        "image":self.image,
        "price":self.price,
        "description":self.description,
        "is_gluten_free":self.is_gluten_free,
        "is_vegeterian":self.is_vegeterian,
        "category_id":self.category_id        
    } 
with app.app_context():
    db.create_all()

class CategoriesAll(Resource):
    def get(self):
        categories = Category.query.all() 
        return [category.serialize() for category in categories] 

class CategoryDishes(Resource):
    def get(self,category_id):
        category = Category.query.filter_by(id=category_id).first()
        if category is None:
            return {
                "message":"product not found"
            }, 404
        return [category.serialize() for category in category.dishes]

api.add_resource(CategoriesAll,'/categories')
api.add_resource(CategoryDishes,'/category/<int:category_id>') 
    

app.run(debug=True,host="0.0.0.0")