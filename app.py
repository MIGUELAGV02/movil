from flask import Flask, jsonify

from config import Config
from controllers.authController import auth_bp
from controllers.productsController import products_bp
from controllers.usersController import users_bp
from extensions import cors, db, jwt, migrate
from seed import register_seed_commands


def create_app() -> Flask:
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	jwt.init_app(app)
	cors.init_app(app)
	migrate.init_app(app, db)

	# register CLI commands
	register_seed_commands(app)

	app.register_blueprint(auth_bp, url_prefix="/api/auth")
	app.register_blueprint(users_bp, url_prefix="/api/users")
	app.register_blueprint(products_bp, url_prefix="/api/products")

	@app.get("/")
	def index():
		return jsonify({"message": "Welcome to the Flask API!"})


	@app.get("/health")
	def health_check():
		return jsonify({"status": "ok"})

	return app




app = create_app()


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
