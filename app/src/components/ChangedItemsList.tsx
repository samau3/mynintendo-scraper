import { IScrapedItems } from "../interfaces/interfaces";
import { ItemCard } from "./ItemCard";

interface ChangedItemsListProps {
  [key: string]: IScrapedItems;
}

export function ChangedItemsList({ changedItemsData }: ChangedItemsListProps) {
  return (
    <>
      {Object.keys(changedItemsData).map((changeCategory, index) => (
        <div key={index} >
          <div  >
            <p className="mb-auto text-lg font-bold tracking-tight text-black dark:text-slate-200">{changeCategory}</p>
            <div className="grid auto-cols-auto">
              {changedItemsData[changeCategory].map((changedItems) =>
                Object.keys(changedItems).map((changedItem, index) => (
                  <div
                    key={`${changedItem}-${index}`}
                    className="m-1"
                  >
                    <ItemCard
                      item={changedItem}
                      index={index}
                      cost={changedItems[changedItem]}
                    />
                  </div>
                )),
              )}
            </div>
          </div>
        </div>
      ))}
    </>
  );
}
