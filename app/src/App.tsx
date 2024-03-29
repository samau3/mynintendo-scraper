import Items from "./components/Items";
import ThemeSwitcher from "./components/ThemeSwitcher";

import styles from "./App.module.css";

function App() {
  return (
    <>
      <div id={styles.app}>
        <div id={styles["star-container"]}>
          <div id={styles["star-pattern"]}></div>
          <div id={styles["star-gradient-overlay"]}></div>
        </div>
        <div id={styles["stripe-container"]}>
          <div id={styles["stripe-pattern"]}></div>
        </div>

        {/* <div className="flex flex-col items-center p-4 min-h-screen">
          <div className="w-full flex flex-row-reverse sm:absolute sm:w-min right-5 top-5">
            <ThemeSwitcher />
          </div>
          <Items />
        </div> */}
      </div>
    </>
  );
}

export default App;
