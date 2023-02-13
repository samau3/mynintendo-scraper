import { Grid, Card, Typography, Box, Paper } from "@mui/material";

import { ScrapedItems } from "../interfaces/scrapedItems";

interface ItemsParameter {
  [key: string]: ScrapedItems;
}

export function ChangedItemsList({ changedItemsData }: ItemsParameter) {
  return (
    <Grid>
      {Object.keys(changedItemsData).map((changeCategory, index) => (
        <Paper variant="outlined" key={index} sx={{ padding: 1 }}>
          <Box textAlign={"center"}>
            <Typography variant="h6">{changeCategory}</Typography>
            <Grid container spacing={1} justifyContent={"center"}>
              {changedItemsData[changeCategory].map((changedItems) =>
                Object.keys(changedItems).map((changedItem, index) => (
                  <Grid
                    key={`${changedItem}-${index}`}
                    item
                    xs={12}
                    sm={6}
                    sx={{ width: "100%" }}
                  >
                    <Card
                      variant="outlined"
                      sx={{ width: "100%", height: "100%" }}
                    >
                      <Typography variant="subtitle1">{changedItem}</Typography>
                      <Typography variant="subtitle2">
                        {changedItems[changedItem]}
                      </Typography>
                    </Card>
                  </Grid>
                ))
              )}
            </Grid>
          </Box>
        </Paper>
      ))}
    </Grid>
  );
}
