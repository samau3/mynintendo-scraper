import React, { useEffect, useState } from "react";
import {
  Box,
  Container,
  List,
  ListItem,
  Paper,
  Typography,
} from "@mui/material";

import { MyNintendoScraperAPI } from "./api/myNintendoScraperAPI";
import { ChangedItemsList } from "./components/changedItemsList";

interface IItems {
  [key: string]: string;
}

interface ItemsInterface {
  [key: string]: IItems[];
}

interface IScrapeResults {
  changes: {
    changes: ItemsInterface;
    timestamp: string;
  };
  current_listings: {
    [key: string]: string;
  };
  last_change: {
    expiration: string;
    items: {
      [key: string]: IItems[];
    };
    timestamp: string;
  };
}

function App() {
  const [scrapeResults, setScrapeResults] = useState<
    IScrapeResults | undefined
  >(undefined);
  useEffect(() => {
    async function loadScrapeResults() {
      try {
        const results = await MyNintendoScraperAPI.getItems();
        setScrapeResults(results);
      } catch (error) {
        console.log(error);
      }
    }
    loadScrapeResults();
  }, []);

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
        <Box>
          <Box sx={{ textAlign: "center" }}>
            <Typography variant="h6">
              Last Checked: {scrapeResults.changes.timestamp}
            </Typography>
          </Box>
          <Box>
            <Paper>
              <Typography>Latest Scrape Results:</Typography>
              {typeof scrapeResults.changes.changes === "string" ? (
                <Typography> {scrapeResults.changes.changes}</Typography>
              ) : (
                <ChangedItemsList
                  changedItemsData={scrapeResults.changes.changes}
                />
              )}
            </Paper>
          </Box>
          <Box>
            <Paper>
              <Typography>Last Change:</Typography>
              On {scrapeResults.last_change.timestamp}
              <ChangedItemsList
                changedItemsData={scrapeResults.last_change.items}
              />
            </Paper>
          </Box>
          <Box>
            <Paper>
              <Typography>Current Listings:</Typography>
              <List>
                {Object.keys(scrapeResults.current_listings).map(
                  (key, index) => (
                    <ListItem key={index}>
                      {key} - {scrapeResults.current_listings[key]}
                    </ListItem>
                  )
                )}
              </List>
            </Paper>
          </Box>
        </Box>
      )}
    </Container>
  );
}

export default App;
