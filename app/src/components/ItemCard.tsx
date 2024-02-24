interface ItemCardProps {
  item: string;
  index: number;
  cost: string;
}

export function ItemCard({ item, index, cost }: ItemCardProps) {
  return (
    <div
      key={`${item}-${index}`}
      className="w-full h-full flex flex-col shadow-lg p-4 bg-white dark:bg-slate-800 rounded-lg justify-between"
    >
      <img src="https://placehold.co/300" />
      <p className="mb-auto text-lg tracking-tight text-black dark:text-slate-200 ">
        {item}
      </p>
      <p className="text-md tracking-tighter text-black dark:text-slate-300 ">
        {cost}
      </p>
    </div>
  );
}
