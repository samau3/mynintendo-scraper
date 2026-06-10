import { useEffect, useState } from "react";
import { RotatingLines } from "react-loader-spinner";

import { MyNintendoScraperAPI } from "./api/myNintendoScraperAPI";
import type { IScrapeResults } from "./interfaces/interfaces";

import Items from "./components/Items";
import ThemeSwitcher from "./components/ThemeSwitcher";
import ErrorView from "./components/ErrorView";

import styles from "./App.module.css";

function App() {
  const [scrapeResults, setScrapeResults] = useState<
    IScrapeResults | undefined
  >(undefined);
  const [errorInfo, setErrorInfo] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(true);
  const [hasLoadedCache, setHasLoadedCache] = useState<boolean>(false);

  const shouldShowLoading = loading && !scrapeResults;

  useEffect(() => {
    loadCachedResults();
  }, []);

  async function loadCachedResults() {
    setLoading(true);
    try {
      const cached = await MyNintendoScraperAPI.getCachedItems();
      if (cached) {
        setScrapeResults(cached);
        setErrorInfo(undefined);
      }
    } catch (error: unknown) {
      const message =
        error instanceof Error ? error.message : "Something went wrong.";
      setErrorInfo(message);
    } finally {
      setLoading(false);
      setHasLoadedCache(true);
    }
  }

  async function scrapeAgain() {
    setLoading(true);
    try {
      const results = await MyNintendoScraperAPI.scrapeItems();
      setScrapeResults(results);
      setErrorInfo(undefined);
    } catch (error: unknown) {
      const message =
        error instanceof Error ? error.message : "Something went wrong.";
      setErrorInfo(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div id={styles.wrapper}>
        <div id={styles["star-container"]}>
          <div id={styles["star-pattern"]}></div>
          <div id={styles["star-gradient-overlay"]}></div>
        </div>
        <div id={styles["stripe-container"]}>
          <div id={styles["stripe-pattern"]}></div>
        </div>
      </div>
      <div className="absolute top-0 z-10 flex min-h-screen min-w-full flex-col items-center p-4">
        <div className="top-5 right-5 flex w-full flex-row-reverse sm:absolute sm:w-min">
          <ThemeSwitcher />
        </div>
        <div>
          <p className="text-4xl dark:text-gray-300">MyNintendo Scraper</p>
        </div>
        {errorInfo && <ErrorView errorInfo={errorInfo} />}

        {shouldShowLoading && (
          <div className="mt-10">
            <RotatingLines color="gray" ariaLabel="loading" />
          </div>
        )}

        {scrapeResults && (
          <Items
            items={scrapeResults}
            loading={loading}
            loadScrapeResults={scrapeAgain}
          />
        )}

        {!scrapeResults && !errorInfo && hasLoadedCache && !loading && (
          <div className="mt-10 text-center">
            <p className="mb-4 dark:text-slate-300">
              No cached listings found. Run a scrape to fetch current items.
            </p>
            <button
              className="rounded-lg bg-blue-200 px-6 py-3 text-sm font-bold text-blue-600 uppercase"
              onClick={scrapeAgain}
            >
              Scrape Now
            </button>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
