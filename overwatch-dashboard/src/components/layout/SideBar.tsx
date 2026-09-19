import { observer } from "mobx-react-lite";
import { useState } from "react";
import { pageStore } from "../../stores/PageStore";
import { ThemeToggle } from "../ThemeToggle";


const SettingsComponent = observer(() => {
    return (
        <>
        <p>Settings</p>
        </>
    )
})

export const SideBar = observer(() => {
    const [isExpanded, setIsExpanded] = useState(false);


    return (
        <div className="h-full flex z-40 pointer-events-none bg-primary-light dark:bg-primary-dark">
            <div className="h-full w-16 flex flex-col items-center py-4 space-y-4 pointer-events-auto">
                <button
                    onClick={() => {pageStore.page = "home"}}
                >
                Home    
                </button>
                <button
                    onClick={() => {pageStore.page = "tools"}}
                >
                Tools    
                </button>                
                <button
                onClick={() => {setIsExpanded(!isExpanded)}}
                >
                Settings
                </button>

                <ThemeToggle/>
            </div>

            <div 
                className={`bg-primary-light h-full w-[400px] shadow-2xl flex flex-col pointer-events-auto ${
                    isExpanded ? "block" : "hidden"
                }`}
            >
            <SettingsComponent/>
        
            </div>

        </div>
    )
});
