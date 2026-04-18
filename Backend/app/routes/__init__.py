from app.routes.auth      import auth_bp
from app.routes.events    import events_bp
from app.routes.student   import student_bp
from app.routes.organizer import organizer_bp
from app.routes.sponsor   import sponsor_bp

__all__ = ['auth_bp', 'events_bp', 'student_bp', 'organizer_bp', 'sponsor_bp']
