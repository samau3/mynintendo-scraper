import { Paper, Typography, Grid } from "@mui/material";
import { ItemCard } from "./ItemCard";
import { ItemsInterface } from "../interfaces/scrapedItems";

export default function ItemGrid({ listings }: { listings: ItemsInterface }) {
  return (
    <>
      <Paper sx={{ padding: 1 }}>
        <Typography variant="h6">Current Listings:</Typography>
        <Grid container spacing={1}>
          {Object.keys(listings).map((item, index) => (
            <Grid
              key={index}
              minWidth={12}
              display={"flex"}
              item
              xs={12}
              sm={6}
              md={4}
            >
              <ItemCard item={item} index={index} cost={listings[item]} />
            </Grid>
          ))}
        </Grid>
      </Paper>
    </>
  );
}
