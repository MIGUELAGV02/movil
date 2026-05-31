from __future__ import annotations

from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from utils.roles import roles_required

from extensions import db
from models.productMode import Product


products_bp = Blueprint("products", __name__)


def parse_price(value):
	if value is None:
		return None

	try:
		return Decimal(str(value))
	except (InvalidOperation, TypeError, ValueError):
		return None


@products_bp.get("")
@jwt_required()
@roles_required(["admin", "user"])
def list_products():
	products = Product.query.order_by(Product.id.asc()).all()
	return jsonify({"items": [product.to_dict() for product in products]})


@products_bp.get("/<int:product_id>")
@jwt_required()
@roles_required(["admin", "user"])
def get_product(product_id: int):
	product = Product.query.get_or_404(product_id)
	return jsonify({"product": product.to_dict()})


@products_bp.post("")
@jwt_required()
@roles_required(["admin", "user"])
def create_product():
	payload = request.get_json(silent=True) or {}
	name = (payload.get("name") or "").strip()
	description = payload.get("description")
	price = parse_price(payload.get("price"))
	stock = payload.get("stock", 0)
	is_active = payload.get("is_active", True)

	if not name:
		return jsonify({"message": "name is required"}), 400

	if price is None:
		return jsonify({"message": "price must be a valid number"}), 400

	try:
		stock = int(stock)
	except (TypeError, ValueError):
		return jsonify({"message": "stock must be an integer"}), 400

	product = Product(
		name=name,
		description=description,
		price=price,
		stock=stock,
		is_active=bool(is_active),
	)

	db.session.add(product)
	db.session.commit()

	return jsonify({"message": "product created", "product": product.to_dict()}), 201


@products_bp.patch("/<int:product_id>")
@jwt_required()
@roles_required(["admin", "user"])
def update_product(product_id: int):
	product = Product.query.get_or_404(product_id)
	payload = request.get_json(silent=True) or {}

	name = payload.get("name")
	description = payload.get("description")
	price = payload.get("price")
	stock = payload.get("stock")
	is_active = payload.get("is_active")

	if name is not None:
		name = name.strip()
		if not name:
			return jsonify({"message": "name cannot be empty"}), 400
		product.name = name

	if description is not None:
		product.description = description

	if price is not None:
		parsed_price = parse_price(price)
		if parsed_price is None:
			return jsonify({"message": "price must be a valid number"}), 400
		product.price = parsed_price

	if stock is not None:
		try:
			product.stock = int(stock)
		except (TypeError, ValueError):
			return jsonify({"message": "stock must be an integer"}), 400

	if is_active is not None:
		product.is_active = bool(is_active)

	db.session.commit()

	return jsonify({"message": "product updated", "product": product.to_dict()})


@products_bp.delete("/<int:product_id>")
@jwt_required()
@roles_required(["admin", "user"])
def delete_product(product_id: int):
	product = Product.query.get_or_404(product_id)

	db.session.delete(product)
	db.session.commit()

	return jsonify({"message": "product deleted"})