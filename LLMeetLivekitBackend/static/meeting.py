from datetime import datetime
import json
from typing import Any, Dict, List, Optional
from .database_connector import get_connection, logger

def add_meeting(meeting) -> int:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = '''
                    INSERT INTO meeting (meeting_id, title, description, creator_id, created_at, status, start_time, end_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cur.execute(sql, (
                    meeting.meeting_id,
                    meeting.title,
                    meeting.description,
                    meeting.creator_id,
                    meeting.created_at,
                    meeting.status,
                    meeting.start_time,
                    meeting.end_time
                ))
            conn.commit()
        return 1
    except Exception as e:
        logger.error(f"add_meeting error: {e}")
        return 0


def add_user_to_meeting(username: str, meeting_id: str, joined_at: datetime) -> int:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO user_meeting (username, meeting_id, joined_at) VALUES (%s, %s, %s)",
                    (username, meeting_id, joined_at)
                )
            conn.commit()
        return 1
    except Exception as e:
        logger.error(f"add_user_to_meeting error: {e}")
        return 0


def delete_meeting(meeting_id: str) -> int:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM meeting WHERE meeting_id = %s", (meeting_id,))
            conn.commit()
        return 1
    except Exception as e:
        logger.error(f"delete_meeting error: {e}")
        return 0


def find_meeting_by_id(meeting_id: str) -> Optional[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM meeting WHERE meeting_id = %s", (meeting_id,))
                row = cur.fetchone()
                if not row:
                    return None
                keys = [desc[0] for desc in cur.description]
                return dict(zip(keys, row))
    except Exception as e:
        logger.error(f"find_meeting_by_id error: {e}")
        return None


def find_meetings_by_username(username: str) -> List[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT m.* FROM meeting m
                    JOIN user_meeting um ON m.meeting_id = um.meeting_id
                    WHERE um.username = %s
                ''', (username,))
                rows = cur.fetchall()
                keys = [desc[0] for desc in cur.description]
                return [dict(zip(keys, row)) for row in rows]
    except Exception as e:
        logger.error(f"find_meetings_by_username error: {e}")   
        return []

def find_recorded_meetings_by_username(username: str) -> List[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT DISTINCT m.*
                    FROM meeting m
                    JOIN user_meeting um ON m.meeting_id = um.meeting_id
                    JOIN records r ON r.user_meeting_id = um.user_meeting_id
                    WHERE um.username = %s
                ''', (username,))
                rows = cur.fetchall()
                keys = [desc[0] for desc in cur.description]
                return [dict(zip(keys, row)) for row in rows]
    except Exception as e:
        logger.error(f"find_recorded_meetings_by_username error: {e}")
        return []


def insert_meeting_record(
    meeting_id: str,
    username: str,
    minute_record_path: str,
) -> bool:
    """
    向 records 表插入一条新的会议录制记录，基于 user_meeting 的关联。

    :param meeting_id: 会议 ID
    :param username: 用户名
    :param minute_record_path: 合并后生成的文件路径
    :return: 成功返回 True，失败返回 False
    """
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # 查找 user_meeting_id
                cursor.execute(
                    """
                    SELECT user_meeting_id FROM user_meeting
                    WHERE meeting_id = %s AND username = %s
                    """,
                    (meeting_id, username)
                )
                result = cursor.fetchone()
                if not result:
                    logger.error(f"[DB] 用户 {username} 无权限或未加入会议 {meeting_id}")
                    return False

                user_meeting_id = result['user_meeting_id']

                # 插入新的录制记录
                cursor.execute(
                    """
                    INSERT INTO records (user_meeting_id, minutes_path)
                    VALUES (%s, %s)
                    """,
                    (user_meeting_id, minute_record_path)
                )

                conn.commit()
                logger.info(
                    f"[DB] 插入会议录制成功: meeting_id={meeting_id}, username={username}, path={minute_record_path}"
                )
                return True

    except Exception as e:
        logger.error(f"[DB] 插入会议录制失败: {e}")
        if conn:
            conn.rollback()
        return False


def fetch_meeting_records(meeting_id: str) -> List[Dict[str, Any]]:
    """
    根据 meeting_id 查询与该会议关联的所有录制记录（记录文件路径和用户名）。
    """
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT
                        um.meeting_id,
                        u.username,
                        r.minutes_path
                    FROM
                        records r
                    JOIN user_meeting um ON r.user_meeting_id = um.user_meeting_id
                    JOIN user u ON um.username = u.username
                    WHERE
                        um.meeting_id = %s
                """
                cursor.execute(sql, (meeting_id,))
                rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error(f"fetch_meeting_records error: {e}")
        return []
    
def insert_meeting_minutes(meeting_id: str, segments: Dict[str, Any], language: str = "en", video_summarization: str = "") -> bool:
    """
    插入或更新会议纪要到 minutes 表，包含 segments 和 language 字段。
    """
    try:
        minutes_json = json.dumps(segments, ensure_ascii=False)

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO minutes (meeting_id, segments, language, video_summarization)
                    VALUES (%s, %s, %s, %s) AS new
                    ON DUPLICATE KEY UPDATE 
                        segments = new.segments,
                        language = new.language,
                        video_summarization = new.video_summarization
                """, (meeting_id, minutes_json, language, video_summarization))
                conn.commit()
        return True
    except Exception as e:
        logger.error(f"insert_meeting_minutes error: {e}")
        return False

def get_meeting_minutes(meeting_id: str) -> Optional[Dict[str, Any]]:
    """
    查询会议纪要，返回一个包含 segments、created_at、language, video_summarization 的字典。
    """
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT segments, created_at, language, video_summarization
                    FROM minutes
                    WHERE meeting_id = %s
                    LIMIT 1
                """, (meeting_id,))
                row = cursor.fetchone()
        if not row or not row["segments"]:
            return None
        return {
            "segments": json.loads(row["segments"]),
            "created_at": row["created_at"],
            "language": row["language"],
            "video_summarization": row["video_summarization"]
        }
    except Exception as e:
        logger.error(f"get_meeting_minutes error: {e}")
        return None