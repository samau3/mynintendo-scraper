import ItemGrid from "./ItemGrid";
import Changes from "./Changes";
import LoadingSVG from "./LoadingSVG";

import { IScrapeResults } from "../interfaces/interfaces";

interface ItemsProps {
  items: IScrapeResults;
  loading: boolean;
  loadScrapeResults: () => void;
}

export default function Items({
  items,
  loading,
  loadScrapeResults,
}: ItemsProps) {
  return (
    <>
      <div className="text-center">
        <div className="pb-2">
          <p className="text-2xl dark:text-gray-300">
            Last Checked:{" "}
            {new Date(items.recent_change.timestamp).toLocaleString()}
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              className={`m-2 flex max-w-xs flex-1 justify-center p-3 text-sm font-bold uppercase xs:max-h-11 ${
                loading
                  ? "bg-blue-100 text-blue-400"
                  : "bg-blue-200 text-blue-600"
              } rounded-lg`}
              onClick={loadScrapeResults}
              disabled={loading}
            >
              {loading ? <LoadingSVG /> : "Scrape Again"}
            </button>
            <button className="m-2 max-w-xs flex-1 rounded-lg bg-blue-200 p-3 text-sm font-bold uppercase text-blue-600">
              <a
                href="https://www.nintendo.com/store/exclusives/rewards/"
                target="_blank"
              >
                Check the listings
              </a>
            </button>
          </div>
        </div>
        <Changes
          recentChange={items.recent_change}
          lastChange={items.last_change}
        ></Changes>
        <ItemGrid listings={items.current_listings} imageURLs={items.images} />
      </div>
    </>
  );
}
