from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
	create_access_token,
	get_jwt,
	get_jwt_identity,
	jwt_required,
	verify_jwt_in_request,
)

from extensions import db
from models.userModel import User


auth_bp = Blueprint("auth", __name__)


def build_token(user: User) -> str:
	return create_access_token(
		identity=str(user.id),
		additional_claims={
			"username": user.username,
			"email": user.email,
			"role": user.role,
		},
	)


@auth_bp.post("/register")
def register():
	payload = request.get_json(silent=True) or {}
	username = (payload.get("username") or "").strip()
	email = (payload.get("email") or "").strip().lower()
	password = payload.get("password") or ""
	role = (payload.get("role") or "user").strip().lower()

	if not username or not email or not password:
		return jsonify({"message": "username, email and password are required"}), 400

	# Only an existing admin may create another admin
	if role == "admin":
		try:
			verify_jwt_in_request()
			current = get_jwt()
			if current.get("role") != "admin":
				return jsonify({"message": "only admin can create admin users"}), 403
		except Exception:
			return jsonify({"message": "admin credentials required to create admin"}), 403

	if User.query.filter((User.username == username) | (User.email == email)).first():
		return jsonify({"message": "username or email already exists"}), 409

	user = User(username=username, email=email, role=role)
	user.set_password(password)

	db.session.add(user)
	db.session.commit()

	token = build_token(user)

	return jsonify({"message": "user created", "user": user.to_dict(), "access_token": token}), 201


@auth_bp.post("/login")
def login():
	payload = request.get_json(silent=True) or {}
	email = (payload.get("email") or "").strip().lower()
	password = payload.get("password") or ""

	if not email or not password:
		return jsonify({"message": "email and password are required"}), 400

	user = User.query.filter_by(email=email).first()
	if user is None or not user.check_password(password):
		return jsonify({"message": "invalid credentials"}), 401

	if not user.is_active:
		return jsonify({"message": "user inactive"}), 403

	token = build_token(user)

	return jsonify({"message": "login successful", "user": user.to_dict(), "access_token": token})


@auth_bp.get("/me")
@jwt_required()
def me():
	identity = get_jwt_identity()
	user = User.query.get(int(identity))

	if user is None:
		return jsonify({"message": "user not found"}), 404

	return jsonify({"user": user.to_dict(), "identity": identity, "claims": get_jwt()})
