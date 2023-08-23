export interface ItemsInterface {
  [key: string]: string;
}

export interface ScrapedItems {
  [key: string]: ItemsInterface[];
}

export interface IChanges {
  changes: ScrapedItems | string;
  timestamp: string;
}

export interface ILastChange {
  expiration: string;
  items: ScrapedItems;
  timestamp: string;
}
