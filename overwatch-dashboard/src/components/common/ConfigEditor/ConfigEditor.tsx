import React, { useState } from "react";
import { observer } from "mobx-react-lite";
import { ConfigEditorStore, type EditMode } from "./stores/ConfigEditorStore";

interface Props<T extends object> {
  title: string;
  subtitle?: string;
  initialConfig: T;
  apiEndpoint?: string;
  // Inject custom component to render
  renderUiForm: (
    config: T,
    update: (updater: (draft: T) => void) => void
  ) => React.ReactNode;
  onSave?: (config: T) => void;
}


export const GenericConfigEditor = observer(
  <T extends object>({ initialConfig, renderUiForm, onSave, title, subtitle, apiEndpoint}: Props<T>) => {

    // FIXME: may be used in future when displaying multiple configs
    const [isExpanded, setIsExpanded] = useState(true);
    const [store] = useState(() => new ConfigEditorStore<T>(initialConfig));

    const handleSave = async () => {
      if (store.jsonError) {
        alert("Please fix JSON syntax errors before saving.");
        return;
      }
      //  FIXME: allow optional override?
      onSave?.(store.config);
      if (apiEndpoint) {
        await store.save(apiEndpoint)
      }
      
     
    };

    const handleReset = () => {
      store.reset();
    }

    const handleUiToggle = (e: React.MouseEvent<HTMLButtonElement>, mode: EditMode) => {
      e.stopPropagation();
      store.setMode(mode);
    }

    return (
      <div className="flex flex-col w-full border rounded-lg overflow-hidden shadow-xl">
        {/* Toggle mode */}
        <div  className="flex justify-between px-4 py-3 border-b">
          <hgroup>
          <h1>{title}</h1>
          <p><small>{subtitle}</small></p>
          </hgroup>
          <div className={`${isExpanded ? "flex justify-around space-x-10" : "hidden"}`}>
          <div className="flex items-center space-x-1 bg-surface-card-dark p-1 rounded-md border">
           
            <button
              onClick={(e) => handleUiToggle(e, "ui")}
              className={`px-3 py-1.5 text-xs font-semibold rounded ${
                store.mode === "ui"
                  ? "bg-primary-light dark:bg-primary-dark shadow"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              UI
            </button>
            <button
              onClick={(e) => handleUiToggle(e, "json") }
              className={`px-3 py-1.5 text-xs font-semibold rounded ${
                store.mode === "json"
                  ? "bg-primary-light dark:bg-primary-dark shadow"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              JSON
            </button>
          </div>

          <div className="flex items-center space-x-3">
            {store.jsonError && (
              <span className="text-xs text-red-400 font-mono animate-pulse">
                Invalid JSON Syntax
              </span>
            )}
            {onSave && (
              <button
                onClick={handleSave}
                disabled={!!store.jsonError}
                className="px-4 py-1.5 bg-emerald-500 hover:bg-emerald-300 disabled:opacity-50 text-white text-xs font-bold rounded"
              >
                Save Changes
              </button>
            )}
            {<button
              onClick={handleReset}
              className="px-4 py-1.5 bg-rose-700 hover:bg-rose-500 disabled:opacity-50 text-xs font-bold rounded"
              >Reset</button>}

          </div>
          </div>
        </div>

        {/* Render custom UI */}
        <div className={`  ${isExpanded ? "flex-1 overflow-auto p-4" : "hidden"}`}>
          {store.mode === "ui" ? (
            renderUiForm(store.config, (fn) => store.updateConfig(fn))
          ) : (
            <div className="h-full flex flex-col space-y-2">
              <textarea
                value={store.jsonText}
                onChange={(e) => store.setJsonText(e.target.value)}
                className="w-full h-96 font-mono text-sm bg-surface-dark text-emerald-400 p-4 rounded border border-gray-700 focus:outline-none focus:border-blue-500 resize-none"
                spellCheck={false}
              />
              {store.jsonError && (
                <div className="p-3 bg-red-950/80 border border-red-700 rounded text-red-200 font-mono text-xs">
                  {store.jsonError}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }
);