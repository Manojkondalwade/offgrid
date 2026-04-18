from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.event        import Event
from app.models.registration import Registration
from app.models.vote         import Poll, PollOption, Vote
from app.models.review       import Review

student_bp = Blueprint('student', __name__)


def require_student(user_id):
    from app.models.user import User
    user = User.query.get_or_404(user_id)
    if user.role not in ('student',):
        return None
    return user


# ── GET student dashboard summary ───────────────────────────────────
@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = int(get_jwt_identity())
    from app.models.user import User
    user = User.query.get_or_404(user_id)

    registrations = Registration.query.filter_by(user_id=user_id).all()
    voted_polls   = Vote.query.filter_by(user_id=user_id).count()
    active_polls  = Poll.query.filter_by(status='active').count()

    return jsonify({
        'user':            user.to_dict(),
        'registeredCount': len(registrations),
        'pollsVoted':      voted_polls,
        'activePolls':     active_polls,
    })


# ── GET my registered events ─────────────────────────────────────────
@student_bp.route('/registrations', methods=['GET'])
@jwt_required()
def my_registrations():
    user_id = int(get_jwt_identity())
    regs    = Registration.query.filter_by(user_id=user_id).all()
    result  = []
    for r in regs:
        d = r.to_dict()
        d['event'] = r.event.to_dict() if r.event else {}
        # Check if user already reviewed this event
        existing_review = Review.query.filter_by(user_id=user_id, event_id=r.event_id).first()
        d['isReviewed'] = existing_review is not None
        d['myReview'] = existing_review.to_dict() if existing_review else None
        result.append(d)
    return jsonify(result)


# ── POST register for event ──────────────────────────────────────────
@student_bp.route('/registrations', methods=['POST'])
@jwt_required()
def register_event():
    user_id  = int(get_jwt_identity())
    data     = request.get_json()
    event_id = data.get('eventId')

    if not event_id:
        return jsonify({'error': 'eventId is required'}), 400

    event = Event.query.get_or_404(event_id)
    if event.status not in ('published', 'poll_active'):
        return jsonify({'error': 'Event is not open for registration'}), 400

    if event.registered_count >= event.capacity:
        return jsonify({'error': 'Event is full'}), 400

    existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        return jsonify({'error': 'Already registered for this event'}), 409

    reg = Registration(user_id=user_id, event_id=event_id)
    db.session.add(reg)
    db.session.commit()
    return jsonify({'message': 'Registered successfully!', 'registration': reg.to_dict()}), 201


# ── DELETE cancel registration ───────────────────────────────────────
@student_bp.route('/registrations/<int:event_id>', methods=['DELETE'])
@jwt_required()
def cancel_registration(event_id):
    user_id = int(get_jwt_identity())
    reg = Registration.query.filter_by(user_id=user_id, event_id=event_id).first_or_404()
    db.session.delete(reg)
    db.session.commit()
    return jsonify({'message': 'Registration cancelled'})


# ── GET all active polls ─────────────────────────────────────────────
@student_bp.route('/polls', methods=['GET'])
@jwt_required()
def get_polls():
    user_id = int(get_jwt_identity())
    polls   = Poll.query.filter_by(status='active').all()
    result  = []
    for p in polls:
        d = p.to_dict()
        # has user voted?
        my_vote = Vote.query.filter_by(user_id=user_id, poll_id=p.id).first()
        d['myVoteOptionId'] = my_vote.option_id if my_vote else None
        result.append(d)
    return jsonify(result)


# ── POST vote on poll option ─────────────────────────────────────────
@student_bp.route('/polls/<int:poll_id>/vote', methods=['POST'])
@jwt_required()
def cast_vote(poll_id):
    user_id   = int(get_jwt_identity())
    data      = request.get_json()
    option_id = data.get('optionId')

    poll = Poll.query.get_or_404(poll_id)
    if poll.status != 'active':
        return jsonify({'error': 'Poll is closed'}), 400

    if poll.ends_at:
        try:
            from datetime import datetime
            ends_dt = datetime.fromisoformat(poll.ends_at)
            if datetime.now() > ends_dt:
                return jsonify({'error': 'Poll deadline has passed'}), 400
        except ValueError:
            pass

    existing = Vote.query.filter_by(user_id=user_id, poll_id=poll_id).first()
    if existing:
        return jsonify({'error': 'Already voted in this poll'}), 409

    option = PollOption.query.get_or_404(option_id)
    option.votes += 1

    vote = Vote(user_id=user_id, option_id=option_id, poll_id=poll_id)
    db.session.add(vote)
    db.session.commit()

    return jsonify({'message': 'Vote recorded!', 'poll': poll.to_dict()}), 201


# ── POST submit event review ─────────────────────────────────────────
@student_bp.route('/events/<int:event_id>/reviews', methods=['POST'])
@jwt_required()
def submit_review(event_id):
    user_id = int(get_jwt_identity())
    data    = request.get_json()
    rating  = data.get('rating')
    comment = data.get('comment', '')

    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({'error': 'A rating between 1 and 5 is required'}), 400

    # Ensure user was registered for this event
    reg = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if not reg:
        return jsonify({'error': 'You must be registered for this event to leave a review'}), 403

    event = Event.query.get_or_404(event_id)
    if event.status != 'completed':
        return jsonify({'error': 'Reviews can only be submitted for completed events'}), 400

    # Check for existing review
    existing = Review.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing:
        return jsonify({'error': 'You have already reviewed this event'}), 409

    review = Review(
        user_id=user_id,
        event_id=event_id,
        rating=int(rating),
        comment=comment
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review submitted successfully!', 'review': review.to_dict()}), 201