import sqlite3
from flask import Blueprint, g


db_bp = Blueprint("db_bp", __name__)

DATABASE = "database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        conn = g._database = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
    return conn


@db_bp.teardown_app_request
def close_connection(exception):
    conn = getattr(g, "_database", None)
    if conn is not None:
        conn.close()


# テスト用に初回リクエスト時にテーブルを作成
@db_bp.before_app_request
def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            nickname TEXT
        )
    """)
    conn.commit()
    conn.close()
