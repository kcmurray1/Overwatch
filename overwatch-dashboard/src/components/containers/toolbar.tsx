import { observer } from "mobx-react-lite";
import { FaPlay, FaPlus, FaStop } from "react-icons/fa";
    
export const ToolBar = observer (() => {
    return (
        <div className="flex justify-between w-full p-4">
            <div>
                <input type="search" placeholder="Search..."></input>
            </div>

            <div className="flex justify-between gap-3">
            <p>CPU</p>
            <p>Memory</p>
            <p>Storage</p>
            </div>

        </div>
    )
});