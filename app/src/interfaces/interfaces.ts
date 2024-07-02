export interface IItems {
  [key: string]: string;
}

export interface IScrapedItems {
  [key: string]: IItems[];
}

export interface IChanges {
  items: IScrapedItems | string;
  timestamp: string;
}

export interface ILastChange {
  expiration: string;
  items: IScrapedItems;
  timestamp: string;
}

export interface IScrapeResults {
  recent_change: IChanges;
  current_listings: IItems;
  last_change: ILastChange;
  images: IItems;
}
