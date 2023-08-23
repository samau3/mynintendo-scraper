import { Box, Paper, Typography } from "@mui/material";
import { ChangedItemsList } from "./ChangedItemsList";
import { IChanges, ILastChange } from "../interfaces/scrapedItems";

interface ChangesProps {
  changes: IChanges;
  lastChange: ILastChange;
}

export default function Changes({ changes, lastChange }: ChangesProps) {
  return (
    <Box sx={{ display: "flex", justifyContent: "center" }}>
      <Paper sx={{ maxWidth: 1 / 2, marginRight: 1, padding: 1 }}>
        <Typography>Latest Scrape Results:</Typography>
        {typeof changes.changes === "string" ? (
          <Typography variant="h6"> {changes.changes}</Typography>
        ) : (
          <ChangedItemsList changedItemsData={changes.changes} />
        )}
      </Paper>
      <Paper sx={{ maxWidth: 1 / 2, marginLeft: 1, padding: 1 }}>
        <Typography>Last Change:</Typography>

        <ChangedItemsList changedItemsData={lastChange.items} />
        <Typography sx={{ fontWeight: "bold" }}>
          From {new Date(lastChange.timestamp).toLocaleString()}
        </Typography>
      </Paper>
    </Box>
  );
}
