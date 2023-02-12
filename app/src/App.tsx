import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  Container,
  Grid,
  Paper,
  Typography,
} from "@mui/material";

import { MyNintendoScraperAPI } from "./api/myNintendoScraperAPI";
import { ChangedItemsList } from "./components/ChangedItemsList";
import { ScrapedItems, ItemsInterface } from "./interfaces/scrapedItems";

interface IScrapeResults {
  changes: {
    changes: ScrapedItems | string;
    timestamp: string;
  };
  current_listings: {
    [key: string]: string;
  };
  last_change: {
    expiration: string;
    items: ScrapedItems;
    timestamp: string;
  };
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
          <Box>
            <Typography variant="h6">
              Last Checked:{" "}
              {new Date(scrapeResults.changes.timestamp).toLocaleString()}
            </Typography>
            <Button onClick={loadScrapeResults}>Scrape Again</Button>
          </Box>
          <Box sx={{ display: "flex", justifyContent: "center" }}>
            <Paper sx={{ maxWidth: 1 / 2, marginRight: 1 }}>
              <Typography>Latest Scrape Results:</Typography>
              {typeof scrapeResults.changes.changes === "string" ? (
                <Typography> {scrapeResults.changes.changes}</Typography>
              ) : (
                <ChangedItemsList
                  changedItemsData={scrapeResults.changes.changes}
                />
              )}
            </Paper>
            <Paper sx={{ maxWidth: 1 / 2, marginLeft: 1 }}>
              <Typography>Last Change:</Typography>
              <Typography sx={{ fontWeight: "bold" }}>
                From{" "}
                {new Date(scrapeResults.last_change.timestamp).toLocaleString()}
              </Typography>
              <ChangedItemsList
                changedItemsData={scrapeResults.last_change.items}
              />
            </Paper>
          </Box>
          <Paper>
            <Typography variant="h6">Current Listings:</Typography>
            <Grid container spacing={1}>
              {Object.keys(scrapeResults.current_listings).map(
                (item, index) => (
                  <Grid
                    key={index}
                    minWidth={12}
                    display={"flex"}
                    item
                    xs={12}
                    md={4}
                  >
                    <Card
                      key={`${item}-${index}`}
                      sx={{ width: "100%", height: "100%" }}
                    >
                      <Typography variant="subtitle1">{item}</Typography>
                      <Typography variant="subtitle2">
                        {scrapeResults.current_listings[item]}
                      </Typography>
                    </Card>
                  </Grid>
                )
              )}
            </Grid>
          </Paper>
        </Box>
      )}
    </Container>
  );
}

export default App;
