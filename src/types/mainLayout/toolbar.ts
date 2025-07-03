import { IconDefinition } from '@fortawesome/fontawesome-svg-core';

export interface ToolbarItem {
  title: string;
  icon: IconDefinition;
  path: string;
}

export interface ToolCardItem {
  title: string;
  icon: IconDefinition;
  photo: string;
  description: string;
  path: string;
}
