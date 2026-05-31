from __future__ import annotations

from datetime import datetime, timezone

from extensions import db


class Product(db.Model):
	__tablename__ = "products"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False, index=True)
	description = db.Column(db.Text, nullable=True)
	price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
	stock = db.Column(db.Integer, nullable=False, default=0)
	is_active = db.Column(db.Boolean, nullable=False, default=True)
	created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
	updated_at = db.Column(
		db.DateTime,
		nullable=False,
		default=lambda: datetime.now(timezone.utc),
		onupdate=lambda: datetime.now(timezone.utc),
	)

	def to_dict(self) -> dict:
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"price": float(self.price) if self.price is not None else 0.0,
			"stock": self.stock,
			"is_active": self.is_active,
			"created_at": self.created_at.isoformat() if self.created_at else None,
			"updated_at": self.updated_at.isoformat() if self.updated_at else None,
		}
