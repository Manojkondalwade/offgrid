from app import db
from datetime import datetime

class Proposal(db.Model):
    __tablename__ = 'proposals'

    id           = db.Column(db.Integer, primary_key=True)
    sponsor_id   = db.Column(db.Integer, db.ForeignKey('users.id'),   nullable=False)
    event_id     = db.Column(db.Integer, db.ForeignKey('events.id'),  nullable=False)
    amount       = db.Column(db.String(30), default='')
    perks        = db.Column(db.Text, default='')
    message      = db.Column(db.Text, default='')
    status       = db.Column(db.String(20), default='pending')
    # status: 'pending' | 'accepted' | 'rejected' | 'discussing'
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    sponsor  = db.relationship('User',  foreign_keys=[sponsor_id])

    def to_dict(self):
        return {
            'id':          self.id,
            'sponsorId':   self.sponsor_id,
            'sponsorName': self.sponsor.name if self.sponsor else '',
            'eventId':     self.event_id,
            'eventTitle':  self.event.title if self.event else '',
            'amount':      self.amount,
            'perks':       self.perks,
            'message':     self.message,
            'status':      self.status,
            'createdAt':   self.created_at.isoformat(),
        }