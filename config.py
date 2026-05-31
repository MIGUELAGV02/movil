from __future__ import annotations

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()


def build_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url:
        return database_url

    host = os.getenv("DATABASE_HOST", "").strip()
    name = os.getenv("DATABASE_NAME", "").strip()
    if not host or not name:
        host = os.getenv("DATABASE_HOST", "localhost").strip()
        name = os.getenv("DATABASE_NAME", "moviluno").strip()

    engine = os.getenv("DATABASE_ENGINE", "mysql+pymysql")
    port = os.getenv("DATABASE_PORT", "3306")
    user = os.getenv("DATABASE_USER", "root")
    password = quote_plus(os.getenv("DATABASE_PASSWORD", ""))

    return f"{engine}://{user}:{password}@{host}:{port}/{name}"


def build_engine_options(database_uri: str) -> dict:
    ssl_ca_path = os.getenv("DATABASE_SSL_CA_PATH", "").strip()
    connect_args = {}
    if ssl_ca_path:
        connect_args["ssl"] = {"ca": ssl_ca_path}

    return {
        "pool_pre_ping": True,
        "pool_recycle": int(os.getenv("DATABASE_POOL_RECYCLE", "280")),
        "connect_args": connect_args,
    }


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_HEADER_TYPE = "Bearer"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "0") == "1"
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_ENGINE_OPTIONS = build_engine_options(SQLALCHEMY_DATABASE_URI)
