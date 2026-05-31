from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from extensions import db
from models.userModel import User
from utils.roles import roles_required


users_bp = Blueprint("users", __name__)


@users_bp.get("")
@jwt_required()
@roles_required(["admin"])
def list_users():
	users = User.query.order_by(User.id.asc()).all()
	return jsonify({"items": [user.to_dict() for user in users]})


@users_bp.get("/<int:user_id>")
@jwt_required()
@roles_required(["admin"])
def get_user(user_id: int):
	user = User.query.get_or_404(user_id)
	return jsonify({"user": user.to_dict()})


@users_bp.patch("/<int:user_id>")
@jwt_required()
@roles_required(["admin"])
def update_user(user_id: int):
	user = User.query.get_or_404(user_id)
	payload = request.get_json(silent=True) or {}

	username = payload.get("username")
	email = payload.get("email")
	password = payload.get("password")
	is_active = payload.get("is_active")

	if username is not None:
		username = username.strip()
		if not username:
			return jsonify({"message": "username cannot be empty"}), 400
		exists = User.query.filter(User.username == username, User.id != user.id).first()
		if exists:
			return jsonify({"message": "username already exists"}), 409
		user.username = username

	if email is not None:
		email = email.strip().lower()
		if not email:
			return jsonify({"message": "email cannot be empty"}), 400
		exists = User.query.filter(User.email == email, User.id != user.id).first()
		if exists:
			return jsonify({"message": "email already exists"}), 409
		user.email = email

	if password:
		user.set_password(password)

	if is_active is not None:
		user.is_active = bool(is_active)

	db.session.commit()

	return jsonify({"message": "user updated", "user": user.to_dict()})


@users_bp.delete("/<int:user_id>")
@jwt_required()
@roles_required(["admin"])
def delete_user(user_id: int):
	user = User.query.get_or_404(user_id)

	db.session.delete(user)
	db.session.commit()

	return jsonify({"message": "user deleted"})
