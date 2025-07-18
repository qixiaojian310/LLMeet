export interface Meeting {
  meeting_id: string;
  title: string;
  description: string;
  start_time: string; // ISO 格式时间字符串
  end_time: string; // ISO 格式时间字符串
  creator_id: string;
  created_at: string; // ISO 格式时间字符串
  status: 'ready' | 'ongoing' | 'ended' | string; // 可根据后端状态值扩展
  minutes: string | null; // 会议纪要路径或内容，如果为空则为 null
}
