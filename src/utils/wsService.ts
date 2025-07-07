// src/services/wsService.ts

/**
 * 接口定义：后端 "merge_complete" 事件的结构
 */
export interface MergeCompleteEvent {
  event: 'merge_complete';
  payload: {
    mergedUrl: string;
    timestamp: string;
    [key: string]: any;
  };
}

type AnyEvent = MergeCompleteEvent;

type MessageHandler = (event: MergeCompleteEvent) => void;

/**
 * WebSocket 单例服务
 */
class WsService {
  private socket?: WebSocket;
  private handlers = new Set<MessageHandler>();

  /**
   * 初始化 WebSocket 连接（只会执行一次）
   */
  public init(): void {
    if (this.socket) return;
    this.socket = new WebSocket(`${import.meta.env.VITE_RECORD_WS_URL}/meeting/ws/recordings`);
    this.socket.addEventListener('open', () => console.log('[WS] connected'));
    this.socket.addEventListener('message', this._onMessage);
    this.socket.addEventListener('close', () => console.log('[WS] closed'));
    this.socket.addEventListener('error', e => console.error('[WS] error', e));
  }

  /**
   * 内部消息处理：解析 JSON 并分发给注册的回调
   */
  private _onMessage = (evt: MessageEvent): void => {
    let data: AnyEvent;
    try {
      data = JSON.parse(evt.data);
    } catch (err) {
      console.warn('[WS] invalid JSON', evt.data);
      return;
    }

    if (data.event === 'merge_complete') {
      this.handlers.forEach(h => h(data));
    }
    // 若有其它事件类型，可在此扩展处理
  };

  /**
   * 订阅 "merge_complete" 事件
   * @param fn 回调函数，当事件触发时调用
   */
  public subscribeMergeComplete(fn: MessageHandler): void {
    this.handlers.add(fn);
  }

  /**
   * 取消订阅 "merge_complete" 事件
   * @param fn 回调函数引用，用于移除
   */
  public unsubscribeMergeComplete(fn: MessageHandler): void {
    this.handlers.delete(fn);
  }
}

// 导出单例实例，供全局使用
export const wsService = new WsService();
