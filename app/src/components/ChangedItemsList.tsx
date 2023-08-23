import { Grid, Typography, Box, Paper } from "@mui/material";

import { ScrapedItems } from "../interfaces/scrapedItems";
import { ItemCard } from "./ItemCard";

interface ChangedItemsListProps {
  [key: string]: ScrapedItems;
}

export function ChangedItemsList({ changedItemsData }: ChangedItemsListProps) {
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
                    <ItemCard
                      item={changedItem}
                      index={index}
                      cost={changedItems[changedItem]}
                    />
                  </Grid>
                )),
              )}
            </Grid>
          </Box>
        </Paper>
      ))}
    </Grid>
  );
}
