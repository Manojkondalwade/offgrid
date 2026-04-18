from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.event    import Event
from app.models.proposal import Proposal

sponsor_bp = Blueprint('sponsor', __name__)


# ── GET events matching sponsor interests ────────────────────────────
@sponsor_bp.route('/discover', methods=['GET'])
@jwt_required()
def discover_events():
    user_id = int(get_jwt_identity())
    from app.models.user import User
    user = User.query.get_or_404(user_id)
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
        # Has sponsor already sent a proposal?
        existing = Proposal.query.filter_by(sponsor_id=user_id, event_id=e.id).first()
        d['proposalStatus'] = existing.status if existing else None
        result.append(d)

    return jsonify(result)


# ── GET sponsor's own proposals ──────────────────────────────────────
@sponsor_bp.route('/proposals', methods=['GET'])
@jwt_required()
def my_proposals():
    user_id   = int(get_jwt_identity())
    proposals = Proposal.query.filter_by(sponsor_id=user_id).all()
    return jsonify([p.to_dict() for p in proposals])


# ── POST send a proposal ─────────────────────────────────────────────
@sponsor_bp.route('/proposals', methods=['POST'])
@jwt_required()
def send_proposal():
    user_id  = int(get_jwt_identity())
    data     = request.get_json()
    event_id = data.get('eventId')

    if not event_id:
        return jsonify({'error': 'eventId is required'}), 400

    existing = Proposal.query.filter_by(sponsor_id=user_id, event_id=event_id).first()
    if existing:
        return jsonify({'error': 'Proposal already sent for this event'}), 409

    proposal = Proposal(
        sponsor_id = user_id,
        event_id   = event_id,
        amount     = data.get('amount', ''),
        perks      = data.get('perks', ''),
        message    = data.get('message', ''),
        status     = 'pending',
    )
    db.session.add(proposal)
    db.session.commit()
    return jsonify({'message': 'Proposal sent!', 'proposal': proposal.to_dict()}), 201


# ── DELETE withdraw a proposal ───────────────────────────────────────
@sponsor_bp.route('/proposals/<int:proposal_id>', methods=['DELETE'])
@jwt_required()
def withdraw_proposal(proposal_id):
    user_id  = int(get_jwt_identity())
    proposal = Proposal.query.get_or_404(proposal_id)

    if proposal.sponsor_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403

    db.session.delete(proposal)
    db.session.commit()
    return jsonify({'message': 'Proposal withdrawn'})


# ── GET sponsor dashboard summary ───────────────────────────────────
@sponsor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id   = int(get_jwt_identity())
    proposals = Proposal.query.filter_by(sponsor_id=user_id).all()

    total_invested = 0
    for p in proposals:
        if p.status == 'accepted':
            try:
                total_invested += int(''.join(filter(str.isdigit, p.amount)))
            except Exception:
                pass

    return jsonify({
        'totalProposals':  len(proposals),
        'pendingCount':    sum(1 for p in proposals if p.status == 'pending'),
        'acceptedCount':   sum(1 for p in proposals if p.status == 'accepted'),
        'totalInvested':   f'₹{total_invested:,}',
        'proposals':       [p.to_dict() for p in proposals],
    })