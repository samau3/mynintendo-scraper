import Items from "./components/Items";
import ThemeSwitcher from "./components/ThemeSwitcher";

function App() {
  return (
    <div className="flex flex-col items-center p-4 bg-white dark:bg-slate-800 min-h-screen">
      <div className="w-full flex flex-row-reverse sm:absolute sm:w-min right-5 top-5">
        <ThemeSwitcher />
      </div>
      <Items />
    </div>
  );
}

export default App;
