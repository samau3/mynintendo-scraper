import { useEffect, useState } from "react";
import { Box, Button, Container, Typography, Link } from "@mui/material";

import { MyNintendoScraperAPI } from "./api/myNintendoScraperAPI";
import {
  IChanges,
  ILastChange,
  IItems,
} from "./interfaces/interfaces";
import ItemGrid from "./components/ItemGrid";
import Changes from "./components/Changes";

interface IScrapeResults {
  recent_change: IChanges;
  current_listings: IItems;
  last_change: ILastChange;
}

function App() {
  const [scrapeResults, setScrapeResults] = useState<
    IScrapeResults | undefined
  >(undefined);

  useEffect(() => {
    loadScrapeResults();
  }, []);

  async function loadScrapeResults() {
    try {
      const results = await MyNintendoScraperAPI.getItems();
      setScrapeResults(results);
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <Container
      sx={{
        height: "100vh",
      }}
    >
      <Box sx={{ textAlign: "center" }}>
        <Typography variant="h3">MyNintendo Scraper</Typography>
      </Box>
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
    </Container>
  );
}

export default App;
