import { getCurrentWindow, LogicalSize } from '@tauri-apps/api/window';

export const closeMeetingWindow = () => {
  const currentWindow = getCurrentWindow();
  currentWindow.setSize(new LogicalSize(650, 400));
  currentWindow.center();
};

export const openMeetingWindow = () => {
  const currentWindow = getCurrentWindow();
  currentWindow.setSize(new LogicalSize(1000, 600));
  currentWindow.center();
};
