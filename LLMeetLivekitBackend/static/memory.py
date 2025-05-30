from .database_connector import get_connection, logger


def get_all_unlearned_words(username: str, wordbook_id: int):
    unlearnd_words = []
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT user_id FROM users WHERE username = %s", (username,)
                )
                user_id = cursor.fetchone()["user_id"]
                cursor.execute(
                    """
                    SELECT word from words where word_id in
                    (SELECT wc.word_id
                    FROM wordbook_contents wc
                    LEFT JOIN user_words uw
                    ON wc.word_id = uw.word_id AND uw.user_id = %s
                    WHERE wc.wordbook_id = %s
                    AND uw.word_id IS NULL);
                    """,
                    (user_id, wordbook_id),
                )
                unlearnd_words: list = cursor.fetchall()
                return [unlearnd_word["word"] for unlearnd_word in unlearnd_words]
    except Exception as e:
        logger.debug(f"查询失败: {e}")
        return unlearnd_words
