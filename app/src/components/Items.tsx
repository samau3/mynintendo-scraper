import { useEffect, useState } from "react";
import { AxiosError } from "axios";
import { RotatingLines } from "react-loader-spinner";

import { MyNintendoScraperAPI } from "../api/myNintendoScraperAPI";
import { IChanges, ILastChange, IItems } from "./../interfaces/interfaces";
import ItemGrid from "./ItemGrid";
import Changes from "./Changes";
import ErrorView from "./ErrorView";
import LoadingSVG from "./LoadingSVG";

interface IScrapeResults {
  recent_change: IChanges;
  current_listings: IItems;
  last_change: ILastChange;
  images: IItems;
}


export default function Items() {
  const [scrapeResults, setScrapeResults] = useState<
    IScrapeResults | undefined
  >(undefined);
  const [errorInfo, setErrorInfo] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(false);

  const shouldShowLoading = !scrapeResults && !errorInfo;

  useEffect(() => {
    loadScrapeResults();
  }, []);

  async function loadScrapeResults() {
    setLoading((prev) => !prev);
    try {
      const results = await MyNintendoScraperAPI.getItems();
      setScrapeResults(results);
      setLoading((prev) => !prev);
      if (errorInfo) {
        setErrorInfo(undefined);
      }
    } catch (error) {
      let message = "Something went wrong.";
      if (error instanceof AxiosError) {
        message = error?.response?.data.message;
      } else {
        console.log(error);
      }
      setErrorInfo(message);

      if (scrapeResults) {
        setScrapeResults(undefined);
      }
    }
  }

  return (
    <>
      <div>
        <p className="text-4xl dark:text-gray-300 ">MyNintendo Scraper</p>
      </div>
      {errorInfo && <ErrorView errorInfo={errorInfo} />}

      {shouldShowLoading && (
        <div className="mt-10">
          <RotatingLines strokeColor="gray" />
        </div>
      )}

      {scrapeResults && (
        <div className="text-center">
          <div className="pb-2">
            <p className="text-2xl dark:text-gray-300 ">
              Last Checked:{" "}
              {new Date(scrapeResults.recent_change.timestamp).toLocaleString()}
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
            recentChange={scrapeResults.recent_change}
            lastChange={scrapeResults.last_change}
          ></Changes>
          <ItemGrid
            listings={scrapeResults.current_listings}
            imageURLs={scrapeResults.images}
          />
        </div>
      )}
    </>
  );
}
