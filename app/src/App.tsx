import { useEffect, useState } from "react";
import { AxiosError } from "axios";
import { RotatingLines } from "react-loader-spinner";

import { MyNintendoScraperAPI } from "./api/myNintendoScraperAPI";
import { IScrapeResults } from "./interfaces/interfaces";

import Items from "./components/Items";
import ThemeSwitcher from "./components/ThemeSwitcher";
import ErrorView from "./components/ErrorView";

import styles from "./App.module.css";

function App() {
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
        console.error(error);
      }
      setErrorInfo(message);

      if (scrapeResults) {
        setScrapeResults(undefined);
      }
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
        <div className="right-5 top-5 flex w-full flex-row-reverse sm:absolute sm:w-min">
          <ThemeSwitcher />
        </div>
        <div>
          <p className="text-4xl dark:text-gray-300">MyNintendo Scraper</p>
        </div>
        {errorInfo && <ErrorView errorInfo={errorInfo} />}

        {shouldShowLoading && (
          <div className="mt-10">
            <RotatingLines strokeColor="gray" />
          </div>
        )}

        {scrapeResults && (
          <Items
            items={scrapeResults}
            loading={loading}
            loadScrapeResults={loadScrapeResults}
          />
        )}
      </div>
    </>
  );
}

export default App;
