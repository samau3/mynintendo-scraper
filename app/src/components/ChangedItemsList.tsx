import { Grid, Card, Typography, Box, Paper } from "@mui/material";

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
    <Grid>
      {Object.keys(changedItemsData).map((changeCategory, index) => (
        <Paper>
          <Box textAlign={"center"}>
            <Typography variant="h6">{changeCategory}</Typography>
            <Grid container spacing={1} justifyContent={"center"} key={index}>
              {changedItemsData[changeCategory].map((changedItems) =>
                Object.keys(changedItems).map((changedItem, index) => (
                  <Grid item md={4} sx={{ width: "100%" }}>
                    <Card key={index} sx={{ width: "100%", height: "100%" }}>
                      <Typography variant="subtitle1">{changedItem}</Typography>
                      <Typography variant="subtitle2">
                        {changedItems[changedItem]}
                      </Typography>
                    </Card>
                  </Grid>
                ))
              )}
            </Grid>
          </Box>
        </Paper>
      ))}
    </Grid>
  );
}
