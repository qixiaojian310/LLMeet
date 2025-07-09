from .database_connector import get_connection, logger
from datetime import datetime
from typing import Optional, Tuple


def username_exists(username: str) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM user WHERE username = %s", (username,))
                return cursor.fetchone()[0] > 0
    except Exception as e:
        logger.error(f"username_exists error: {e}")
        return False


def email_exists(email: str) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM user WHERE email = %s", (email,))
                return cursor.fetchone()[0] > 0
    except Exception as e:
        logger.error(f"email_exists error: {e}")
        return False


def insert_user(username: str, email: str, hashed_password: str) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user (username, email, password, created_at)
                    VALUES (%s, %s, %s, %s)
                """, (username, email, hashed_password, datetime.utcnow()))
                conn.commit()
        return True
    except Exception as e:
        logger.error(f"insert_user error: {e}")
        return False


def get_user_by_username(username: str) -> Optional[Tuple[int, str, str]]:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT username, password FROM user WHERE username = %s",
                    (username,)
                )
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"get_user_by_username error: {e}")
        return None
