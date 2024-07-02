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
      className="flex h-full w-full flex-col justify-between rounded-lg border-2 bg-gray-100 bg-opacity-80 p-4 shadow-lg dark:border-gray-600 dark:bg-slate-800 dark:bg-opacity-80"
    >
      {imageURL && <img className="mb-2" src={imageURL} />}
      <p className="mb-auto text-lg tracking-tight text-black dark:text-slate-200">
        {item}
      </p>
      <p className="text-md font-medium tracking-tighter text-black dark:text-slate-300">
        {cost}
      </p>
    </div>
  );
}
