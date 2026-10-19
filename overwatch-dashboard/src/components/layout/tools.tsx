import { observer } from "mobx-react-lite";
import { ScannerPage } from "../scanner/ScannerPage";


export const ToolsPage = observer(() => {

    return (
        <div className="flex flex-1">
        <ScannerPage />
        <h1>Tools</h1>
        </div>
    )
});