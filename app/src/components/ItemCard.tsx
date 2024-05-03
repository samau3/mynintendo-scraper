interface ItemCardProps {
  item: string;
  index: number;
  cost: string;
  imageURL?: string;
}

export function ItemCard({ item, index, cost, imageURL }: ItemCardProps) {
  return (
    <div
      key={`${item}-${index}`}
      className="w-full h-full flex flex-col shadow-lg p-4 bg-gray-100 bg-opacity-80 border-2 dark:bg-slate-800 dark:border-gray-600 dark:bg-opacity-80 rounded-lg justify-between"
    >
      {imageURL && <img className="mb-2" src={imageURL} />}
      <p className="mb-auto text-lg tracking-tight text-black dark:text-slate-200 ">
        {item}
      </p>
      <p className="text-md font-medium tracking-tighter text-black dark:text-slate-300 ">
        {cost}
      </p>
    </div>
  );
}
