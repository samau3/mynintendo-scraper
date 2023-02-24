import { Card, Typography } from "@mui/material";
import { ItemsInterface } from "../interfaces/scrapedItems";

interface ItemCardParams {
  item: string;
  index: number;
  items: ItemsInterface;
}

export function ItemCard({ item, index, items }: ItemCardParams) {
  return (
    <Card
      key={`${item}-${index}`}
      sx={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Typography variant="subtitle1">{item}</Typography>
      <Typography sx={{ mt: "auto" }} variant="subtitle2">
        {items[item]}
      </Typography>
    </Card>
  );
}
