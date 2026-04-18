from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20), nullable=False, default='student')
    # role: 'student' | 'organizer' | 'sponsor'
    degree     = db.Column(db.String(50))           # for students
    branch     = db.Column(db.String(50))          # for students
    year       = db.Column(db.Integer)              # for students
    college    = db.Column(db.String(150))
    interests  = db.Column(db.Text, default='')     # comma-separated tags
    avatar     = db.Column(db.String(5), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    registrations = db.relationship('Registration', backref='user', lazy=True)
    votes         = db.relationship('Vote',         backref='user', lazy=True)

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def to_dict(self):
        return {
            'id':        self.id,
            'name':      self.name,
            'email':     self.email,
            'role':      self.role,
            'degree':    self.degree,
            'branch':    self.branch,
            'year':      self.year,
            'college':   self.college,
            'interests': self.interests.split(',') if self.interests else [],
            'avatar':    self.avatar or self.name[:2].upper(),
        }