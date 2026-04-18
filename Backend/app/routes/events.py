from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import db
from app.models.event        import Event
from app.models.vote         import Poll, PollOption
from app.models.registration import Registration
from app.models.review       import Review

events_bp = Blueprint('events', __name__)


def optional_identity():
    try:
        verify_jwt_in_request(optional=True)
        return get_jwt_identity()
    except Exception:
        return None


# ── GET all events (public) ──────────────────────────────────────────
@events_bp.route('/', methods=['GET'])
def get_events():
    category = request.args.get('category')
    status   = request.args.get('status', 'published')
    search   = request.args.get('q', '')

    query = Event.query
    if status != 'all':
        query = query.filter(Event.status.in_(['published', 'poll_active']))
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Event.title.ilike(f'%{search}%'))

    events = query.order_by(Event.created_at.desc()).all()
    return jsonify([e.to_dict() for e in events])


# ── GET single event ─────────────────────────────────────────────────
@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    data  = event.to_dict()

    # Include poll if active
    poll = Poll.query.filter_by(event_id=event_id, status='active').first()
    if poll:
        data['poll'] = poll.to_dict()

    # Include reviews
    data['reviews'] = [r.to_dict() for r in event.reviews] if hasattr(event, 'reviews') else []
    return jsonify(data)


# ── GET recommended events for current user ──────────────────────────
@events_bp.route('/recommended', methods=['GET'])
@jwt_required()
def get_recommended():
    from app.models.user import User
    user_id = int(get_jwt_identity())
    user    = User.query.get_or_404(user_id)
    interests = set(user.interests.split(',')) if user.interests else set()

    events = Event.query.filter(Event.status.in_(['published', 'poll_active'])).all()

    def score(e):
        tags = set(e.tags.split(',')) if e.tags else set()
        return len(tags & interests)

    ranked = sorted(events, key=score, reverse=True)
    result = []
    for e in ranked:
        d = e.to_dict()
        tags = set(e.tags.split(',')) if e.tags else set()
        d['matchScore'] = len(tags & interests)
        result.append(d)

    return jsonify(result)


# ── POST review for event ────────────────────────────────────────────
@events_bp.route('/<int:event_id>/reviews', methods=['POST'])
@jwt_required()
def post_review(event_id):
    user_id = int(get_jwt_identity())
    data    = request.get_json()

    existing = Review.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        return jsonify({'error': 'Already reviewed this event'}), 409

    review = Review(
        user_id  = user_id,
        event_id = event_id,
        rating   = data.get('rating', 5),
        comment  = data.get('comment', ''),
    )
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201


# ── GET reviews for event ────────────────────────────────────────────
@events_bp.route('/<int:event_id>/reviews', methods=['GET'])
def get_reviews(event_id):
    reviews = Review.query.filter_by(event_id=event_id).all()
    return jsonify([r.to_dict() for r in reviews])