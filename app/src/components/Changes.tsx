import { ChangedItemsList } from "./ChangedItemsList";
import { IChanges, ILastChange } from "../interfaces/interfaces";

interface ChangesProps {
  recentChange: IChanges;
  lastChange: ILastChange;
}

export default function Changes({ recentChange, lastChange }: ChangesProps) {
  return (
    <div className="flex gap-x-3 mb-3">
      <div className="flex-1 rounded-md p-2 dark:bg-slate-800 ">
        <p className="dark:text-slate-300">Latest Scrape Results:</p>
        {typeof recentChange.items === "string" ? (
          <p className="font-bold text-lg dark:text-slate-300"> {recentChange.items}</p>
        ) : (
          <ChangedItemsList changedItemsData={recentChange.items} />
        )}
      </div>
      <div className="flex-1 rounded-md p-2 dark:bg-slate-800 ">
        <p className="dark:text-slate-300">Last Change:</p>

        <ChangedItemsList changedItemsData={lastChange.items} />
        <p className="font-bold dark:text-slate-300">
          From {new Date(lastChange.timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
}
