import { makeAutoObservable, runInAction } from "mobx";
import { CustomApiRequest } from "../../../../FetchAPI";

export type EditMode = "ui" | "json";

export class ConfigEditorStore<T extends object = object> {
  // Current valid data object
  config: T;
  initialConfig: T;
  
  // Current active editor view mode
  mode: EditMode = "ui";
  
  // Text string for raw JSON editor
  jsonText: string = "";
  
  // Syntax or structural error message from JSON editing
  jsonError: string | null = null;
  apiError: string | null = null;

  constructor(initialConfig: T) {
    this.config = initialConfig;
    this.initialConfig = initialConfig;
    this.jsonText = JSON.stringify(initialConfig, null, 2);
    makeAutoObservable(this);
  }

  // Set view mode and sync representations
  setMode(newMode: EditMode) {
    if (newMode === "json") {
      // Sync object to JSON text string when switching to JSON mode
      this.jsonText = JSON.stringify(this.config, null, 2);
      this.jsonError = null;
    } else if (newMode === "ui") {
      // Validate and apply JSON text to config object when switching to UI mode
      const isValid = this.applyJsonText();
      if (!isValid) return; // Block tab switch if JSON is invalid
    }
    this.mode = newMode;
  }

  // Handle direct text changes in the raw JSON editor
  setJsonText(text: string) {
    this.jsonText = text;
    this.applyJsonText(); // Live validate on edit
  }

  // Update object state directly from UI forms
  updateConfig(updater: (draft: T) => void) {
    // Basic mutable draft pattern
    const draft = JSON.parse(JSON.stringify(this.config));
    updater(draft);
    this.config = draft;
    this.jsonText = JSON.stringify(this.config, null, 2);
    this.jsonError = null;
  }

  save = async (apiEndpoint: string) => {
        try {
            const response = await CustomApiRequest<T>(apiEndpoint, this.config, "POST");
            console.log("saving", apiEndpoint)
            console.log(response);
        } catch(err) {
            runInAction(() => {
                this.apiError = (err as Error).message;
            });
        }
  }

  reset = () => {
    this.config = this.initialConfig;
  }

  // Helper: Try parsing JSON text and updating internal object state
  private applyJsonText(): boolean {
    try {
      const parsed = JSON.parse(this.jsonText);
      this.config = parsed;
      this.jsonError = null;
      return true;
    } catch (err) {
      this.jsonError = (err as Error).message;
      return false;
    }
  }
}