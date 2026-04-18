"""
Recommendation engine — ranks events for a user based on interest overlap.
"""
from app.models.event        import Event
from app.models.registration import Registration


def get_recommendations(user):
    """Return events ranked by interest match for the given user."""
    user_interests = set(user.interests.split(',')) if user.interests else set()
    registered_ids = {r.event_id for r in Registration.query.filter_by(user_id=user.id).all()}

    events = Event.query.filter(
        Event.status.in_(['published', 'poll_active'])
    ).all()

    result = []
    for event in events:
        tags  = set(event.tags.split(',')) if event.tags else set()
        score = len(tags & user_interests)
        result.append({
            **event.to_dict(),
            'matchScore':    score,
            'isRegistered':  event.id in registered_ids,
        })

    # Sort: by match score desc, then by registration desc
    result.sort(key=lambda e: (e['matchScore'], e['registered']), reverse=True)
    return result


def get_trending_events(limit=5):
    """Return top events by registration count."""
    events = Event.query.filter(
        Event.status.in_(['published', 'poll_active'])
    ).all()
    events.sort(key=lambda e: e.registered_count, reverse=True)
    return [e.to_dict() for e in events[:limit]]
