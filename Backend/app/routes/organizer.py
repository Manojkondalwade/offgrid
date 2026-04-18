from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.event    import Event
from app.models.vote     import Poll, PollOption
from app.models.proposal import Proposal

organizer_bp = Blueprint('organizer', __name__)


def require_organizer(user_id):
    from app.models.user import User
    user = User.query.get_or_404(user_id)
    if user.role != 'organizer':
        return None, jsonify({'error': 'Organizer access required'}), 403
    return user, None, None


# ── GET organizer dashboard ──────────────────────────────────────────
@organizer_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = int(get_jwt_identity())
    events  = Event.query.filter_by(organizer_id=user_id).all()
    total_regs = sum(e.registered_count for e in events)
    active_polls = Poll.query.join(Event).filter(
        Event.organizer_id == user_id, Poll.status == 'active'
    ).count()
    pending_proposals = Proposal.query.join(Event).filter(
        Event.organizer_id == user_id, Proposal.status == 'pending'
    ).count()

    return jsonify({
        'totalEvents':       len(events),
        'totalRegistrations': total_regs,
        'activePolls':       active_polls,
        'pendingProposals':  pending_proposals,
        'events':            [e.to_dict() for e in events],
    })


# ── GET organizer's events ───────────────────────────────────────────
@organizer_bp.route('/events', methods=['GET'])
@jwt_required()
def my_events():
    user_id = int(get_jwt_identity())
    events  = Event.query.filter_by(organizer_id=user_id).order_by(Event.created_at.desc()).all()
    return jsonify([e.to_dict() for e in events])


# ── POST create event ────────────────────────────────────────────────
@organizer_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    user_id = int(get_jwt_identity())
    data    = request.get_json()

    if not data.get('title'):
        return jsonify({'error': 'title is required'}), 400

    capacity = data.get('capacity', 100)
    if capacity is not None and int(capacity) < 1:
        return jsonify({'error': 'Max participants must be at least 1'}), 400

    event = Event(
        title        = data['title'],
        description  = data.get('description', ''),
        category     = data.get('category', 'general'),
        emoji        = data.get('emoji', '📅'),
        date         = data.get('date', 'TBD'),
        time         = data.get('time', 'TBD'),
        venue        = data.get('venue', ''),
        capacity     = max(1, int(capacity)) if capacity is not None else 100,
        status       = data.get('status', 'draft'),
        tags         = ','.join(data.get('tags', [])),
        organizer_id = user_id,
        club_name    = data.get('clubName', ''),
    )
    db.session.add(event)
    db.session.commit()

    # If poll requested, create it
    if data.get('pollOptions'):
        poll = Poll(
            event_id = event.id,
            title    = f'{event.title} — Best Timing?',
            question = 'When should we host this event?',
            ends_at  = data.get('pollEndsAt', ''),
            status   = 'active',
        )
        db.session.add(poll)
        db.session.flush()
        for label in data['pollOptions']:
            db.session.add(PollOption(poll_id=poll.id, label=label))
        event.status = 'poll_active'

    db.session.commit()
    return jsonify(event.to_dict()), 201


# ── PUT update event ─────────────────────────────────────────────────
@organizer_bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    user_id = int(get_jwt_identity())
    event   = Event.query.get_or_404(event_id)

    if event.organizer_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json()
    new_capacity = data.get('capacity', event.capacity)
    if new_capacity is not None and int(new_capacity) < 1:
        return jsonify({'error': 'Max participants must be at least 1'}), 400

    event.title       = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.category    = data.get('category', event.category)
    event.emoji       = data.get('emoji', event.emoji)
    event.date        = data.get('date', event.date)
    event.time        = data.get('time', event.time)
    event.venue       = data.get('venue', event.venue)
    event.capacity    = max(1, int(new_capacity)) if new_capacity is not None else event.capacity
    event.status      = data.get('status', event.status)
    event.tags        = ','.join(data.get('tags', event.tags.split(',') if event.tags else []))
    event.club_name   = data.get('clubName', event.club_name)

    db.session.commit()
    return jsonify(event.to_dict())


# ── DELETE event ─────────────────────────────────────────────────────
@organizer_bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    user_id = int(get_jwt_identity())
    event   = Event.query.get_or_404(event_id)

    if event.organizer_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'})


# ── GET proposals for organizer's events ────────────────────────────
@organizer_bp.route('/proposals', methods=['GET'])
@jwt_required()
def my_proposals():
    user_id = int(get_jwt_identity())
    proposals = Proposal.query.join(Event).filter(Event.organizer_id == user_id).all()
    return jsonify([p.to_dict() for p in proposals])


# ── PUT respond to proposal ──────────────────────────────────────────
@organizer_bp.route('/proposals/<int:proposal_id>', methods=['PUT'])
@jwt_required()
def respond_proposal(proposal_id):
    user_id  = int(get_jwt_identity())
    proposal = Proposal.query.get_or_404(proposal_id)

    if proposal.event.organizer_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    data     = request.get_json()
    proposal.status = data.get('status', proposal.status)
    db.session.commit()
    return jsonify(proposal.to_dict())


# ── GET analytics for organizer ──────────────────────────────────────
@organizer_bp.route('/analytics', methods=['GET'])
@jwt_required()
def analytics():
    user_id = int(get_jwt_identity())
    events  = Event.query.filter_by(organizer_id=user_id).all()

    top_events = sorted(events, key=lambda e: e.registered_count, reverse=True)[:5]

    return jsonify({
        'totalRegistrations': sum(e.registered_count for e in events),
        'totalEvents':        len(events),
        'topEvents': [
            {'title': e.title, 'registrations': e.registered_count}
            for e in top_events
        ],
    })