from flask import Flask
from flask_migrate import Migrate
from models import db  # Import db from models
from routes import initialize_routes
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Set up your database URI (example using SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids overhead
app.config['JWT_SECRET_KEY'] = 'Hello_From_The_dark_side'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.config['DEFAULT_PROFILE_PIC'] = 'static/profile_pics/default_pic.png'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
jwt=JWTManager(app)

# Initialize the db with the app
db.init_app(app)

# Set up Flask-Migrate
migrate = Migrate(app, db)

# Initialize your routes
initialize_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
