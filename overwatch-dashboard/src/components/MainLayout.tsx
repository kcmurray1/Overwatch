import { observer } from "mobx-react-lite";
import { pageStore } from "../stores/PageStore";
import { HomePage } from "./home";
import { SideBar } from "./MyNavBar";
import { ToolsPage } from "./tools";

export const MainLayout = observer(() => {
  // Function to render the active component based on MobX state
  const renderActivePage = () => {
    switch (pageStore.activePage) {
      case "home":
        return <HomePage/>;
      case "tools":
        return <ToolsPage/>;
      case "settings":
        return ;
      default:
        return <HomePage/>
    }
  };


   return (
          <div className="flex">
              {/* load side navbar */}
              <div className="col-span-5">
              <SideBar/>
              </div>
              {/* load control and search bar above listed containers */}
              <div className="h-screen col-span-7 p-4">
                
                {renderActivePage()}

  
              </div>
  
          </div>
      )

});