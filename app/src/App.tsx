import Items from "./components/Items";
import ThemeSwitcher from "./components/ThemeSwitcher";

import styles from "./App.module.css";

function App() {
  return (
    <>
      <div id={styles.wrapper}>
        <div id={styles["star-container"]}>
          <div id={styles["star-pattern"]}></div>
          <div id={styles["star-gradient-overlay"]}></div>
        </div>
        <div id={styles["stripe-container"]}>
          <div id={styles["stripe-pattern"]}></div>
        </div>
      </div>
      <div className="flex flex-col items-center p-4 min-h-screen min-w-full absolute top-0 z-10 ">
        <div className="w-full flex flex-row-reverse sm:absolute sm:w-min right-5 top-5">
          <ThemeSwitcher />
        </div>
        <Items />
        <button className="uppercase text-sm font-bold text-blue-600 p-2 m-2 bg-blue-100 rounded-lg">
              <a
                href="https://j50pzswk.status.cron-job.org/"
                target="_blank"
              >
                API Status
              </a>
            </button>
      </div>
    </>
  );
}

export default App;
