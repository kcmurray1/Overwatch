import { observer } from "mobx-react-lite";
import { machineStore } from "../../stores/MachineStore";
import { useState } from "react";
import { CustomApiRequest, type MessageOnlyResponse } from "../../FetchAPI";

export const ScannerPage = observer(() => {

    const [isScanning, setIsScanning] = useState<boolean>(false);

    const handleRunScan = async () => {
        setIsScanning(true);
        try {
            console.info("Scanning...")
            const res = await CustomApiRequest<MessageOnlyResponse>("machines/scan", {}, "POST");

        } catch (err) {
            console.error(err as Error);
        } finally {
            setIsScanning(false);
        }
    }

    return (
        <div className="flex flex-col p-4 bg-primary-light dark:bg-primary-dark">
            <div className="flex items-center p-4 justify-between">
                <div>
                    <h1 className="text-lg font-semibold text-slate-100">Network Scanner</h1>
                    <p className="text-xs">Review active machine IP addresses and ports</p>
                </div>
                <button onClick={handleRunScan} className="p-2 rounded-xl bg-accent-light dark:bg-accent-dark  hover:bg-select-light dark:hover:bg-select-dark transition-colors">Scan</button>
            </div>
            <table className="p-4 font-mono border-2 border-accent-light dark:border-accent-dark bg-surface-card-dark">
                <thead>
                <tr>
                    <th  className="p-2">Machine</th>
                    <th  className="p-2">Address</th>
                    <th className="p-2">Port</th>
                </tr>
                </thead>
                <tbody>
                {machineStore.machines.map((machine) => {
                    return <tr key={machine.id}>
                            <td className="p-2">{machine.model}</td>
                            <td className="p-2">{machine.address}</td>
                            <td className="p-2">{machine.port}</td>
                        </tr>
                })}
                </tbody>
            </table>
        </div>
    )
});