"""
Development seed script.

Creates:
  - The 7 canonical roles
  - One SUPER_ADMIN user (password from SEED_ADMIN_PASSWORD env var — never hard-coded)
  - A handful of sample clients and cities for local development

Run with:  python -m app.db.seed
"""

import os
import sys

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.city import City
from app.models.client import Client
from app.models.role import Role, RoleName
from app.models.user import User

SAMPLE_CLIENTS = [
    {"name": "Delhivery", "code": "DELHIVERY"},
    {"name": "Porter", "code": "PORTER"},
    {"name": "Zomato", "code": "ZOMATO"},
    {"name": "Flipkart", "code": "FLIPKART"},
]

SAMPLE_CITIES = [
    {"name": "Gurgaon", "state": "Haryana"},
    {"name": "Delhi", "state": "Delhi"},
    {"name": "Bangalore", "state": "Karnataka"},
    {"name": "Mumbai", "state": "Maharashtra"},
    {"name": "Hyderabad", "state": "Telangana"},
    {"name": "Pune", "state": "Maharashtra"},
]


def seed() -> None:
    admin_password = settings.SEED_ADMIN_PASSWORD or os.environ.get("SEED_ADMIN_PASSWORD")
    if not admin_password:
        print(
            "ERROR: SEED_ADMIN_PASSWORD is not set. "
            "Set it in your .env before running the seed script.",
            file=sys.stderr,
        )
        sys.exit(1)

    db = SessionLocal()
    try:
        # Roles
        roles_by_name = {}
        for role_name in RoleName.ALL:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=f"{role_name.replace('_', ' ').title()}")
                db.add(role)
                db.flush()
            roles_by_name[role_name] = role

        # Admin user
        admin = db.query(User).filter(User.email == settings.SEED_ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                name="System Admin",
                email=settings.SEED_ADMIN_EMAIL,
                password_hash=hash_password(admin_password),
                role_id=roles_by_name[RoleName.SUPER_ADMIN].id,
                is_active=True,
            )
            db.add(admin)
            print(f"Created admin user: {settings.SEED_ADMIN_EMAIL}")
        else:
            print(f"Admin user already exists: {settings.SEED_ADMIN_EMAIL}")

        # Sample clients
        for c in SAMPLE_CLIENTS:
            existing = db.query(Client).filter(Client.code == c["code"]).first()
            if not existing:
                db.add(Client(name=c["name"], code=c["code"], status="ACTIVE"))

        # Sample cities
        for c in SAMPLE_CITIES:
            existing = db.query(City).filter(City.name == c["name"]).first()
            if not existing:
                db.add(City(name=c["name"], state=c["state"], country="India", status="ACTIVE"))

        db.commit()
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
