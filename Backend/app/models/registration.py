from app import db
from datetime import datetime

class Registration(db.Model):
    __tablename__ = 'registrations'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),  nullable=False)
    event_id   = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status     = db.Column(db.String(20), default='confirmed')
    # status: 'confirmed' | 'waitlisted' | 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_id', name='unique_registration'),
    )

    def to_dict(self):
        return {
            'id':        self.id,
            'userId':    self.user_id,
            'eventId':   self.event_id,
            'status':    self.status,
            'createdAt': self.created_at.isoformat(),
        }