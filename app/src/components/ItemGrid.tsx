import { ItemCard } from "./ItemCard";
import { IItems } from "../interfaces/interfaces";

interface ItemGridProps {
  listings: IItems;
  imageURLs: IItems;
}

export default function ItemGrid({ listings, imageURLs }: ItemGridProps) {
  return (
    <>
      <p className="mb-auto text-lg font-bold tracking-tight text-black dark:text-slate-200">
        Current Listings:
      </p>
      <div className="grid auto-cols-fr gap-8 sm:grid-cols-3">
        {Object.keys(listings).map((item, index) => (
          <div key={index}>
            <ItemCard
              item={item}
              index={index}
              cost={listings[item]}
              imageURL={imageURLs[item]}
            />
          </div>
        ))}
      </div>
    </>
  );
}
