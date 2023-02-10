import { List, ListItem, Box } from "@mui/material";

interface IItems {
  [key: string]: string;
}

interface ItemsInterface {
  [key: string]: IItems[];
}

interface Items {
  [key: string]: ItemsInterface;
}

export function ChangedItemsList({ changedItemsData }: Items) {
  return (
    <Box>
      {Object.keys(changedItemsData).map((changeCategory, index) => (
        <List key={index}>
          {changeCategory} -
          {changedItemsData[changeCategory].map((changedItems) =>
            Object.keys(changedItems).map((changedItem, index) => (
              <ListItem key={index}>
                {changedItem} - {changedItems[changedItem]}
              </ListItem>
            ))
          )}
        </List>
      ))}
    </Box>
  );
}
