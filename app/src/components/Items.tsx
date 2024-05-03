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
  images: IItems;
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
    setLoading((prev) => !prev);
    try {
      const results = await MyNintendoScraperAPI.getItems();
      setScrapeResults(results);
      setLoading((prev) => !prev);
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
              className={`uppercase text-sm font-bold p-2 m-2 ${
                loading
                  ? "bg-blue-100 text-blue-400"
                  : "bg-blue-200 text-blue-600"
              } rounded-lg`}
              onClick={loadScrapeResults}
              disabled={loading}
            >
              {loading ? (
                <svg
                  aria-hidden="true"
                  className="w-6 h-6 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                  viewBox="0 0 100 101"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor"
                  />
                  <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill"
                  />
                </svg>
              ) : (
                "Scrape Again"
              )}
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
          <ItemGrid listings={scrapeResults.current_listings} imageURLs={scrapeResults.images} />
        </div>
      )}
    </>
  );
}
