import sqlite3
from flask import Blueprint, g


db_bp = Blueprint("db_bp", __name__)

DATABASE = "database.db"


# リクエストごとにDBコネクション
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@db_bp.teardown_app_request
def close_connection(exception):
    conn = getattr(g, "_database", None)
    if conn is not None:
        conn.close()


# テスト用に初回リクエスト時にテーブルを作成
@db_bp.before_app_request
def init_db():
    conn = get_db()
    # テーブル作成
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            nickname TEXT
        )
    """)

    # userがいない場合、テストユーザーを作成
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        conn.execute("INSERT INTO user (name, age) VALUES (?, ?)", ("test", 20))
        conn.execute(
            "INSERT INTO user (name, age, nickname) VALUES (?, ?, ?)",
            ("test2", 22, "2"),
        )
        conn.commit()
