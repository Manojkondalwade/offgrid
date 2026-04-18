from app import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'

    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text, default='')
    category     = db.Column(db.String(50), default='general')
    emoji        = db.Column(db.String(5),  default='📅')
    date         = db.Column(db.String(50), default='TBD')
    time         = db.Column(db.String(20), default='TBD')
    venue        = db.Column(db.String(150), default='')
    capacity     = db.Column(db.Integer, default=100)
    status       = db.Column(db.String(20), default='draft')
    # status: 'draft' | 'published' | 'poll_active' | 'cancelled'
    tags         = db.Column(db.Text, default='')   # comma-separated
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    club_name    = db.Column(db.String(100), default='')
    sponsor_name = db.Column(db.String(100), default='')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')
    polls         = db.relationship('Poll',         backref='event', lazy=True, cascade='all, delete-orphan')
    proposals     = db.relationship('Proposal',     backref='event', lazy=True)

    @property
    def registered_count(self):
        return len(self.registrations)

    def to_dict(self, include_registrations=False):
        data = {
            'id':           self.id,
            'title':        self.title,
            'description':  self.description,
            'category':     self.category,
            'emoji':        self.emoji,
            'date':         self.date,
            'time':         self.time,
            'venue':        self.venue,
            'capacity':     self.capacity,
            'registered':   self.registered_count,
            'status':       self.status,
            'tags':         self.tags.split(',') if self.tags else [],
            'organizerId':  self.organizer_id,
            'clubName':     self.club_name,
            'sponsorName':  self.sponsor_name,
            'createdAt':    self.created_at.isoformat(),
        }
        return data