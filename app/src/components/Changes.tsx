import { ChangedItemsList } from "./ChangedItemsList";
import { IChanges, ILastChange } from "../interfaces/interfaces";

interface ChangesProps {
  recentChange: IChanges;
  lastChange: ILastChange;
}

export default function Changes({ recentChange, lastChange }: ChangesProps) {
  return (
    <div className="grid grid-cols-2 gap-x-3 mb-3">
      <div className="flex-1 rounded-md p-2 bg-gray-100 bg-opacity-30 dark:bg-slate-800 dark:bg-opacity-70">
        <p className="dark:text-slate-300">Latest Scrape Results:</p>
        {typeof recentChange.items === "string" ? (
          <>
            <p className="font-bold text-lg dark:text-slate-300">
              {recentChange.items}
            </p>
            <section className="flex flex-col items-center">
              <p className="mt-10 text-lg dark:text-slate-300">
                As of <span className="font-bold">{new Date(recentChange.timestamp).toLocaleString()}</span> there
                are no new changes to the listings detected. Feel free to scrape again or check the listings directly.
              </p>
            </section>
          </>
        ) : (
          <ChangedItemsList changedItemsData={recentChange.items} />
        )}
      </div>
      <div className="flex-1 rounded-md p-2 bg-gray-100 bg-opacity-30 dark:bg-slate-800 dark:bg-opacity-70 ">
        <p className="dark:text-slate-300">Last Change:</p>
        <ChangedItemsList changedItemsData={lastChange.items} />
        <p className="font-bold dark:text-slate-300">
          From {new Date(lastChange.timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
}
