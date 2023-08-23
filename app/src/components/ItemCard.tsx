import { Card, Typography } from "@mui/material";

interface ItemCardProps {
  item: string;
  index: number;
  cost: string;
}

export function ItemCard({ item, index, cost }: ItemCardProps) {
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
        {cost}
      </Typography>
    </Card>
  );
}
