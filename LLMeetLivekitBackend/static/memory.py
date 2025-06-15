# meeting_minute_dao.py

from .database_connector import get_connection, logger

def insert_meeting_minute(
    meeting_id: str,
    minute_record_path: str,
    content: str = ""
) -> int:
    """
    向 meeting_minutes 表插入一条新记录。

    :param meeting_id:   会议 ID（room name）
    :param minute_record_path: 合并后生成的文件路径
    :param content:      会议纪要内容，默认为空
    :return:              新插入记录的 minutes_id，如果失败则返回 0
    """
    new_id = 0
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    INSERT INTO meeting_minutes
                      (meeting_id, content, created_at, minute_record_path)
                    VALUES (%s, %s, NOW(), %s)
                    """,
                    (meeting_id, content, minute_record_path),
                )
                conn.commit()
                new_id = cursor.lastrowid
                logger.info(f"[DB] 插入 meeting_minutes 成功，minutes_id={new_id}")
    except Exception as e:
        logger.error(f"[DB] 插入 meeting_minutes 失败: {e}")
    return new_id
