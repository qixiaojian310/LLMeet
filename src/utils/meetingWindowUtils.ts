import { getCurrentWindow, LogicalSize } from '@tauri-apps/api/window';

export const closeMeetingWindow = async () => {
  const currentWindow = getCurrentWindow();
  await currentWindow.setSize(new LogicalSize(880, 530));
  currentWindow.center();
};

export const openMeetingWindow = async () => {
  const currentWindow = getCurrentWindow();
  await currentWindow.setSize(new LogicalSize(1000, 600));
  currentWindow.center();
};
