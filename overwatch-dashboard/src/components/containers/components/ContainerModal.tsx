import { observer } from "mobx-react-lite";
import { useState } from "react";
import { BaseModal, type BaseModalProps } from "../../common/BaseModal";
import { GenericConfigEditor } from "../../common/ConfigEditor/ConfigEditor";
import type { ContainerConfig } from "../types/configs";
import { containerStore } from "../../../stores/ContainerStore";
export const ContainerModal = observer(({isOpen, onClose}: BaseModalProps) => {

    const [selectedName, setSelectedName] = useState<string>("");

    // Convert MobX Map values into an array for the dropdown options
    const configs: ContainerConfig[] = Array.from(containerStore.configMap.values());
    
    // Determine the active config (fallback to the first one if none selected)
    const activeConfig = configs.find(c => c.name === selectedName) || configs[0];

    return (
        <BaseModal maxWidth="max-w-4xl" isOpen={isOpen} onClose={onClose}>
            <div>
                <label className="block text-sm font-semibold">
                    Add Container
                </label>
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
           <GenericConfigEditor<ContainerConfig>
            key={activeConfig.id}
            title={activeConfig.name}
            apiEndpoint=""
            initialConfig={activeConfig}
            renderUiForm={(config, updateConfig) => (
                <>
                <div>{config.name}</div>
                </>
            )}
           >

           </GenericConfigEditor>

        </BaseModal>
    )
});

