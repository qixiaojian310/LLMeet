import json
from typing import Any, Dict, List, Optional
from .database_connector import get_connection, logger

def insert_meeting_minute(
    meeting_id: str,
    username: str,  # 改为接收 username
    minute_record_path: str,
) -> bool:
    """
    更新 user_meeting 表中的会议记录路径。

    :param meeting_id: 会议 ID（room name）
    :param username: 用户名
    :param minute_record_path: 合并后生成的文件路径
    :return: 成功返回 True，失败返回 False
    """
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # 1. 根据 username 查询 user_id
                cursor.execute(
                    """
                    SELECT * FROM user 
                    WHERE username = %s
                    """,
                    (username,)
                )
                user = cursor.fetchone()
                
                if not user:
                    logger.error(f"[DB] 用户名不存在: {username}")
                    return False
                
                user_id = user['user_id']
                
                # 2. 检查用户是否有权限访问该会议
                cursor.execute(
                    """
                    SELECT 1 FROM user_meeting 
                    WHERE meeting_id = %s AND user_id = %s
                    """,
                    (meeting_id, user_id)
                )
                if not cursor.fetchone():
                    logger.error(f"[DB] 用户 {username}(id:{user_id}) 无权限访问会议 {meeting_id}")
                    return False
                
                # 3. 更新user_meeting表中的记录路径
                cursor.execute(
                    """
                    UPDATE user_meeting 
                    SET minutes_path = %s 
                    WHERE meeting_id = %s AND user_id = %s
                    """,
                    (minute_record_path, meeting_id, user_id)
                )
                
                conn.commit()
                logger.info(
                    f"[DB] 更新会议记录路径成功: "
                    f"meeting_id={meeting_id}, username={username}, user_id={user_id}, minute_record_path={minute_record_path}"
                )
                return True
                
    except Exception as e:
        logger.error(f"[DB] 更新会议记录路径失败: {e}")
        if conn:
            conn.rollback()
        return False
    

def fetch_meeting_minutes(meeting_id: str) -> List[Dict[str, Any]]:
    """
    根据 meeting_id 从 user_meeting 表中查询所有录制记录。
    返回列表，元素为字典：{'meeting_id': ..., 'username': ..., 'minute_record_path': ...}
    """
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = (
                    "SELECT um.meeting_id, u.username, um.minutes_path "
                    "FROM user_meeting um "
                    "JOIN user u ON um.user_id = u.user_id "
                    "WHERE um.meeting_id = %s"
                )
                cursor.execute(sql, (meeting_id,))
                rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error(f"fetch_meeting_minutes error: {e}")
        return []
    
def get_meeting_minutes(meeting_id: str) -> Optional[Dict[str, Any]]:
    """
    根据 meeting_id 从 meeting 表中查询合并后的会议纪要（JSON），
    并返回为 Python 对象（dict）。
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT minutes FROM meeting WHERE meeting_id = %s LIMIT 1",
                    (meeting_id,)
                )
                row = cursor.fetchone()
        if not row or not row[0]:
            return None
        # 数据库中存储的是 JSON 字符串，反序列化后返回 dict
        print(row[0])
        return json.loads(row[0])
    except Exception as e:
        logger.error(f"get_meeting_minutes error: {e}")
        return None