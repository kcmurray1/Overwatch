import { observer } from "mobx-react-lite";
import { pageStore } from "../../stores/PageStore";
import { SideBar } from "./SideBar";
import { ToolsPage } from "../tools";
import { MachinePage } from "../machines/MachinePage";

export const MainLayout = observer(() => {
  // Function to render the active component based on MobX state
  const renderActivePage = () => {
    switch (pageStore.activePage) {
      case "home":
        return <MachinePage/>;
      case "tools":
        return <ToolsPage/>;
      case "settings":
        return ;
      default:
        return <MachinePage/>
    }
  };


   return (
          <div className="flex">
              {/* load side navbar */}
              <div className="col-span-5">
              <SideBar/>
              </div>
              {/* load control and search bar above listed containers */}
              <div className="h-screen w-full col-span-7 p-4">
                
                {renderActivePage()}

  
              </div>
  
          </div>
      )

});