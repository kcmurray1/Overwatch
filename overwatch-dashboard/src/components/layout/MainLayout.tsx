import { observer } from "mobx-react-lite";
import { pageStore } from "../../stores/PageStore";
import { SideBar } from "./SideBar";
import { ToolsPage } from "./tools";
import { MachinePage } from "../machines/MachinePage";
import { Home } from "./home";

export const MainLayout = observer(() => {
  // Function to render the active component based on MobX state
  const renderActivePage = () => {
    switch (pageStore.activePage) {
      case "home":
        return <Home/>;
      case "tools":
        return <ToolsPage/>;
      case "settings":
        return ;
      default:
        return <Home/>
    }
  };


   return (
          <div className="min-h-screen flex">
              {/* load side navbar */}
              <div className="shrink-0">
              <SideBar/>
              </div>
              {/* load control and search bar above listed containers */}
              <div className="flex-1 p-4">
                
                {renderActivePage()}

  
              </div>
  
          </div>
      );

});