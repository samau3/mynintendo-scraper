import { useEffect, useState } from "react";
import { AxiosError } from "axios";
import { RotatingLines } from "react-loader-spinner";

import { MyNintendoScraperAPI } from "../api/myNintendoScraperAPI";
import { IChanges, ILastChange, IItems } from "./../interfaces/interfaces";
import ItemGrid from "./ItemGrid";
import Changes from "./Changes";

interface IScrapeResults {
  recent_change: IChanges;
  current_listings: IItems;
  last_change: ILastChange;
}

export default function Items() {
  const [scrapeResults, setScrapeResults] = useState<
    IScrapeResults | undefined
  >(undefined);
  const [errorInfo, setErrorInfo] = useState<string | undefined>(undefined);

  useEffect(() => {
    loadScrapeResults();
  }, []);

  async function loadScrapeResults() {
    try {
      const results = await MyNintendoScraperAPI.getItems();
      setScrapeResults(results);
      if (errorInfo) {
        setErrorInfo(undefined);
      }
    } catch (error) {
      let message = "Something went wrong";
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
      {errorInfo && (
        <div className="text-center">
          <p className="font-bold text-lg text-red-700">{errorInfo}</p>
          <p className="font-bold text-lg">
            Please create a new issue on the{" "}
            <a
              href="https://github.com/samau3/mynintendo-scraper"
              target="_blank"
            >
              Github repository
            </a>
            .
          </p>
        </div>
      )}
      {scrapeResults ? (
        <div className="text-center">
          <div className="pb-2">
            <p className="text-2xl dark:text-gray-300 ">
              Last Checked:{" "}
              {new Date(scrapeResults.recent_change.timestamp).toLocaleString()}
            </p>
            <button
              className="uppercase text-sm font-bold text-blue-600 p-2 m-2 bg-blue-100 rounded-full"
              onClick={loadScrapeResults}
            >
              Scrape Again
            </button>
            <button className="uppercase text-sm font-bold text-blue-600 p-2 m-2 bg-blue-100 rounded-full">
              <a
                href="https://www.nintendo.com/store/exclusives/rewards/"
                target="_blank"
              >
                Check the listings
              </a>
            </button>
          </div>
          <Changes
            recentChange={scrapeResults.recent_change}
            lastChange={scrapeResults.last_change}
          ></Changes>
          <ItemGrid listings={scrapeResults.current_listings} />
        </div>
      ) : (
        <div className="mt-10">
          <RotatingLines strokeColor="gray" />
        </div>
      )}
    </>
  );
}
