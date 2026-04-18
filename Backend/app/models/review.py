from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'),   nullable=False)
    event_id   = db.Column(db.Integer, db.ForeignKey('events.id'),  nullable=False)
    rating     = db.Column(db.Integer, nullable=False)   # 1-5
    comment    = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_id', name='unique_review'),
    )

    user  = db.relationship('User',  foreign_keys=[user_id])
    event = db.relationship('Event', foreign_keys=[event_id])

    def to_dict(self):
        return {
            'id':        self.id,
            'userId':    self.user_id,
            'userName':  self.user.name if self.user else '',
            'eventId':   self.event_id,
            'rating':    self.rating,
            'comment':   self.comment,
            'createdAt': self.created_at.isoformat(),
        }