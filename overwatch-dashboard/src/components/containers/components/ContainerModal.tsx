import { observer } from "mobx-react-lite";
import { useState } from "react";
import { BaseModal, type BaseModalProps } from "../../common/BaseModal";
import { GenericConfigEditor } from "../../common/ConfigEditor/ConfigEditor";
import type { ContainerConfig } from "../types/configs";
import { containerStore } from "../../../stores/ContainerStore";
import { machineStore } from "../../../stores/MachineStore";
import { TextField } from "../../common/ConfigEditor/components/TextField";
import { NumberField } from "../../common/ConfigEditor/components/NumberField";


type ConfigUpdater<T> = (recipe: (draft: T) => void) => void;


const ContainerForm = observer(({config, update}: {config: ContainerConfig, update: ConfigUpdater<ContainerConfig>}) => {
    return (
        <div>
            <TextField  label="Name" value={config.name}  />
            <TextField label="Description" value={config.description ? config.description : "No Description"}/>
            <h1>Configuration</h1>
            <TextField label="Image" value={config.spec?.image} onChange={(value) => {
                update((draft) => {
                    draft.spec.image = value;
                })
            }}/>
            <TextField label="Container Name" value={config.spec?.name} onChange={(value) => {
                update((draft) => {
                    draft.spec.name = value;
                })
            }}/>
            

            {config.spec && (
                    <div>
                        <h3 className="font-bold">Environment Variables</h3>
                        <div className="grid grid-cols-2 p-2">
                        {Object.entries(config.spec?.environment || {}).map(([key, val], index) => {
                            if (typeof val === 'string') {
                                return (
                                    <TextField
                                        key={index}
                                        label={key}
                                        value={val}
                                        onChange={(newVal) => update((draft) => {
                                            if (draft.spec.environment) {
                                                draft.spec.environment[key] = newVal;
                                            }
                                        })}
                                    />
                                );
                            }
                            if (typeof val === 'number') {
                                return <p key={index}>{key}: {val}</p>;
                            }
                        })}
                        </div>
                    </div>
                )}
             {config.spec && ( 
                <div>
                <h3 className="font-bold">Ports</h3>
                <div className="grid grid-cols-2 p-2">
                {Object.entries(config.spec.ports || {}).map(([key, val], index) => {
                if (typeof val === 'string') {
                        return <TextField
                        key={index}
                        label={key}
                        value={val}
                        onChange={(newVal) => update((draft) => {
                            if (draft.spec.ports) {
                                draft.spec.ports[key] = newVal
                            }
                        })}
                        />
                    }
                    if(typeof val === 'number') {
                    return <NumberField
                    key={index}
                    label={key}
                    value={val}
                    onChange={(newVal) => update((draft) => {
                            if (draft.spec.ports) {
                                draft.spec.ports[key] = newVal
                            }
                        })}
                    />
                    }
                })}
                </div>
            </div>
            )
            }

            </div>
   
    )
});




export const ContainerModal = observer(({isOpen, onClose}: BaseModalProps) => {

    const [selectedName, setSelectedName] = useState<string>("");
    const [selectedMachineIds, setSelectedMachineIds] = useState<number[]>([]);

    const handleToggleMachine = (machineId: number) => {
        setSelectedMachineIds(prev => 
            prev.includes(machineId) 
                ? prev.filter(id => id !== machineId) 
                : [...prev, machineId]
        );
    };

    // Convert MobX Map values into an array for the dropdown options
    const configs: ContainerConfig[] = Array.from(containerStore.configMap.values());
    
    // Determine the active config (fallback to the first one if none selected)
    const activeConfig = configs.find(c => c.name === selectedName) || configs[0];
    if (containerStore.loading) { return <p>loading...</p>}
    return (
        <BaseModal maxWidth="max-w-4xl" isOpen={isOpen} onClose={onClose}>
            <div>
                <label className="block text-sm font-semibold">
                    Add Container
                </label>
                <div className="p-2">
                    <div className="flex items-center justify-between">
                        <label className="font-bold">
                            Target Machines
                        </label>
                        <span className="text-xs">
                            {selectedMachineIds.length} selected
                        </span>
                    </div>

                    <div className="p-2 grid grid-cols-4">
                           {machineStore.machines.map((machine, index) => {
                                const isSelected = selectedMachineIds.includes(machine.id);
                                const isOnline = machine.is_online; // Assuming this is boolean based on your status span

                                return (
                                    <div
                                        key={machine.id}
                                        onClick={() => {
                                            if (isOnline) {
                                                handleToggleMachine(machine.id);
                                            }
                                        }}
                                        className={`flex items-center justify-between p-3 rounded-lg border transition-all ${
                                            !isOnline
                                                ? "bg-accent-dark/40 border-zinc-800 opacity-50 cursor-not-allowed" // Greyed out & disabled styling
                                                : isSelected 
                                                    ? "bg-emerald-950/40 border-emerald-300 cursor-pointer" 
                                                    : "bg-accent-dark border-zinc-700 hover:border-zinc-500 cursor-pointer"
                                        }`}
                                    >
                                        <div className="flex items-center space-x-3">
                                            <input
                                                type="checkbox"
                                                checked={isSelected}
                                                disabled={!isOnline}
                                                onChange={() => {}}
                                                className="rounded border-zinc-700 bg-zinc-900 disabled:cursor-not-allowed"
                                            />
                                            <div>
                                                <p className={`text-sm font-mono ${!isOnline ? "text-zinc-500" : "text-zinc-200"}`}>
                                                    {machine.user || machine.address}
                                                </p>
                                                <p className="text-xs text-gray-500 font-mono">{machine.address}</p>
                                            </div>
                                        </div>
                                        
                                        <span className={`text-xs font-mono px-2 py-0.5 rounded ${
                                            isOnline ? "bg-zinc-800 text-emerald-400" : "bg-zinc-900 text-rose-600"
                                        }`}>
                                            {isOnline ? "online" : "offline"}
                                        </span>
                                    </div>
                                );
                            })}
                    </div>
                </div>
                <select
                    className="w-full border  bg-accent-dark rounded-md p-2 text-sm focus:ring-2 outline-none"
                    value={activeConfig?.name || ""}
                    onChange={(e) => setSelectedName(e.target.value)}
                >
                    {configs.length === 0 ? (
                    <option value="" disabled>Loading templates...</option>
                    ) : (
                    configs.map((cfg) => (
                        <option key={cfg.name} value={cfg.name}>
                        {cfg.name} {cfg.description ? `(${cfg.description})` : ""}
                        </option>
                    ))
                    )}
                </select>
            </div>
            {/* NOTE: changing key forces component to reinitialize */}
           {activeConfig ? <GenericConfigEditor<ContainerConfig>
            key={activeConfig.id}
            title={activeConfig.name}
            apiEndpoint="containers/deploy"
            initialConfig={activeConfig}
            renderUiForm={(config, updateConfig) => (
                <div className="flex flex-col gap-2">
                    <ContainerForm config={config} update={updateConfig} />

                </div>
            )}
            onSave={async(updatedConfig) => {console.log("savingawdw", updatedConfig)}}
           >
            
           </GenericConfigEditor>
           : <div>No configurations</div>}

        </BaseModal>
    )
});

