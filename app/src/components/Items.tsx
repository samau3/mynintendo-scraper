import { useEffect, useState } from "react";
import { Box, Button, Container, Typography, Link } from "@mui/material";
import { AxiosError } from "axios";

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
    } catch (error) {
      let message = "Something went wrong";
      if (error instanceof AxiosError) {
        message = error?.response?.data.message;
      } else {
        console.log(error);
      }
      setErrorInfo(message);
    }
  }

  return (
    <>
      <Box sx={{ textAlign: "center" }}>
        <Typography variant="h3">MyNintendo Scraper</Typography>
      </Box>
      {errorInfo && (
        <Box sx={{ textAlign: "center" }}>
          <Typography variant="h5" color="red">
            {errorInfo}
          </Typography>
          <Typography variant="h5">
            Please create a new issue on the{" "}
            <a
              href="https://github.com/samau3/mynintendo-scraper"
              target="_blank"
            >
              Github repository
            </a>
            .
          </Typography>
        </Box>
      )}
      {scrapeResults && (
        <Box textAlign={"center"}>
          <Box paddingBottom={1}>
            <Typography variant="h6">
              Last Checked:{" "}
              {new Date(scrapeResults.recent_change.timestamp).toLocaleString()}
            </Typography>
            <Button onClick={loadScrapeResults}>Scrape Again</Button>
            <Button>
              <Link
                href="https://www.nintendo.com/store/exclusives/rewards/"
                target="_blank"
                underline="none"
              >
                Check the listings
              </Link>
            </Button>
          </Box>
          <Changes
            recentChange={scrapeResults.recent_change}
            lastChange={scrapeResults.last_change}
          ></Changes>
          <ItemGrid listings={scrapeResults.current_listings} />
        </Box>
      )}
    </>
  );
}
