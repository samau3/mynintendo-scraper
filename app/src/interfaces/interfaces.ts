export interface IItems {
  [key: string]: string;
}

export interface IScrapedItems {
  [key: string]: IItems[];
}

export interface IChanges {
  changes: IScrapedItems | string;
  timestamp: string;
}

export interface ILastChange {
  expiration: string;
  items: IScrapedItems;
  timestamp: string;
}
