import { ChangedItemsList } from "./ChangedItemsList";
import type { IChanges, ILastChange } from "../interfaces/interfaces";

interface ChangesProps {
  recentChange: IChanges;
  lastChange: ILastChange;
}

export default function Changes({ recentChange, lastChange }: ChangesProps) {
  return (
    <div className="mb-3 grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-x-3">
      <div className="bg-opacity-30 dark:bg-opacity-70 flex-1 rounded-md bg-gray-100 p-2 dark:bg-slate-800">
        <p className="dark:text-slate-300">Latest Scrape Results:</p>
        {typeof recentChange.items === "string" ? (
          <>
            <p className="text-lg font-bold dark:text-slate-300">
              {recentChange.items}
            </p>
            <section className="flex flex-col items-center">
              <p className="mt-6 mb-6 text-lg dark:text-slate-300">
                As of{" "}
                <span className="font-bold">
                  {new Date(recentChange.timestamp).toLocaleString()}
                </span>{" "}
                there are no new changes to the listings detected. Feel free to
                scrape again or check the listings directly.
              </p>
            </section>
          </>
        ) : (
          <ChangedItemsList changedItemsData={recentChange.items} />
        )}
      </div>
      <div className="bg-opacity-30 dark:bg-opacity-70 flex-1 rounded-md bg-gray-100 p-2 dark:bg-slate-800">
        <p className="dark:text-slate-300">Last Change:</p>
        {Object.keys(lastChange.items).length > 0 ? (
          <ChangedItemsList changedItemsData={lastChange.items} />
        ) : (
          <p className="text-lg dark:text-slate-300">
            No changes recorded yet.
          </p>
        )}
        {lastChange.timestamp && (
          <p className="font-bold dark:text-slate-300">
            From {new Date(lastChange.timestamp).toLocaleString()}
          </p>
        )}
      </div>
    </div>
  );
}
