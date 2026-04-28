from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Create Flask app
app = Flask(__name__)

# Configure SQLite database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Assuming instance folder is at project root
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, '..', '..', 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import and register blueprints
from .routes import recipe_bp, ingredient_bp
app.register_blueprint(recipe_bp, url_prefix='/')
app.register_blueprint(ingredient_bp, url_prefix='/')

# Ensure tables are created (for demo purposes)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
