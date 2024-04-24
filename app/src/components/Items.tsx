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

const API_STATUS_URL = "https://j50pzswk.status.cron-job.org/";

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
    setLoading(prev => !prev);
    try {
      const results = await MyNintendoScraperAPI.getItems();
      setScrapeResults(results);
      setLoading(prev => !prev);
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
          <p className="font-bold text-lg dark:text-gray-300">
            Please create a new issue on the{" "}
            <a
              href={API_STATUS_URL}
              target="_blank"
              className="text-blue-600 underline"
            >
              Github repository
            </a>
            .
          </p>
          <button className="uppercase text-sm font-bold text-blue-600 p-2 m-2 bg-blue-100 rounded-lg">
            <a href={API_STATUS_URL} target="_blank">
              API Status
            </a>
          </button>
        </div>
      )}

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
            <button
              className={`uppercase text-sm font-bold text-blue-600 p-2 m-2 bg-blue-200 ${loading ? "bg-blue-100 text-blue-400" : ""} rounded-lg`}
              onClick={loadScrapeResults}
              disabled={loading}
            >
              Scrape Again
            </button>
            <button className="uppercase text-sm font-bold text-blue-600 p-2 m-2 bg-blue-200 rounded-lg">
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
      )}
    </>
  );
}
