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
          <p className="text-2xl dark:text-gray-300 ">
            Last Checked:{" "}
            {new Date(items.recent_change.timestamp).toLocaleString()}
          </p>
          <div className="flex justify-center gap-4 flex-wrap">
            <button
              className={`flex justify-center flex-1 max-w-xs uppercase text-sm font-bold xs:max-h-11 p-3 m-2 ${
                loading
                  ? "bg-blue-100 text-blue-400"
                  : "bg-blue-200 text-blue-600"
              } rounded-lg`}
              onClick={loadScrapeResults}
              disabled={loading}
            >
              {loading ? <LoadingSVG /> : "Scrape Again"}
            </button>
            <button className="flex-1 max-w-xs uppercase text-sm font-bold text-blue-600 p-3 m-2 bg-blue-200 rounded-lg">
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
