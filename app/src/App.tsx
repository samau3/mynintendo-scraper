import Items from "./components/Items";
import ThemeSwitcher from "./components/ThemeSwitcher";

function App() {
  return (
    <div className="flex flex-col items-center p-4 bg-white dark:bg-slate-800">
      <div className="w-full flex flex-row-reverse ">
        <ThemeSwitcher />
      </div>
      <Items />
    </div>
  );
}

export default App;
