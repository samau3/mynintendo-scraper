import { Paper } from "@mui/material";
import { ChangedItemsList } from "./ChangedItemsList";
import { IChanges, ILastChange } from "../interfaces/interfaces";

interface ChangesProps {
  recentChange: IChanges;
  lastChange: ILastChange;
}

export default function Changes({ recentChange, lastChange }: ChangesProps) {
  return (
    <div className="flex justify-center">
      <Paper sx={{ maxWidth: 1 / 2, marginRight: 1, padding: 1 }}>
        <p>Latest Scrape Results:</p>
        {typeof recentChange.items === "string" ? (
          <p className="font-bold text-lg"> {recentChange.items}</p>
        ) : (
          <ChangedItemsList changedItemsData={recentChange.items} />
        )}
      </Paper>
      <Paper sx={{ maxWidth: 1 / 2, marginLeft: 1, padding: 1 }}>
        <p>Last Change:</p>

        <ChangedItemsList changedItemsData={lastChange.items} />
        <p className="font-bold">
          From {new Date(lastChange.timestamp).toLocaleString()}
        </p>
      </Paper>
    </div>
  );
}
