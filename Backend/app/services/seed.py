"""
Seed script - populates the database with baseline demo users on first run.
Safe to call multiple times (idempotent).
"""
from app import db
from app.models.user import User


def seed_db():
    # Only seed if DB is empty
    if User.query.first():
        return

    print("[SEED] Seeding database...")

    student = User(
        name="Arjun Sharma",
        email="student@college.edu",
        role="student",
        branch="CSE",
        year=3,
        college="VJTI Mumbai",
        interests="tech,hackathon,ai,music",
    )
    student.set_password("student123")

    organizer = User(
        name="CodeDecode Club",
        email="organizer@college.edu",
        role="organizer",
        college="VJTI Mumbai",
    )
    organizer.set_password("organizer123")

    sponsor_user = User(
        name="TechCorp India",
        email="sponsor@techcorp.in",
        role="sponsor",
        interests="hackathon,tech,coding",
    )
    sponsor_user.set_password("sponsor123")

    student2 = User(
        name="Priya Sharma",
        email="priya@college.edu",
        role="student",
        branch="IT",
        year=2,
        college="VJTI Mumbai",
        interests="cultural,music,dance",
    )
    student2.set_password("priya123")

    db.session.add_all([student, organizer, sponsor_user, student2])
    db.session.commit()

    print("[SEED] Database seeded successfully without organizer events.")
