import { ItemCard } from "./ItemCard";
import { IItems } from "../interfaces/interfaces";

export default function ItemGrid({ listings }: { listings: IItems }) {
  return (
    <>
      
      <p className="mb-auto text-lg tracking-tight text-black dark:text-slate-200 ">
        Current Listings:
        </p>
        <div className="grid auto-cols-fr gap-8 sm:grid-cols-3">
          {Object.keys(listings).map((item, index) => (
            <div
              key={index}
            >
              <ItemCard item={item} index={index} cost={listings[item]} />
            </div>
          ))}
        </div>
    </>
  );
}
