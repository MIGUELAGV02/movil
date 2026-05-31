from __future__ import annotations

import os
from typing import Optional

from flask import current_app


def register_seed_commands(app):
    @app.cli.group()
    def seed():
        """Seed database commands"""

    @seed.command("run")
    def run():
        """Run seeders to populate initial data"""
        from extensions import db
        from models.userModel import User
        from models.productMode import Product
        import click

        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "adminpass")

        def ensure_admin():
            existing = User.query.filter_by(email=admin_email).first()
            if existing:
                click.echo(f"Admin already exists: {admin_email}")
                return existing

            admin = User(username="admin", email=admin_email, role="admin")
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            click.echo(f"Created admin: {admin_email}")
            return admin

        def ensure_sample_user():
            email = os.getenv("SAMPLE_USER_EMAIL", "user@example.com")
            pwd = os.getenv("SAMPLE_USER_PASSWORD", "userpass")
            if User.query.filter_by(email=email).first():
                click.echo(f"Sample user already exists: {email}")
                return
            u = User(username="sampleuser", email=email, role="user")
            u.set_password(pwd)
            db.session.add(u)
            db.session.commit()
            click.echo(f"Created sample user: {email}")

        def ensure_products():
            samples = [
                {"name": "Sample Product 1", "description": "Seeded product 1", "price": 9.99, "stock": 10},
                {"name": "Sample Product 2", "description": "Seeded product 2", "price": 19.99, "stock": 5},
            ]
            created = 0
            for s in samples:
                if not Product.query.filter_by(name=s["name"]).first():
                    p = Product(name=s["name"], description=s["description"], price=s["price"], stock=s["stock"], is_active=True)
                    db.session.add(p)
                    created += 1
            if created:
                db.session.commit()
            click.echo(f"Ensured {len(samples)} sample products (created: {created})")

        # Run in app context
        with app.app_context():
            ensure_admin()
            ensure_sample_user()
            ensure_products()
            click.echo("Seeding complete")
