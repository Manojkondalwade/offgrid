import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    # Serve static files from the Frontend folder
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Frontend'))
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

    # ── Config ──────────────────────────────────────────────────────────
    app.config['SECRET_KEY']                = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['JWT_SECRET_KEY']            = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    app.config['SQLALCHEMY_DATABASE_URI']   = os.getenv('DATABASE_URL', 'sqlite:///offgrid.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES']  = False   # no expiry for prototype

    # ── Extensions ──────────────────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins='*')

    # ── Blueprints ──────────────────────────────────────────────────────
    from app.routes.auth      import auth_bp
    from app.routes.events    import events_bp
    from app.routes.student   import student_bp
    from app.routes.organizer import organizer_bp
    from app.routes.sponsor   import sponsor_bp

    app.register_blueprint(auth_bp,      url_prefix='/api/auth')
    app.register_blueprint(events_bp,    url_prefix='/api/events')
    app.register_blueprint(student_bp,   url_prefix='/api/student')
    app.register_blueprint(organizer_bp, url_prefix='/api/organizer')
    app.register_blueprint(sponsor_bp,   url_prefix='/api/sponsor')

    # ── Health check ────────────────────────────────────────────────────
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'OffGrid API is running 🚀'}

    # ── Serve Frontend index.html at root ───────────────────────────────
    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')

    # ── Create tables ───────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        from app.services.seed import seed_db
        seed_db()

    return app