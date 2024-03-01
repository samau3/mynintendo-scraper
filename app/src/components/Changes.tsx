import { ChangedItemsList } from "./ChangedItemsList";
import { IChanges, ILastChange } from "../interfaces/interfaces";

interface ChangesProps {
  recentChange: IChanges;
  lastChange: ILastChange;
}

export default function Changes({ recentChange, lastChange }: ChangesProps) {
  return (
    <div className="flex gap-x-3 mb-3">
      <div className="flex-1 bg-white rounded-md p-2 ">
        <p>Latest Scrape Results:</p>
        {typeof recentChange.items === "string" ? (
          <p className="font-bold text-lg"> {recentChange.items}</p>
        ) : (
          <ChangedItemsList changedItemsData={recentChange.items} />
        )}
      </div>
      <div className="flex-1 bg-white rounded-md p-2 ">
        <p>Last Change:</p>

        <ChangedItemsList changedItemsData={lastChange.items} />
        <p className="font-bold">
          From {new Date(lastChange.timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
}
