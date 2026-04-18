from app import db
from datetime import datetime

class Poll(db.Model):
    __tablename__ = 'polls'

    id         = db.Column(db.Integer, primary_key=True)
    event_id   = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    title      = db.Column(db.String(200), nullable=False)
    question   = db.Column(db.String(300), default='When should we host this event?')
    ends_at    = db.Column(db.String(50), default='')
    status     = db.Column(db.String(20), default='active')
    # status: 'active' | 'closed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    options    = db.relationship('PollOption', backref='poll', lazy=True, cascade='all, delete-orphan')

    @property
    def total_votes(self):
        return sum(o.votes for o in self.options)

    def to_dict(self):
        return {
            'id':         self.id,
            'eventId':    self.event_id,
            'title':      self.title,
            'question':   self.question,
            'endsAt':     self.ends_at,
            'status':     self.status,
            'totalVotes': self.total_votes,
            'options':    [o.to_dict() for o in self.options],
        }


class PollOption(db.Model):
    __tablename__ = 'poll_options'

    id      = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    label   = db.Column(db.String(200), nullable=False)
    votes   = db.Column(db.Integer, default=0)

    voter_ids = db.relationship('Vote', backref='option', lazy=True)

    def to_dict(self):
        return {
            'id':    self.id,
            'label': self.label,
            'votes': self.votes,
        }


class Vote(db.Model):
    __tablename__ = 'votes'

    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'),        nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('poll_options.id'), nullable=False)
    poll_id   = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'poll_id', name='unique_vote_per_poll'),
    )

    def to_dict(self):
        return {
            'userId':   self.user_id,
            'optionId': self.option_id,
            'pollId':   self.poll_id,
        }